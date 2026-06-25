from pydantic import BaseModel

class LocationDTO(BaseModel):
    name: str
    country: str
    latitude: float
    longitude: float
    
class LocationResponseDTO(BaseModel):
     locations: list[LocationDTO]