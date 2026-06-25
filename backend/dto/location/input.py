

from pydantic import BaseModel


class LocationRequestDTO(BaseModel):
    location: str