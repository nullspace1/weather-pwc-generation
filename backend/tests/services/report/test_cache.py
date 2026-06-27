from pathlib import Path
from unittest.mock import MagicMock

import pytest

from backend.services.folder.selection import FolderSelectionCancelledError
from backend.services.report.cache import ReportCacheService, ReportNotFoundError
from backend.services.storage.storage import StorageService

REPORT_METADATA = {
    "location_name": "Berlin, Germany",
    "latitude": 52.52,
    "longitude": 13.405,
    "from_date": "2024-01-01",
    "to_date": "2024-01-31",
}


def _build_service(tmp_path, cache_dir=None, picker=None):
    db_path = tmp_path / "locations.db"
    cache_dir = cache_dir or tmp_path / "reports"
    storage = StorageService(sqlite_db=str(db_path))
    picker = picker or MagicMock()
    service = ReportCacheService(
        storage_service=storage,
        cache_dir=str(cache_dir),
        folder_picker_service=picker,
    )
    return service, storage, cache_dir, picker


def test_save_report_copies_file_and_creates_metadata(tmp_path):
    service, _, cache_dir, _ = _build_service(tmp_path)
    source = tmp_path / "source.wea"
    source.write_text("1,1,11,0,6.5,25.9,432.4,880.3,,\n", encoding="utf-8")

    service.save_report("My Report", str(source), **REPORT_METADATA)

    reports = service.list_reports()
    assert len(reports) == 1
    assert reports[0].name == "My Report"
    assert reports[0].file_name == "My_Report.wea"
    assert reports[0].location_name == "Berlin, Germany"
    assert reports[0].latitude == 52.52
    assert reports[0].from_date == "2024-01-01"
    assert reports[0].to_date == "2024-01-31"
    assert (cache_dir / "My_Report.wea").exists()


def test_list_reports_returns_saved_reports(tmp_path):
    service, _, _, _ = _build_service(tmp_path)
    source = tmp_path / "source.wea"
    source.write_text("data", encoding="utf-8")
    service.save_report("Report A", str(source), **REPORT_METADATA)
    service.save_report("Report B", str(source), **REPORT_METADATA)

    reports = service.list_reports()

    assert len(reports) == 2
    names = {report.name for report in reports}
    assert names == {"Report A", "Report B"}


def test_delete_report_removes_file_and_metadata(tmp_path):
    service, _, cache_dir, _ = _build_service(tmp_path)
    source = tmp_path / "source.wea"
    source.write_text("data", encoding="utf-8")
    service.save_report("To Delete", str(source), **REPORT_METADATA)

    service.delete_report("To Delete")

    assert service.list_reports() == []
    assert not (cache_dir / "To_Delete.wea").exists()


def test_save_report_overwrites_existing_entry(tmp_path):
    service, _, cache_dir, _ = _build_service(tmp_path)
    source_a = tmp_path / "source_a.wea"
    source_b = tmp_path / "source_b.wea"
    source_a.write_text("first", encoding="utf-8")
    source_b.write_text("second", encoding="utf-8")
    service.save_report("Same Name", str(source_a), **REPORT_METADATA)
    updated_metadata = {**REPORT_METADATA, "from_date": "2024-06-01", "to_date": "2024-06-30"}
    service.save_report("Same Name", str(source_b), **updated_metadata)

    reports = service.list_reports()

    assert len(reports) == 1
    assert reports[0].from_date == "2024-06-01"
    assert (cache_dir / "Same_Name.wea").read_text(encoding="utf-8") == "second"


def test_export_report_copies_to_picked_folder(tmp_path):
    picker = MagicMock()
    export_dir = tmp_path / "export"
    export_dir.mkdir()
    picker.pick_folder.return_value = str(export_dir)
    service, _, _, _ = _build_service(tmp_path, picker=picker)
    source = tmp_path / "source.wea"
    source.write_text("cached-data", encoding="utf-8")
    service.save_report("My Report", str(source), **REPORT_METADATA)

    file_path = service.export_report("My Report")

    assert file_path == str(export_dir / "My_Report.wea")
    assert (export_dir / "My_Report.wea").read_text(encoding="utf-8") == "cached-data"
    picker.pick_folder.assert_called_once()


def test_export_report_raises_when_report_not_found(tmp_path):
    service, _, _, _ = _build_service(tmp_path)

    with pytest.raises(ReportNotFoundError):
        service.export_report("Missing Report")


def test_export_report_raises_when_folder_selection_cancelled(tmp_path):
    picker = MagicMock()
    picker.pick_folder.return_value = None
    service, _, _, _ = _build_service(tmp_path, picker=picker)
    source = tmp_path / "source.wea"
    source.write_text("data", encoding="utf-8")
    service.save_report("My Report", str(source), **REPORT_METADATA)

    with pytest.raises(FolderSelectionCancelledError):
        service.export_report("My Report")
