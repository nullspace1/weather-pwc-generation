from unittest.mock import MagicMock, patch

import pytest

from backend.services.folder.picker import FolderPickerService


@patch("backend.services.folder.picker.filedialog.askdirectory", return_value="/tmp/picked")
@patch("backend.services.folder.picker.tk.Tk")
def test_pick_folder_returns_selected_path(mock_tk, mock_askdirectory):
    mock_root = MagicMock()
    mock_tk.return_value = mock_root

    service = FolderPickerService()
    path = service.pick_folder()

    assert path == "/tmp/picked"
    mock_root.withdraw.assert_called_once()
    mock_root.attributes.assert_called_once_with("-topmost", True)
    mock_root.destroy.assert_called_once()


@patch("backend.services.folder.picker.filedialog.askdirectory", return_value="")
@patch("backend.services.folder.picker.tk.Tk")
def test_pick_folder_returns_none_when_cancelled(mock_tk, mock_askdirectory):
    mock_root = MagicMock()
    mock_tk.return_value = mock_root

    service = FolderPickerService()
    path = service.pick_folder()

    assert path is None
