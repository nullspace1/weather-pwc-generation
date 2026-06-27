from pydantic import BaseModel


class ReportDTO(BaseModel):
    name: str
    file_name: str
    created_at: str
    location_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    from_date: str | None = None
    to_date: str | None = None


class ReportListResponseDTO(BaseModel):
    reports: list[ReportDTO]
