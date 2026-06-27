from backend.model.location import Location
from backend.services.storage.storage import StorageService


def test_store_location_persists_and_get_all_returns_in_order(tmp_path):
    db_path = tmp_path / "locations.db"
    service = StorageService(sqlite_db=str(db_path))
    berlin = Location(name="Berlin", latitude=52.52, longitude=13.405)
    munich = Location(name="Munich", latitude=48.137, longitude=11.575)

    service.store_location(berlin)
    service.store_location(munich)

    locations = service.get_all_locations()

    assert len(locations) == 2
    assert locations[0].id == 1
    assert locations[0].name == "Berlin"
    assert locations[0].latitude == 52.52
    assert locations[1].id == 2
    assert locations[1].name == "Munich"
    assert locations[1].longitude == 11.575


def test_delete_location_removes_row(tmp_path):
    db_path = tmp_path / "locations.db"
    service = StorageService(sqlite_db=str(db_path))
    berlin = Location(name="Berlin", latitude=52.52, longitude=13.405)
    service.store_location(berlin)
    location_id = service.get_all_locations()[0].id

    service.delete_location(location_id)

    assert service.get_all_locations() == []


def test_get_all_locations_returns_empty_list_when_no_rows(tmp_path):
    db_path = tmp_path / "locations.db"
    service = StorageService(sqlite_db=str(db_path))

    assert service.get_all_locations() == []
