from backend.model.weather import WeatherDailyData, WeatherResult
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


def test_convert_keeps_mm_per_day_and_celsius():
    service = WeatherConverterService()
    weather_data = _make_weather_result()

    result = service.convert(weather_data)

    assert result.daily.temperature_2m_mean == [10.0]
    assert result.daily.precipitation_sum == [10.0]
    assert result.daily.et0_fao_evapotranspiration == [1.0]


def test_convert_wind_speed_to_cm_per_second():
    service = WeatherConverterService()
    weather_data = _make_weather_result()

    result = service.convert(weather_data)

    assert result.daily.wind_speed_10m_mean == [10.0 * 100.0 / 3.6]


def test_convert_radiation_to_langley_per_day():
    service = WeatherConverterService()
    weather_data = _make_weather_result()

    result = service.convert(weather_data)

    assert result.daily.shortwave_radiation_sum == [239.005736]
