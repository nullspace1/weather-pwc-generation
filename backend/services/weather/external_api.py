from datetime import date
from typing import Protocol
import requests
from pydantic import BaseModel

from backend.model.weather import WeatherResult


class WeatherAPIServiceProtocol(Protocol):
    
    def get_data(self, lat : float, lon : float, from_date : date, to_date : date) -> WeatherResult:
        raise NotImplementedError

    
class WeatherAPIService(WeatherAPIServiceProtocol):
    
    url = "https://archive-api.open-meteo.com/v1/archive"
    
    
    def get_data(self, lat : float, lon : float, from_date : date, to_date : date) -> WeatherResult:
        response = requests.get(
            url=self.url,
            params={
                "latitude": lat,
                "longitude": lon,
                "start_date": from_date.isoformat(),
                "end_date": to_date.isoformat(),
                "daily": "temperature_2m_mean,precipitation_sum,wind_speed_10m_mean,shortwave_radiation_sum,et0_fao_evapotranspiration",
                "timezone": "auto"
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get weather data when calling {self.url} with params: {response.request.url}, status code: {response.status_code}")
        
        val = response.json()
        
        print(f"Weather API response: {val}")
        
        return WeatherResult.model_validate(val)
    
    