from unittest.mock import MagicMock, patch

import pandas as pd

from backend.services.export.export import ExportService


@patch.object(pd.DataFrame, "to_csv")
def test_export_writes_csv_without_index(mock_to_csv):
    service = ExportService()
    df = pd.DataFrame({"time": ["2024-01-01"], "temperature_2m_mean": [10.0]})
    output_path = "/tmp/weather.csv"

    service.export(df, output_path)

    mock_to_csv.assert_called_once_with(output_path, index=False)


def test_export_delegates_to_dataframe_to_csv():
    service = ExportService()
    df = MagicMock(spec=pd.DataFrame)
    output_path = "output/weather.csv"

    service.export(df, output_path)

    df.to_csv.assert_called_once_with(output_path, index=False)
