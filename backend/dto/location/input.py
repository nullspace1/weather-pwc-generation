

from pydantic import BaseModel


class LocationRequestDTO(BaseModel):
    name: str
    
class LocationSaveRequestDTO(BaseModel):
    name: str
    latitude: float
    longitude: float