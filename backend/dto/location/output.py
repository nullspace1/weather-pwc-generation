from pydantic import BaseModel

class LocationDTO(BaseModel):
    id: int | None = None
    name: str
    latitude: float
    longitude: float
    
class LocationResponseDTO(BaseModel):
     locations: list[LocationDTO]
     results_count: int = 0