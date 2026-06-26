
from typing import Literal, Protocol, TypeVar



from backend.model.weather import ConfigUnits, UnitConversion, Units, WeatherResult


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

    FROM_API_UNITS: dict[str, dict[str, UnitConversion]] = {
    "precipitation_sum": {
        "mm/day": {"scale": 1.0, "offset": 0.0},
        "cm/day": {"scale": 0.1, "offset": 0.0},
        "in/day": {"scale": 0.0393701, "offset": 0.0},
    },
    "et0_fao_evapotranspiration": {
        "mm/day": {"scale": 1.0, "offset": 0.0},
        "cm/day": {"scale": 0.1, "offset": 0.0},
        "in/day": {"scale": 0.0393701, "offset": 0.0},
    },
    "temperature_2m_mean": {
        "C": {"scale": 1.0, "offset": 0.0},
        "F": {"scale": 1.8, "offset": 32.0},
        "K": {"scale": 1.0, "offset": 273.15},
    },
    "wind_speed_10m_mean": {
        "km/h": {"scale": 1.0, "offset": 0.0},
        "m/s": {"scale": 1 / 3.6, "offset": 0.0},
        "mph": {"scale": 0.621371, "offset": 0.0},
    },
    "shortwave_radiation_sum": {
        "MJ/m^2/day": {"scale": 1.0, "offset": 0.0},
        "La/day": {"scale": 23.8846, "offset": 0.0},
        "W/m²": {"scale": 11.574074, "offset": 0.0},
        "kW/m²": {"scale": 0.011574074, "offset": 0.0},
    },
}
    
    def convert(self, weather_data: WeatherResult, units: ConfigUnits) -> WeatherResult:
        
        weather_data.daily.precipitation_sum = [self._convert(value, "precipitation_sum", units.precipitation_sum) for value in weather_data.daily.precipitation_sum]
        weather_data.daily.temperature_2m_mean = [self._convert(value, "temperature_2m_mean", units.temperature_2m_mean) for value in weather_data.daily.temperature_2m_mean]
        weather_data.daily.wind_speed_10m_mean = [self._convert(value, "wind_speed_10m_mean", units.wind_speed_10m_mean) for value in weather_data.daily.wind_speed_10m_mean]
        weather_data.daily.shortwave_radiation_sum = [self._convert(value, "shortwave_radiation_sum", units.shortwave_radiation_sum) for value in weather_data.daily.shortwave_radiation_sum]
        weather_data.daily.et0_fao_evapotranspiration = [self._convert(value, "et0_fao_evapotranspiration", units.et0_fao_evapotranspiration) for value in weather_data.daily.et0_fao_evapotranspiration]
        return weather_data


    def _convert(self, value: float, parameter: str, to_unit: Units) -> float:
        conversion = self.FROM_API_UNITS[parameter][to_unit]
        return value * conversion["scale"] + conversion["offset"]