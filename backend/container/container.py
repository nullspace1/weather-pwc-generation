



from functools import cached_property

from pathlib import Path





class Container():

    

    @cached_property

    def storage_service(self):

        from backend.services.storage.storage import StorageService

        return StorageService(sqlite_db=str(Path("./appdata/locations.db").expanduser()))

    

    @cached_property

    def location_service(self):

        from backend.services.location.location import LocationService

        return LocationService(storage_service=self.storage_service)

    

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

    def folder_picker_service(self):

        from backend.services.folder.picker import FolderPickerService

        return FolderPickerService()



    @cached_property

    def folder_selection_service(self):

        from backend.services.folder.selection import FolderSelectionService

        return FolderSelectionService(folder_picker_service=self.folder_picker_service)



    @cached_property

    def report_cache_service(self):

        from backend.services.report.cache import ReportCacheService

        return ReportCacheService(

            storage_service=self.storage_service,

            cache_dir=str(Path("./appdata/reports").expanduser()),

            folder_picker_service=self.folder_picker_service,

        )

    

    @cached_property

    def weather_service(self):

        from backend.services.weather.weather import WeatherService

        return WeatherService(

            converter_service=self.weather_converter_service,

            weather_api_service=self.weather_api_service,

            folder_selection_service=self.folder_selection_service,

            export_service=self.export_service,

            report_cache_service=self.report_cache_service,

        )

        

        

container = Container()

