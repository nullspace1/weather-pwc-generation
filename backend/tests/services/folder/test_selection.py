from unittest.mock import MagicMock

import pytest

from backend.services.folder.selection import (
    FolderSelectionCancelledError,
    FolderSelectionService,
)


def test_select_folder_stores_and_returns_path():
    picker = MagicMock()
    picker.pick_folder.return_value = "/tmp/output"
    service = FolderSelectionService(folder_picker_service=picker)

    result = service.select_folder()

    assert result.path == "/tmp/output"
    assert service.get_selected_folder() == "/tmp/output"
    picker.pick_folder.assert_called_once()


def test_select_folder_raises_when_cancelled():
    picker = MagicMock()
    picker.pick_folder.return_value = None
    service = FolderSelectionService(folder_picker_service=picker)

    with pytest.raises(FolderSelectionCancelledError):
        service.select_folder()

    assert service.get_selected_folder() is None


def test_get_selected_folder_returns_none_initially():
    picker = MagicMock()
    service = FolderSelectionService(folder_picker_service=picker)

    assert service.get_selected_folder() is None
