from pydantic import BaseModel, field_validator


class WeatherDataRequestDTO(BaseModel):
    lat: float
    lon: float
    from_date: str
    to_date: str
    report_name: str
    save_to_cache: bool = False
    location_name: str | None = None

    @field_validator("report_name")
    @classmethod
    def report_name_must_not_contain_path_separators(cls, value: str) -> str:
        if "/" in value or "\\" in value:
            raise ValueError("report_name must not contain path separators")
        return value
