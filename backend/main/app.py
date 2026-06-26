

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from backend.container.container import container
from backend.dto.config.input import ConfigUnitsRequestDTO
from backend.dto.config.output import ConfigUnitsDTO
from backend.dto.folder.output import SelectedFolderDTO
from backend.dto.location.input import LocationRequestDTO
from backend.dto.location.output import LocationResponseDTO
from backend.dto.weather.input import WeatherDataRequestDTO
from backend.dto.weather.output import WeatherDataResponseDTO
from backend.services.folder.selection import FolderSelectionCancelledError
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
    return container.location_service.get_locations(LocationRequestDTO.model_validate(dict(request.query_params)))
    
@app.post("/config/units")
async def set_units(request: Request):
    units = ConfigUnitsRequestDTO.model_validate(dict(request.query_params))
    container.weather_config.set_units(units)
    
@app.get("/config/units")
async def get_units() -> ConfigUnitsDTO:
    return container.weather_config.get_units()

@app.post("/folders/select")
async def select_folder() -> SelectedFolderDTO:
    try:
        return container.folder_selection_service.select_folder()
    except FolderSelectionCancelledError:
        raise HTTPException(status_code=400, detail="Folder selection cancelled")

@app.get("/folders/selected")
async def get_selected_folder() -> SelectedFolderDTO:
    path = container.folder_selection_service.get_selected_folder()
    if path is None:
        raise HTTPException(status_code=404, detail="No output folder selected")
    return SelectedFolderDTO(path=path)

@app.get("/weather")
async def get_weather(request: Request) -> WeatherDataResponseDTO:
    try:
        file_path = container.weather_service.generate_weather_data(
            WeatherDataRequestDTO.model_validate(dict(request.query_params))
        )
    except NoOutputFolderSelectedError:
        raise HTTPException(status_code=400, detail="No output folder selected")
    return WeatherDataResponseDTO(file_path=file_path)
