

from functools import cached_property


class Container():
    
    @cached_property
    def location_service(self):
        from backend.services.location.location import LocationService
        return LocationService()
    
    @cached_property
    def export_service(self):
        from backend.services.export.export import ExportService
        return ExportService()
    
    @cached_property
    def weather_converter_service(self):
        from backend.services.weather.units_converter import WeatherConverterService
        return WeatherConverterService()
    
    @cached_property
    def weather_api_service(self):
        from backend.services.weather.external_api import WeatherAPIService
        return WeatherAPIService()
    
    @cached_property
    def weather_config(self):
        from backend.services.config.config import ConfigService
        return ConfigService()

    @cached_property
    def folder_picker_service(self):
        from backend.services.folder.picker import FolderPickerService
        return FolderPickerService()

    @cached_property
    def folder_selection_service(self):
        from backend.services.folder.selection import FolderSelectionService
        return FolderSelectionService(folder_picker_service=self.folder_picker_service)
    
    @cached_property
    def weather_service(self):
        from backend.services.weather.weather import WeatherService
        return WeatherService(
            config=self.weather_config,
            converter_service=self.weather_converter_service,
            weather_api_service=self.weather_api_service,
            folder_selection_service=self.folder_selection_service,
            export_service=self.export_service,
        )
        
        
container = Container()