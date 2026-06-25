
from typing import Literal, Protocol, TypeVar



from model.weather import ConfigUnits, Units, WeatherResult


class WeatherConverterServiceProtocol(Protocol):
    def convert(self, weather_data: WeatherResult, units: ConfigUnits) -> WeatherResult:
        ...

class WeatherConverterService(WeatherConverterServiceProtocol):
    
    API_UNITS: dict[str, Units] = {
        "precipitation_sum": "mm/day",
        "et0_fao_evapotranspiration": "mm/day",
        "temperature_2m_mean": "C",
        "wind_speed_10m_mean": "km/h",
        "shortwave_radiation_sum": "MJ/m^2/day"
    }

    FROM_API_UNITS: dict[str, dict[Units, float]] = {
        "precipitation_sum": {
            "cm/day": 0.1,
            "mm/day": 1,
            "in/day": 0.0393701
        },
        "et0_fao_evapotranspiration": {
            "cm/day": 0.1,
            "mm/day": 1,
            "in/day": 0.0393701
        },
        "temperature_2m_mean": {
            "C": 1,
            "F": 1.8,
            "K": 1
        },
        "wind_speed_10m_mean": {
            "m/s": 3.6,
            "km/h": 1,
            "mph": 0.44704
        },
        "shortwave_radiation_sum": {
            "W/m²": 1,
            "kW/m²": 0.001,
            "MJ/m^2/day": 1,
            "La/day": 0.48426
        }
    }
    
    def convert(self, weather_data: WeatherResult, units: ConfigUnits) -> WeatherResult:
        
        weather_data.daily.precipitation_sum = [self._convert(value, "precipitation_sum", units.precipitation_sum) for value in weather_data.daily.precipitation_sum]
        weather_data.daily.temperature_2m_mean = [self._convert(value, "temperature_2m_mean", units.temperature_2m_mean) for value in weather_data.daily.temperature_2m_mean]
        weather_data.daily.wind_speed_10m_mean = [self._convert(value, "wind_speed_10m_mean", units.wind_speed_10m_mean) for value in weather_data.daily.wind_speed_10m_mean]
        weather_data.daily.shortwave_radiation_sum = [self._convert(value, "shortwave_radiation_sum", units.shortwave_radiation_sum) for value in weather_data.daily.shortwave_radiation_sum]
        
        return weather_data


    def _convert(self, value: float, parameter: str, to_unit: Units) -> float:
        return value * self.FROM_API_UNITS[parameter][to_unit]