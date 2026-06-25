from datetime import date

import pytest

from model.weather import ConfigUnits, WeatherDailyData, WeatherResult


@pytest.fixture
def sample_weather_result() -> WeatherResult:
    return WeatherResult(
        latitude=52.5,
        longitude=13.4,
        daily=WeatherDailyData(
            time=["2024-01-01", "2024-01-02"],
            temperature_2m_mean=[10.0, 12.0],
            precipitation_sum=[1.0, 2.0],
            wind_speed_10m_mean=[15.0, 20.0],
            shortwave_radiation_sum=[5.0, 6.0],
            et0_fao_evapotranspiration=[0.5, 0.6],
        ),
    )


@pytest.fixture
def default_config_units() -> ConfigUnits:
    return ConfigUnits(
        precipitation_sum="mm/day",
        et0_fao_evapotranspiration="mm/day",
        temperature_2m_mean="C",
        wind_speed_10m_mean="km/h",
        shortwave_radiation_sum="MJ/m^2/day",
    )


@pytest.fixture
def weather_date_range() -> tuple[date, date]:
    return date(2024, 1, 1), date(2024, 1, 2)
