from unittest.mock import MagicMock, Mock, patch

from backend.dto.location.input import LocationRequestDTO, LocationSaveRequestDTO
from backend.model.location import Location
from backend.services.location.location import LocationService


@patch("backend.services.location.location.requests.get")
def test_get_locations_returns_mapped_dtos(mock_get):
    mock_get.return_value = MagicMock(
        status_code=200,
        json=MagicMock(
            return_value=[
                {
                    "display_name": "Berlin, Germany",
                    "lat": 52.52,
                    "lon": 13.405,
                },
                {
                    "display_name": "Munich, Germany",
                    "lat": 48.137,
                    "lon": 11.575,
                },
            ]
        ),
    )
    service = LocationService(Mock())

    response = service.get_api_locations(LocationRequestDTO(name="Berlin"))

    assert len(response.locations) == 2
    assert response.locations[0].name == "Berlin, Germany"
    assert response.locations[0].latitude == 52.52
    assert response.locations[1].name == "Munich, Germany"
    assert response.results_count == 2


@patch("backend.services.location.location.requests.get")
def test_get_locations_builds_nominatim_request(mock_get):
    mock_get.return_value = MagicMock(status_code=200, json=MagicMock(return_value=[]))
    service = LocationService(Mock())

    service.get_api_locations(LocationRequestDTO(name="Paris"))

    mock_get.assert_called_once_with(
        url="https://nominatim.openstreetmap.org/search",
        params={"q": "Paris", "format": "json", "limit": 5},
        headers={"User-Agent": "LocationService/1.0"},
    )


@patch("backend.services.location.location.requests.get")
def test_get_locations_handles_empty_results(mock_get):
    mock_get.return_value = MagicMock(status_code=200, json=MagicMock(return_value=[]))
    service = LocationService(Mock())

    response = service.get_api_locations(LocationRequestDTO(name="Nowhere"))

    assert response.locations == []
    assert response.results_count == 0


def test_get_stored_locations_returns_mapped_dtos():
    storage_service = Mock()
    storage_service.get_all_locations.return_value = [
        Location(id=1, name="Berlin", latitude=52.52, longitude=13.405),
    ]
    service = LocationService(storage_service)

    response = service.get_stored_locations()

    assert len(response.locations) == 1
    assert response.locations[0].id == 1
    assert response.locations[0].name == "Berlin"
    assert response.locations[0].latitude == 52.52
    assert response.results_count == 1


def test_store_location_delegates_to_storage():
    storage_service = Mock()
    service = LocationService(storage_service)
    dto = LocationSaveRequestDTO(name="Berlin", latitude=52.52, longitude=13.405)

    service.store_location(dto)

    storage_service.store_location.assert_called_once_with(
        Location(name="Berlin", latitude=52.52, longitude=13.405)
    )


def test_delete_location_delegates_to_storage():
    storage_service = Mock()
    service = LocationService(storage_service)

    service.delete_location(3)

    storage_service.delete_location.assert_called_once_with(3)
