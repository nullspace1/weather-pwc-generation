
from typing import Literal, TypedDict, Union

from pydantic import BaseModel


class WeatherDailyData(BaseModel):
    time: list[str]
    temperature_2m_mean: list[float]
    precipitation_sum: list[float]
    wind_speed_10m_mean: list[float]
    shortwave_radiation_sum: list[float]
    et0_fao_evapotranspiration: list[float]
    
    
class WeatherResult(BaseModel):
    latitude : float
    longitude : float
    daily: WeatherDailyData
    
class UnitConversion(TypedDict):
    scale: float
    offset: float
    
type PrecipitationUnits = Literal["cm/day", "mm/day", "in/day"]
type TemperatureUnits = Literal["C", "F", "K"]
type WindSpeedUnits = Literal["m/s", "km/h", "mph"]
type RadiationUnits = Literal["W/m²", "kW/m²", "MJ/m^2/day", "La/day"]
type ETZeroUnits = Literal["cm/day", "mm/day", "in/day"]

type Units = Union[PrecipitationUnits, TemperatureUnits, WindSpeedUnits, RadiationUnits, ETZeroUnits]

class ConfigUnits(BaseModel):
    precipitation_sum: PrecipitationUnits
    temperature_2m_mean: TemperatureUnits
    wind_speed_10m_mean: WindSpeedUnits
    shortwave_radiation_sum: RadiationUnits
    et0_fao_evapotranspiration: ETZeroUnits
  


    