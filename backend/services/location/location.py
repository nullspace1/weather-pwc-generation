

from typing import Protocol
import requests

from backend.dto.location.input import LocationRequestDTO
from backend.dto.location.output import LocationDTO, LocationResponseDTO
from backend.model.location import Location


class LocationServiceProtocol(Protocol):
    
    def get_locations(self, query: LocationRequestDTO) -> LocationResponseDTO:
        ...
        
class LocationService(LocationServiceProtocol):
    
    url : str = f"https://nominatim.openstreetmap.org/search"
    
    def get_locations(self, query: LocationRequestDTO) -> LocationResponseDTO:
        
        response = requests.get(
           url= self.url,
           params= {
                "q": query.location,
                "format": "json",
                "limit": 5
           },
           headers={
               "User-Agent": "LocationService/1.0"
           }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get locations: {response.status_code}")
        
        results = [Location.model_validate(result) for result in response.json()]
        locations = [LocationDTO(
            name=result.display_name, latitude=result.lat, longitude=result.lon) for result in results]
        return LocationResponseDTO(locations=locations)
        
        
        