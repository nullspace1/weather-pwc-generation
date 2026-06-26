from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from backend.dto.weather.input import WeatherDataRequestDTO
from backend.model.weather import ConfigUnits
from backend.services.weather.weather import NoOutputFolderSelectedError, WeatherService


def _build_service(
    config: MagicMock | None = None,
    converter_service: MagicMock | None = None,
    weather_api_service: MagicMock | None = None,
    folder_selection_service: MagicMock | None = None,
) -> tuple[WeatherService, MagicMock, MagicMock, MagicMock, MagicMock]:
    config = config or MagicMock()
    converter_service = converter_service or MagicMock()
    weather_api_service = weather_api_service or MagicMock()
    folder_selection_service = folder_selection_service or MagicMock()
    return (
        WeatherService(config, converter_service, weather_api_service, folder_selection_service),
        config,
        converter_service,
        weather_api_service,
        folder_selection_service,
    )


@patch.object(pd.DataFrame, "to_csv")
def test_generate_weather_data_fetches_converts_and_exports(
    mock_to_csv, sample_weather_result, default_config_units
):
    service, config, converter_service, weather_api_service, folder_selection_service = _build_service()
    config.units = default_config_units
    weather_api_service.get_data.return_value = sample_weather_result
    converter_service.convert.return_value = sample_weather_result
    folder_selection_service.get_selected_folder.return_value = "/picked/dir"
    dto = WeatherDataRequestDTO(
        lat=52.5,
        lon=13.4,
        from_date="2024-01-01",
        to_date="2024-01-02",
        file_name="data.wea",
    )

    file_path = service.generate_weather_data(dto)

    weather_api_service.get_data.assert_called_once_with(
        52.5, 13.4, date(2024, 1, 1), date(2024, 1, 2)
    )
    converter_service.convert.assert_called_once_with(
        sample_weather_result, default_config_units
    )
    mock_to_csv.assert_called_once_with(Path("/picked/dir/data.wea"), index=False)
    assert file_path == str(Path("/picked/dir/data.wea"))


@patch.object(pd.DataFrame, "to_csv")
def test_generate_weather_data_builds_dataframe_columns(
    mock_to_csv, sample_weather_result, default_config_units
):
    service, config, converter_service, weather_api_service, folder_selection_service = _build_service()
    config.units = default_config_units
    weather_api_service.get_data.return_value = sample_weather_result
    converter_service.convert.return_value = sample_weather_result
    folder_selection_service.get_selected_folder.return_value = "/picked/dir"
    dto = WeatherDataRequestDTO(
        lat=0.0,
        lon=0.0,
        from_date="2024-01-01",
        to_date="2024-01-02",
        file_name="weather.csv",
    )

    with patch("backend.services.weather.weather.pd.DataFrame") as mock_dataframe:
        mock_df = MagicMock()
        mock_dataframe.return_value = mock_df
        service.generate_weather_data(dto)

    mock_dataframe.assert_called_once_with(
        {
            "time": sample_weather_result.daily.time,
            "temperature_2m_mean": sample_weather_result.daily.temperature_2m_mean,
            "precipitation_sum": sample_weather_result.daily.precipitation_sum,
            "wind_speed_10m_mean": sample_weather_result.daily.wind_speed_10m_mean,
            "shortwave_radiation_sum": sample_weather_result.daily.shortwave_radiation_sum,
            "et0_fao_evapotranspiration": sample_weather_result.daily.et0_fao_evapotranspiration,
        }
    )
    mock_df.to_csv.assert_called_once_with(Path("/picked/dir/weather.csv"), index=False)


def test_generate_weather_data_raises_when_no_folder_selected(sample_weather_result):
    service, config, converter_service, weather_api_service, folder_selection_service = _build_service()
    folder_selection_service.get_selected_folder.return_value = None
    dto = WeatherDataRequestDTO(
        lat=0.0,
        lon=0.0,
        from_date="2024-01-01",
        to_date="2024-01-02",
        file_name="weather.csv",
    )

    with pytest.raises(NoOutputFolderSelectedError):
        service.generate_weather_data(dto)

    weather_api_service.get_data.assert_not_called()
