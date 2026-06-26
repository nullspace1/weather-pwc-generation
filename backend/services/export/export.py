from typing import Protocol

import pandas as pd


class ExportServiceProtocol(Protocol):
    def export(self, data: pd.DataFrame, file_path: str) -> None:
        ...


def _format_number(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return format(value, "g")


class ExportService(ExportServiceProtocol):
    def export(self, data: pd.DataFrame, file_path: str) -> None:
        lines = []
        for _, row in data.iterrows():
            date_value = pd.to_datetime(row["time"])
            line = ",".join(
                [
                    str(date_value.month),
                    str(date_value.day),
                    str(date_value.year % 100),
                    _format_number(row["precipitation_sum"]),
                    _format_number(row["et0_fao_evapotranspiration"]),
                    _format_number(row["temperature_2m_mean"]),
                    _format_number(row["wind_speed_10m_mean"]),
                    _format_number(row["shortwave_radiation_sum"]),
                    "",
                ]
            )
            lines.append(f"{line},")

        with open(file_path, "w", encoding="utf-8", newline="") as file:
            file.write("\n".join(lines) + "\n")
