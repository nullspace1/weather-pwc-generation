import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol

from backend.dto.report.output import ReportDTO
from backend.model.report import CachedReport
from backend.services.folder.picker import FolderPickerServiceProtocol
from backend.services.folder.selection import FolderSelectionCancelledError
from backend.services.storage.storage import StorageServiceProtocol
from backend.services.weather.report_name import to_file_name


class ReportNotFoundError(Exception):
    pass


class ReportCacheServiceProtocol(Protocol):
    def save_report(
        self,
        report_name: str,
        source_path: str,
        *,
        location_name: str | None,
        latitude: float,
        longitude: float,
        from_date: str,
        to_date: str,
    ) -> None:
        ...

    def list_reports(self) -> list[ReportDTO]:
        ...

    def delete_report(self, report_name: str) -> None:
        ...

    def export_report(self, report_name: str) -> str:
        ...


class ReportCacheService(ReportCacheServiceProtocol):
    def __init__(
        self,
        storage_service: StorageServiceProtocol,
        cache_dir: str,
        folder_picker_service: FolderPickerServiceProtocol,
    ) -> None:
        self.storage_service = storage_service
        self.cache_dir = Path(cache_dir).expanduser()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._folder_picker_service = folder_picker_service

    def save_report(
        self,
        report_name: str,
        source_path: str,
        *,
        location_name: str | None,
        latitude: float,
        longitude: float,
        from_date: str,
        to_date: str,
    ) -> None:
        file_name = to_file_name(report_name)
        destination = self.cache_dir / file_name
        shutil.copy2(source_path, destination)
        created_at = datetime.now(timezone.utc).isoformat()
        self.storage_service.upsert_cached_report(
            CachedReport(
                name=report_name,
                file_name=file_name,
                created_at=created_at,
                location_name=location_name,
                latitude=latitude,
                longitude=longitude,
                from_date=from_date,
                to_date=to_date,
            )
        )

    def list_reports(self) -> list[ReportDTO]:
        reports = self.storage_service.get_all_cached_reports()
        return [
            ReportDTO(
                name=report.name,
                file_name=report.file_name,
                created_at=report.created_at,
                location_name=report.location_name,
                latitude=report.latitude,
                longitude=report.longitude,
                from_date=report.from_date,
                to_date=report.to_date,
            )
            for report in reports
        ]

    def delete_report(self, report_name: str) -> None:
        report = self.storage_service.get_cached_report(report_name)
        if report is None:
            return
        file_path = self.cache_dir / report.file_name
        if file_path.exists():
            file_path.unlink()
        self.storage_service.delete_cached_report(report_name)

    def export_report(self, report_name: str) -> str:
        report = self.storage_service.get_cached_report(report_name)
        if report is None:
            raise ReportNotFoundError()
        source_path = self.cache_dir / report.file_name
        if not source_path.exists():
            raise ReportNotFoundError()
        folder = self._folder_picker_service.pick_folder()
        if folder is None:
            raise FolderSelectionCancelledError()
        destination = Path(folder) / report.file_name
        shutil.copy2(source_path, destination)
        return str(destination)
