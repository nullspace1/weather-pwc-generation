from backend.dto.config.input import ConfigUnitsRequestDTO
from backend.services.config.config import ConfigService


def test_default_units_on_init():
    service = ConfigService()

    assert service.units.precipitation_sum == "mm/day"
    assert service.units.et0_fao_evapotranspiration == "mm/day"
    assert service.units.temperature_2m_mean == "C"
    assert service.units.wind_speed_10m_mean == "km/h"
    assert service.units.shortwave_radiation_sum == "MJ/m^2/day"


def test_get_units_returns_current_config():
    service = ConfigService()

    units = service.get_units()

    assert units.precipitation_sum == "mm/day"
    assert units.et0_fao_evapotranspiration == "mm/day"
    assert units.temperature_2m_mean == "C"
    assert units.wind_speed_10m_mean == "km/h"
    assert units.shortwave_radiation_sum == "MJ/m^2/day"


def test_set_units_updates_stored_units():
    service = ConfigService()
    request = ConfigUnitsRequestDTO(
        precipitation_sum="cm/day",
        et0_fao_evapotranspiration="in/day",
        temperature_2m_mean="F",
        wind_speed_10m_mean="m/s",
        shortwave_radiation_sum="W/m²",
    )

    service.set_units(request)

    assert service.units.precipitation_sum == "cm/day"
    assert service.units.et0_fao_evapotranspiration == "in/day"
    assert service.units.temperature_2m_mean == "F"
    assert service.units.wind_speed_10m_mean == "m/s"
    assert service.units.shortwave_radiation_sum == "W/m²"


def test_get_units_reflects_set_units():
    service = ConfigService()
    service.set_units(
        ConfigUnitsRequestDTO(
            precipitation_sum="in/day",
            et0_fao_evapotranspiration="cm/day",
            temperature_2m_mean="K",
            wind_speed_10m_mean="mph",
            shortwave_radiation_sum="kW/m²",
        )
    )

    units = service.get_units()

    assert units.precipitation_sum == "in/day"
    assert units.et0_fao_evapotranspiration == "cm/day"
    assert units.temperature_2m_mean == "K"
    assert units.wind_speed_10m_mean == "mph"
    assert units.shortwave_radiation_sum == "kW/m²"
