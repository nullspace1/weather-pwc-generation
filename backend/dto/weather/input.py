from pydantic import BaseModel


class WeatherDataRequestDTO(BaseModel):
    lat: float
    lon: float
    from_date: str
    to_date: str
    output_path: str
    