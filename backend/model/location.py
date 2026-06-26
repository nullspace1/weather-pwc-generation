from pydantic import BaseModel

class Location(BaseModel):
    display_name: str
    lat: float
    lon: float
    
    
