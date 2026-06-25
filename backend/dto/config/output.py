from pydantic import BaseModel

class ConfigUnitsDTO(BaseModel):
    precipitation_sum: str
    et0_fao_evapotranspiration: str
    temperature_2m_mean: str
    wind_speed_10m_mean: str
    shortwave_radiation_sum: str