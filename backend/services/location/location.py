

from typing import Protocol
import requests

from backend.dto.location.input import LocationRequestDTO, LocationSaveRequestDTO
from backend.dto.location.output import LocationDTO, LocationResponseDTO
from backend.model.location import APILocation, Location
from backend.services.storage.storage import StorageServiceProtocol


class LocationServiceProtocol(Protocol):
    
    def get_api_locations(self, query: LocationRequestDTO) -> LocationResponseDTO:
        ...
        
    def get_stored_locations(self) -> LocationResponseDTO:
        ...
        
    def store_location(self, location: LocationSaveRequestDTO) -> None:
        ...

    def delete_location(self, location_id: int) -> None:
        ...
        
class LocationService(LocationServiceProtocol):
    
    url : str = f"https://nominatim.openstreetmap.org/search"
    
    def __init__(self, storage_service: StorageServiceProtocol):
        self.storage_service = storage_service
    
    def get_api_locations(self, query: LocationRequestDTO) -> LocationResponseDTO:
        
        response = requests.get(
           url= self.url,
           params= {
                "q": query.name,
                "format": "json",
                "limit": 5
           },
           headers={
               "User-Agent": "LocationService/1.0"
           }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to get locations: {response.status_code}")
        
        results = [APILocation.model_validate(result) for result in response.json()]
        locations = [LocationDTO(
            name=result.display_name, latitude=result.lat, longitude=result.lon) for result in results]
        return LocationResponseDTO(locations=locations, results_count=len(locations))
    
    def get_stored_locations(self) -> LocationResponseDTO:
        stored_locations = self.storage_service.get_all_locations()
        locations = [
            LocationDTO(
                id=loc.id, name=loc.name, latitude=loc.latitude, longitude=loc.longitude
            )
            for loc in stored_locations
        ]
        return LocationResponseDTO(locations=locations, results_count=len(locations))
        
    def store_location(self, location: LocationSaveRequestDTO) -> None:
        stored_location = Location(name=location.name, latitude=location.latitude, longitude=location.longitude)
        self.storage_service.store_location(stored_location)

    def delete_location(self, location_id: int) -> None:
        self.storage_service.delete_location(location_id)
        