from typing import Any, Protocol
from backend.dto.config.input import ConfigUnitsRequestDTO
from backend.dto.config.output import ConfigUnitsDTO
from backend.model.weather import ConfigUnits


class ConfigServiceProtocol(Protocol):
    
    @property
    def units(self) -> ConfigUnits:
        ...

    def get_units(self) -> ConfigUnitsDTO:
        ...
        
    def set_units(self, units: ConfigUnitsRequestDTO) -> None:
        ...
        
        
class ConfigService(ConfigServiceProtocol):
    
    _units : ConfigUnits
    
    def __init__(self):
        
        self._units = ConfigUnits(
            precipitation_sum="mm/day",
            et0_fao_evapotranspiration="mm/day",
            temperature_2m_mean="C",
            wind_speed_10m_mean="cm/s",
            shortwave_radiation_sum="La/day"
        ) 
        
    @property
    def units(self) -> ConfigUnits:
        return self._units
        
    def set_units(self, units: ConfigUnitsRequestDTO) -> None:
        self._units = ConfigUnits(
            precipitation_sum=units.precipitation_sum,
            et0_fao_evapotranspiration=units.et0_fao_evapotranspiration,
            temperature_2m_mean=units.temperature_2m_mean,
            wind_speed_10m_mean=units.wind_speed_10m_mean,
            shortwave_radiation_sum=units.shortwave_radiation_sum
        )
        
    def get_units(self) -> ConfigUnitsDTO:        
        return ConfigUnitsDTO(
            precipitation_sum=self.units.precipitation_sum,
            et0_fao_evapotranspiration=self.units.et0_fao_evapotranspiration,
            temperature_2m_mean=self.units.temperature_2m_mean,
            wind_speed_10m_mean=self.units.wind_speed_10m_mean,
            shortwave_radiation_sum=self.units.shortwave_radiation_sum
        )