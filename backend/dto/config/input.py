

from pydantic import BaseModel

from backend.model.weather import ETZeroUnits, PrecipitationUnits, RadiationUnits, TemperatureUnits, WindSpeedUnits

class ConfigUnitsRequestDTO(BaseModel):
    precipitation_sum: PrecipitationUnits
    temperature_2m_mean: TemperatureUnits
    wind_speed_10m_mean: WindSpeedUnits
    shortwave_radiation_sum: RadiationUnits
    et0_fao_evapotranspiration: ETZeroUnits
    