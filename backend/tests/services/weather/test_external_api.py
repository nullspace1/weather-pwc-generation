from datetime import date
from unittest.mock import MagicMock, patch

from backend.services.weather.external_api import WeatherAPIService


@patch("backend.services.weather.external_api.requests.get")
def test_get_data_returns_weather_result(mock_get, sample_weather_result):
    mock_get.return_value = MagicMock(
        json=MagicMock(return_value=sample_weather_result.model_dump())
    )
    service = WeatherAPIService()
    from_date = date(2024, 1, 1)
    to_date = date(2024, 1, 2)

    result = service.get_data(52.5, 13.4, from_date, to_date)

    assert result.latitude == 52.5
    assert result.longitude == 13.4
    assert result.daily.time == ["2024-01-01", "2024-01-02"]
    assert result.daily.temperature_2m_mean == [10.0, 12.0]


@patch("backend.services.weather.external_api.requests.get")
def test_get_data_builds_open_meteo_url(mock_get, sample_weather_result):
    mock_get.return_value = MagicMock(
        json=MagicMock(return_value=sample_weather_result.model_dump())
    )
    service = WeatherAPIService()
    from_date = date(2024, 1, 1)
    to_date = date(2024, 1, 31)

    service.get_data(40.7, -74.0, from_date, to_date)

    called_url = mock_get.call_args[0][0]
    assert "latitude=40.7" in called_url
    assert "longitude=-74.0" in called_url
    assert "start_date=2024-01-01" in called_url
    assert "end_date=2024-01-31" in called_url
    assert "daily=temperature_2m_mean,precipitation_sum,wind_speed_10m_mean,shortwave_radiation_sum,et0_fao_evapotranspiration" in called_url
