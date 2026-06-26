from pydantic import BaseModel

class LocationDTO(BaseModel):
    name: str
    latitude: float
    longitude: float
    
class LocationResponseDTO(BaseModel):
     locations: list[LocationDTO]