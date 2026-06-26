from pydantic import BaseModel


class SelectedFolderDTO(BaseModel):
    path: str
