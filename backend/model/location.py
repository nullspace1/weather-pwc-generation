from pydantic import BaseModel

class APILocation(BaseModel):
    display_name: str
    lat: float
    lon: float
    
class Location(BaseModel):
    id: int | None = None
    name: str
    latitude: float
    longitude: float
    
    
