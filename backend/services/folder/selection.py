from typing import Protocol

from backend.dto.folder.output import SelectedFolderDTO
from backend.services.folder.picker import FolderPickerServiceProtocol


class FolderSelectionCancelledError(Exception):
    pass


class FolderSelectionServiceProtocol(Protocol):
    def select_folder(self) -> SelectedFolderDTO:
        ...

    def get_selected_folder(self) -> str | None:
        ...


class FolderSelectionService(FolderSelectionServiceProtocol):
    def __init__(self, folder_picker_service: FolderPickerServiceProtocol):
        self._folder_picker_service = folder_picker_service
        self._selected_path: str | None = None

    def select_folder(self) -> SelectedFolderDTO:
        path = self._folder_picker_service.pick_folder()
        if path is None:
            raise FolderSelectionCancelledError()
        self._selected_path = path
        return SelectedFolderDTO(path=path)

    def get_selected_folder(self) -> str | None:
        return self._selected_path
