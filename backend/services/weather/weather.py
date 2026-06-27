from datetime import date
from pathlib import Path
from typing import Protocol

import pandas as pd

from backend.dto.weather.input import WeatherDataRequestDTO
from backend.model.weather import WeatherResult
from backend.services.export.export import ExportServiceProtocol
from backend.services.folder.selection import FolderSelectionServiceProtocol
from backend.services.report.cache import ReportCacheServiceProtocol
from backend.services.weather.external_api import WeatherAPIServiceProtocol
from backend.services.weather.report_name import to_file_name
from backend.services.weather.units_converter import WeatherConverterServiceProtocol


class NoOutputFolderSelectedError(Exception):
    pass


class WeatherServiceProtocol(Protocol):
    def generate_weather_data(self, dto: WeatherDataRequestDTO) -> str:
        ...


class WeatherService(WeatherServiceProtocol):
    def __init__(
        self,
        converter_service: WeatherConverterServiceProtocol,
        weather_api_service: WeatherAPIServiceProtocol,
        folder_selection_service: FolderSelectionServiceProtocol,
        export_service: ExportServiceProtocol,
        report_cache_service: ReportCacheServiceProtocol,
    ):
        self.converter_service = converter_service
        self.weather_api_service = weather_api_service
        self.folder_selection_service = folder_selection_service
        self.export_service = export_service
        self.report_cache_service = report_cache_service

    def generate_weather_data(self, dto: WeatherDataRequestDTO) -> str:
        folder = self.folder_selection_service.get_selected_folder()
        if folder is None:
            raise NoOutputFolderSelectedError()

        data: WeatherResult = self.weather_api_service.get_data(
            dto.lat, dto.lon, date.fromisoformat(dto.from_date), date.fromisoformat(dto.to_date)
        )
        data = self.converter_service.convert(data)
        df = pd.DataFrame(
            {
                "time": data.daily.time,
                "temperature_2m_mean": data.daily.temperature_2m_mean,
                "precipitation_sum": data.daily.precipitation_sum,
                "wind_speed_10m_mean": data.daily.wind_speed_10m_mean,
                "shortwave_radiation_sum": data.daily.shortwave_radiation_sum,
                "et0_fao_evapotranspiration": data.daily.et0_fao_evapotranspiration,
            }
        )
        output_path = Path(folder) / to_file_name(dto.report_name)
        self.export_service.export(df, str(output_path))
        if dto.save_to_cache:
            location_name = dto.location_name or f"{dto.lat}, {dto.lon}"
            self.report_cache_service.save_report(
                dto.report_name,
                str(output_path),
                location_name=location_name,
                latitude=dto.lat,
                longitude=dto.lon,
                from_date=dto.from_date,
                to_date=dto.to_date,
            )
        return str(output_path)
