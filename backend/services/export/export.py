from typing import Protocol

import pandas as pd


class ExportServiceProtocol(Protocol):
    
    def export(self, data: pd.DataFrame, file_path: str) -> None:
        ...
        
class ExportService(ExportServiceProtocol):
    
    def export(self, data: pd.DataFrame, file_path: str) -> None:
        data.to_csv(file_path, index=False)