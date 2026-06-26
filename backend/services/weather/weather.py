from datetime import date
from typing import Protocol, TypedDict

import pandas as pd

from backend.dto.weather.input import WeatherDataRequestDTO
from backend.services.config.config import ConfigServiceProtocol
from backend.model.weather import WeatherResult
from backend.services.weather.external_api import WeatherAPIServiceProtocol
from backend.services.weather.units_converter import WeatherConverterServiceProtocol



class WeatherServiceProtocol(Protocol):
    def generate_weather_data(self, dto: WeatherDataRequestDTO) -> None:
        ...

class WeatherService(WeatherServiceProtocol):
    
    def __init__(self, 
                 config : ConfigServiceProtocol, 
                 converter_service: WeatherConverterServiceProtocol,
                 weather_api_service: WeatherAPIServiceProtocol):
        self.config = config
        self.converter_service = converter_service
        self.weather_api_service = weather_api_service
        
    def generate_weather_data(self, dto: WeatherDataRequestDTO) -> None:
        data : WeatherResult = self.weather_api_service.get_data(dto.lat, dto.lon, date.fromisoformat(dto.from_date), date.fromisoformat(dto.to_date))
        data : WeatherResult = self.converter_service.convert(data, self.config.units)
        df : pd.DataFrame = pd.DataFrame({
            "time": data.daily.time,
            "temperature_2m_mean": data.daily.temperature_2m_mean,
            "precipitation_sum": data.daily.precipitation_sum,
            "wind_speed_10m_mean": data.daily.wind_speed_10m_mean,
            "shortwave_radiation_sum": data.daily.shortwave_radiation_sum,
            "et0_fao_evapotranspiration": data.daily.et0_fao_evapotranspiration
        })
        df.to_csv(dto.output_path, index=False)
        
        
        