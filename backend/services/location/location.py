

from typing import Protocol
import requests

from backend.dto.location.input import LocationRequestDTO
from backend.dto.location.output import LocationDTO, LocationResponseDTO
from model.location import Location, LocationResult


class LocationServiceProtocol(Protocol):
    
    def get_locations(self, query: LocationRequestDTO) -> LocationResponseDTO:
        ...
        
class LocationService(LocationServiceProtocol):
    
    def get_locations(self, query: LocationRequestDTO) -> LocationResponseDTO:
        url = f"https://nominatim.openstreetmap.org/search?q={query.location}&format=jsonv2"
        response = requests.get(url)
        results = LocationResult.model_validate(response.json())
        locations = [
            LocationDTO(
                name=result.name,
                country=result.country,
                latitude=result.latitude,
                longitude=result.longitude,
            )
            for result in results.results
        ]
        return LocationResponseDTO(locations=locations)
        
        
        