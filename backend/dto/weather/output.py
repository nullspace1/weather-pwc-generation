from pydantic import BaseModel


class WeatherDataResponseDTO(BaseModel):
    file_path: str
