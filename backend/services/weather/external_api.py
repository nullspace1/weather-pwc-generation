from datetime import date
from typing import Protocol
import requests
from pydantic import BaseModel

from model.weather import WeatherResult
from services.weather.units_converter import WeatherConverterServiceProtocol


class WeatherAPIServiceProtocol(Protocol):
    
    def get_data(self, lat : float, lon : float, from_date : date, to_date : date) -> WeatherResult:
        raise NotImplementedError

    
class WeatherAPIService(WeatherAPIServiceProtocol):
    
    
    def get_data(self, lat : float, lon : float, from_date : date, to_date : date) -> WeatherResult:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&start_date={from_date}&end_date={to_date}&daily=temperature_2m_mean,precipitation_sum,wind_speed_10m_mean,shortwave_radiation_sum&timezone=auto"
        response = requests.get(url)
        return WeatherResult.model_validate(response.json())
    
    