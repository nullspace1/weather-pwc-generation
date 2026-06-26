from typing import Protocol

import tkinter as tk
from tkinter import filedialog


class FolderPickerServiceProtocol(Protocol):
    def pick_folder(self) -> str | None:
        ...


class FolderPickerService(FolderPickerServiceProtocol):
    def pick_folder(self) -> str | None:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        path = filedialog.askdirectory()
        root.destroy()
        return path or None
