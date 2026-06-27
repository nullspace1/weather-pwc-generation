from datetime import date
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from backend.dto.weather.input import WeatherDataRequestDTO
from backend.model.weather import WeatherDailyData, WeatherResult
from backend.services.export.export import ExportService
from backend.services.weather.weather import NoOutputFolderSelectedError, WeatherService


def _build_service(
    converter_service: MagicMock | None = None,
    weather_api_service: MagicMock | None = None,
    folder_selection_service: MagicMock | None = None,
    export_service: ExportService | None = None,
    report_cache_service: MagicMock | None = None,
) -> tuple[WeatherService, MagicMock, MagicMock, MagicMock, MagicMock]:
    converter_service = converter_service or MagicMock()
    weather_api_service = weather_api_service or MagicMock()
    folder_selection_service = folder_selection_service or MagicMock()
    export_service = export_service or ExportService()
    report_cache_service = report_cache_service or MagicMock()
    return (
        WeatherService(
            converter_service,
            weather_api_service,
            folder_selection_service,
            export_service,
            report_cache_service,
        ),
        converter_service,
        weather_api_service,
        folder_selection_service,
        report_cache_service,
    )


def test_generate_weather_data_fetches_converts_and_exports(
    sample_weather_result, tmp_path
):
    service, converter_service, weather_api_service, folder_selection_service, _ = _build_service()
    weather_api_service.get_data.return_value = sample_weather_result
    converter_service.convert.return_value = sample_weather_result
    folder_selection_service.get_selected_folder.return_value = str(tmp_path)
    dto = WeatherDataRequestDTO(
        lat=52.5,
        lon=13.4,
        from_date="2024-01-01",
        to_date="2024-01-02",
        report_name="data.wea",
    )

    file_path = service.generate_weather_data(dto)

    weather_api_service.get_data.assert_called_once_with(
        52.5, 13.4, date(2024, 1, 1), date(2024, 1, 2)
    )
    converter_service.convert.assert_called_once_with(sample_weather_result)
    assert file_path == str(Path(tmp_path) / "data.wea")
    assert (tmp_path / "data.wea").exists()


def test_generate_weather_data_sanitizes_report_name(tmp_path, sample_weather_result):
    service, converter_service, weather_api_service, folder_selection_service, _ = _build_service()
    weather_api_service.get_data.return_value = sample_weather_result
    converter_service.convert.return_value = sample_weather_result
    folder_selection_service.get_selected_folder.return_value = str(tmp_path)
    dto = WeatherDataRequestDTO(
        lat=52.5,
        lon=13.4,
        from_date="2024-01-01",
        to_date="2024-01-02",
        report_name="My Report 2024",
    )

    file_path = service.generate_weather_data(dto)

    assert file_path == str(Path(tmp_path) / "My_Report_2024.wea")
    assert (tmp_path / "My_Report_2024.wea").exists()


def test_generate_weather_data_writes_wea_file_format(tmp_path):
    service, converter_service, weather_api_service, folder_selection_service, _ = _build_service()
    weather_result = WeatherResult(
        latitude=52.5,
        longitude=13.4,
        daily=WeatherDailyData(
            time=["2011-01-01"],
            temperature_2m_mean=[25.9],
            precipitation_sum=[0.0],
            wind_speed_10m_mean=[432.4],
            shortwave_radiation_sum=[880.3],
            et0_fao_evapotranspiration=[6.5],
        ),
    )
    weather_api_service.get_data.return_value = weather_result
    converter_service.convert.return_value = weather_result
    folder_selection_service.get_selected_folder.return_value = str(tmp_path)
    dto = WeatherDataRequestDTO(
        lat=52.5,
        lon=13.4,
        from_date="2011-01-01",
        to_date="2011-01-01",
        report_name="output.wea",
    )

    service.generate_weather_data(dto)

    content = (tmp_path / "output.wea").read_text(encoding="utf-8")
    assert content == "1,1,11,0,6.5,25.9,432.4,880.3,,\n"
    assert "month" not in content


def test_generate_weather_data_raises_when_no_folder_selected(sample_weather_result):
    service, converter_service, weather_api_service, folder_selection_service, _ = _build_service()
    folder_selection_service.get_selected_folder.return_value = None
    dto = WeatherDataRequestDTO(
        lat=0.0,
        lon=0.0,
        from_date="2024-01-01",
        to_date="2024-01-02",
        report_name="weather.wea",
    )

    with pytest.raises(NoOutputFolderSelectedError):
        service.generate_weather_data(dto)

    weather_api_service.get_data.assert_not_called()


def test_generate_weather_data_caches_report_when_requested(
    sample_weather_result, tmp_path
):
    service, converter_service, weather_api_service, folder_selection_service, report_cache_service = _build_service()
    weather_api_service.get_data.return_value = sample_weather_result
    converter_service.convert.return_value = sample_weather_result
    folder_selection_service.get_selected_folder.return_value = str(tmp_path)
    dto = WeatherDataRequestDTO(
        lat=52.5,
        lon=13.4,
        from_date="2024-01-01",
        to_date="2024-01-02",
        report_name="cached-report",
        save_to_cache=True,
    )

    file_path = service.generate_weather_data(dto)

    report_cache_service.save_report.assert_called_once_with(
        "cached-report",
        file_path,
        location_name="52.5, 13.4",
        latitude=52.5,
        longitude=13.4,
        from_date="2024-01-01",
        to_date="2024-01-02",
    )
