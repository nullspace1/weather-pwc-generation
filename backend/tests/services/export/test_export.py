import pandas as pd

from backend.services.export.export import ExportService


def test_export_writes_wea_format_without_headers(tmp_path):
    service = ExportService()
    df = pd.DataFrame(
        {
            "time": ["2011-01-01"],
            "precipitation_sum": [0.0],
            "et0_fao_evapotranspiration": [6.5],
            "temperature_2m_mean": [25.9],
            "wind_speed_10m_mean": [432.4],
            "shortwave_radiation_sum": [880.3],
        }
    )
    output_path = tmp_path / "weather.wea"

    service.export(df, str(output_path))

    content = output_path.read_text(encoding="utf-8")
    assert content == "1,1,11,0,6.5,25.9,432.4,880.3,,\n"
    assert "month" not in content
