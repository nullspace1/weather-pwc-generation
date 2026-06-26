from unittest.mock import MagicMock, patch

from backend.dto.location.input import LocationRequestDTO
from backend.services.location.location import LocationService


@patch("backend.services.location.location.requests.get")
def test_get_locations_returns_mapped_dtos(mock_get):
    mock_get.return_value = MagicMock(
        json=MagicMock(
            return_value={
                "results": [
                    {
                        "name": "Berlin",
                        "country": "Germany",
                        "latitude": 52.52,
                        "longitude": 13.405,
                    },
                    {
                        "name": "Munich",
                        "country": "Germany",
                        "latitude": 48.137,
                        "longitude": 11.575,
                    },
                ]
            }
        )
    )
    service = LocationService()

    response = service.get_locations(LocationRequestDTO(location="Berlin"))

    assert len(response.locations) == 2
    assert response.locations[0].name == "Berlin"
    assert response.locations[0].country == "Germany"
    assert response.locations[1].name == "Munich"
    assert response.locations[1].country == "Germany"


@patch("backend.services.location.location.requests.get")
def test_get_locations_builds_nominatim_url(mock_get):
    mock_get.return_value = MagicMock(json=MagicMock(return_value={"results": []}))
    service = LocationService()

    service.get_locations(LocationRequestDTO(location="Paris"))

    mock_get.assert_called_once_with(
        "https://nominatim.openstreetmap.org/search?q=Paris&format=jsonv2"
    )


@patch("backend.services.location.location.requests.get")
def test_get_locations_handles_empty_results(mock_get):
    mock_get.return_value = MagicMock(json=MagicMock(return_value={"results": []}))
    service = LocationService()

    response = service.get_locations(LocationRequestDTO(location="Nowhere"))

    assert response.locations == []
