



from fastapi import FastAPI, HTTPException, Request

from fastapi.middleware.cors import CORSMiddleware



from backend.container.container import container

from backend.dto.folder.output import SelectedFolderDTO

from backend.dto.location.input import LocationRequestDTO, LocationSaveRequestDTO

from backend.dto.location.output import LocationResponseDTO

from backend.dto.report.output import ReportListResponseDTO

from backend.dto.weather.input import WeatherDataRequestDTO

from backend.dto.weather.output import WeatherDataResponseDTO

from backend.services.folder.selection import FolderSelectionCancelledError

from backend.services.report.cache import ReportNotFoundError

from backend.services.weather.weather import NoOutputFolderSelectedError



app = FastAPI()



app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)





@app.get("/locations")

async def root(request: Request) -> LocationResponseDTO:

    return container.location_service.get_api_locations(LocationRequestDTO.model_validate(dict(request.query_params)))



@app.post("/folders/select")

async def select_folder() -> SelectedFolderDTO:

    try:

        return container.folder_selection_service.select_folder()

    except FolderSelectionCancelledError:

        raise HTTPException(status_code=400, detail="Folder selection cancelled")



@app.get("/folders/selected")

async def get_selected_folder() -> SelectedFolderDTO:

    return SelectedFolderDTO(path=container.folder_selection_service.get_selected_folder())



@app.get("/weather")

async def get_weather(request: Request) -> WeatherDataResponseDTO:

    try:

        file_path = container.weather_service.generate_weather_data(

            WeatherDataRequestDTO.model_validate(dict(request.query_params))

        )

    except NoOutputFolderSelectedError:

        raise HTTPException(status_code=400, detail="No output folder selected")

    return WeatherDataResponseDTO(file_path=file_path)



@app.get("/weather/locations")

async def get_stored_locations() -> LocationResponseDTO:

    return container.location_service.get_stored_locations()



@app.post("/weather/locations")

async def store_location(location: LocationSaveRequestDTO) -> None:

    container.location_service.store_location(location)



@app.delete("/weather/locations/{location_id}")

async def delete_stored_location(location_id: int) -> None:

    container.location_service.delete_location(location_id)



@app.get("/weather/reports")

async def get_cached_reports() -> ReportListResponseDTO:

    return ReportListResponseDTO(reports=container.report_cache_service.list_reports())



@app.delete("/weather/reports/{report_name}")

async def delete_cached_report(report_name: str) -> None:

    container.report_cache_service.delete_report(report_name)



@app.post("/weather/reports/{report_name}/export")

async def export_cached_report(report_name: str) -> WeatherDataResponseDTO:

    try:

        file_path = container.report_cache_service.export_report(report_name)

    except ReportNotFoundError:

        raise HTTPException(status_code=404, detail="Report not found")

    except FolderSelectionCancelledError:

        raise HTTPException(status_code=400, detail="Folder selection cancelled")

    return WeatherDataResponseDTO(file_path=file_path)

