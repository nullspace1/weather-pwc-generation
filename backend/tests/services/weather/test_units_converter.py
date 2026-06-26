from backend.model.weather import ConfigUnits, WeatherDailyData, WeatherResult
from backend.services.weather.units_converter import WeatherConverterService


def _make_weather_result() -> WeatherResult:
    return WeatherResult(
        latitude=0.0,
        longitude=0.0,
        daily=WeatherDailyData(
            time=["2024-01-01"],
            temperature_2m_mean=[10.0],
            precipitation_sum=[10.0],
            wind_speed_10m_mean=[10.0],
            shortwave_radiation_sum=[10.0],
            et0_fao_evapotranspiration=[1.0],
        ),
    )


def test_convert_keeps_values_when_units_match_api_defaults():
    service = WeatherConverterService()
    weather_data = _make_weather_result()
    units = ConfigUnits(
        precipitation_sum="mm/day",
        et0_fao_evapotranspiration="mm/day",
        temperature_2m_mean="C",
        wind_speed_10m_mean="km/h",
        shortwave_radiation_sum="MJ/m^2/day",
    )

    result = service.convert(weather_data, units)

    assert result.daily.temperature_2m_mean == [10.0]
    assert result.daily.precipitation_sum == [10.0]
    assert result.daily.wind_speed_10m_mean == [10.0]
    assert result.daily.shortwave_radiation_sum == [10.0]


def test_convert_temperature_to_fahrenheit():
    service = WeatherConverterService()
    weather_data = _make_weather_result()
    units = ConfigUnits(
        precipitation_sum="mm/day",
        et0_fao_evapotranspiration="mm/day",
        temperature_2m_mean="F",
        wind_speed_10m_mean="km/h",
        shortwave_radiation_sum="MJ/m^2/day",
    )

    result = service.convert(weather_data, units)

    assert result.daily.temperature_2m_mean == [18.0]


def test_convert_precipitation_to_cm_per_day():
    service = WeatherConverterService()
    weather_data = _make_weather_result()
    units = ConfigUnits(
        precipitation_sum="cm/day",
        et0_fao_evapotranspiration="mm/day",
        temperature_2m_mean="C",
        wind_speed_10m_mean="km/h",
        shortwave_radiation_sum="MJ/m^2/day",
    )

    result = service.convert(weather_data, units)

    assert result.daily.precipitation_sum == [1.0]


def test_convert_wind_speed_to_meters_per_second():
    service = WeatherConverterService()
    weather_data = _make_weather_result()
    units = ConfigUnits(
        precipitation_sum="mm/day",
        et0_fao_evapotranspiration="mm/day",
        temperature_2m_mean="C",
        wind_speed_10m_mean="m/s",
        shortwave_radiation_sum="MJ/m^2/day",
    )

    result = service.convert(weather_data, units)

    assert result.daily.wind_speed_10m_mean == [36.0]


def test_convert_radiation_to_kilowatts_per_square_meter():
    service = WeatherConverterService()
    weather_data = _make_weather_result()
    units = ConfigUnits(
        precipitation_sum="mm/day",
        et0_fao_evapotranspiration="mm/day",
        temperature_2m_mean="C",
        wind_speed_10m_mean="km/h",
        shortwave_radiation_sum="kW/m²",
    )

    result = service.convert(weather_data, units)

    assert result.daily.shortwave_radiation_sum == [0.01]
