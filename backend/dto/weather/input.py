from pydantic import BaseModel, field_validator


class WeatherDataRequestDTO(BaseModel):
    lat: float
    lon: float
    from_date: str
    to_date: str
    file_name: str

    @field_validator("file_name")
    @classmethod
    def file_name_must_not_contain_path_separators(cls, value: str) -> str:
        if "/" in value or "\\" in value:
            raise ValueError("file_name must not contain path separators")
        return value
