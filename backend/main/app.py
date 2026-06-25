

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.dto.config.input import ConfigUnitsRequestDTO
from backend.dto.config.output import ConfigUnitsDTO
from backend.dto.location.input import LocationRequestDTO
from backend.dto.location.output import LocationResponseDTO
from backend.dto.weather.input import WeatherDataRequestDTO
from container import container
from fastapi import Request

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
    return container.location_service.get_locations(LocationRequestDTO.model_validate(request.query_params))
    
@app.post("/config/units")
async def set_units(request: Request):
    units = ConfigUnitsRequestDTO.model_validate(request.query_params)
    container.weather_config.set_units(units)
    
@app.get("/config/units")
async def get_units() -> ConfigUnitsDTO:
    return container.weather_config.get_units()

@app.get("/weather")
async def get_weather(request: Request):
    container.weather_service.generate_weather_data(WeatherDataRequestDTO.model_validate(request.query_params))

    

