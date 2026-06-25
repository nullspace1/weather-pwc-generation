

from functools import cached_property


class Container():
    
    @cached_property
    def location_service(self):
        from services.location.location import LocationService
        return LocationService()
    
    @cached_property
    def export_service(self):
        from services.export.export import ExportService
        return ExportService()
    
    @cached_property
    def weather_converter_service(self):
        from services.weather.units_converter import WeatherConverterService
        return WeatherConverterService()
    
    @cached_property
    def weather_api_service(self):
        from services.weather.external_api import WeatherAPIService
        return WeatherAPIService()
    
    @cached_property
    def weather_config(self):
        from services.config.config import ConfigService
        import os
        return ConfigService()
    
    @cached_property
    def weather_service(self):
        from services.weather.weather import WeatherService
        return WeatherService(
            config=self.weather_config,
            converter_service=self.weather_converter_service,
            weather_api_service=self.weather_api_service
        )
        
        
container = Container()