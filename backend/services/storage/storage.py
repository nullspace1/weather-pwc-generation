

from pathlib import Path
import sqlite3
from typing import Protocol

from backend.model.location import Location
from backend.model.report import CachedReport


class StorageServiceProtocol(Protocol):
    def store_location(self, location: Location) -> None:
        ...

    def get_all_locations(self) -> list[Location]:
        ...

    def delete_location(self, location_id: int) -> None:
        ...

    def upsert_cached_report(self, report: CachedReport) -> None:
        ...

    def get_all_cached_reports(self) -> list[CachedReport]:
        ...

    def get_cached_report(self, name: str) -> CachedReport | None:
        ...

    def delete_cached_report(self, name: str) -> None:
        ...

class StorageService(StorageServiceProtocol):
    
    def __init__(self, sqlite_db : str) -> None:
        self.sqlite_db = sqlite_db
        self._initialize_database()
        
    def _initialize_database(self) -> None:
        Path(self.sqlite_db).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.sqlite_db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS locations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cached_reports (
                    name TEXT PRIMARY KEY,
                    file_name TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    location_name TEXT,
                    latitude REAL,
                    longitude REAL,
                    from_date TEXT,
                    to_date TEXT
                )
            """)
            self._ensure_cached_report_columns(cursor)
            conn.commit()

    def _ensure_cached_report_columns(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute("PRAGMA table_info(cached_reports)")
        columns = {row[1] for row in cursor.fetchall()}
        migrations = [
            ("location_name", "TEXT"),
            ("latitude", "REAL"),
            ("longitude", "REAL"),
            ("from_date", "TEXT"),
            ("to_date", "TEXT"),
        ]
        for column_name, column_type in migrations:
            if column_name not in columns:
                cursor.execute(
                    f"ALTER TABLE cached_reports ADD COLUMN {column_name} {column_type}"
                )
        
    
    def store_location(self, location: Location) -> None:
        
        with sqlite3.connect(self.sqlite_db) as conn:
            
            cursor = conn.cursor()
            cursor.execute("INSERT INTO locations (name, latitude, longitude) VALUES (?, ?, ?)", (location.name, location.latitude, location.longitude))
            conn.commit()
    
    def get_all_locations(self) -> list[Location]:
        with sqlite3.connect(self.sqlite_db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, latitude, longitude FROM locations")
            rows = cursor.fetchall()
            return [
                Location(id=row[0], name=row[1], latitude=row[2], longitude=row[3])
                for row in rows
            ]

    def delete_location(self, location_id: int) -> None:
        with sqlite3.connect(self.sqlite_db) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM locations WHERE id = ?", (location_id,))
            conn.commit()

    def upsert_cached_report(self, report: CachedReport) -> None:
        with sqlite3.connect(self.sqlite_db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO cached_reports (
                    name, file_name, created_at,
                    location_name, latitude, longitude, from_date, to_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    file_name = excluded.file_name,
                    created_at = excluded.created_at,
                    location_name = excluded.location_name,
                    latitude = excluded.latitude,
                    longitude = excluded.longitude,
                    from_date = excluded.from_date,
                    to_date = excluded.to_date
                """,
                (
                    report.name,
                    report.file_name,
                    report.created_at,
                    report.location_name,
                    report.latitude,
                    report.longitude,
                    report.from_date,
                    report.to_date,
                ),
            )
            conn.commit()

    def _row_to_cached_report(self, row: tuple) -> CachedReport:
        return CachedReport(
            name=row[0],
            file_name=row[1],
            created_at=row[2],
            location_name=row[3],
            latitude=row[4],
            longitude=row[5],
            from_date=row[6],
            to_date=row[7],
        )

    def get_all_cached_reports(self) -> list[CachedReport]:
        with sqlite3.connect(self.sqlite_db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT name, file_name, created_at,
                       location_name, latitude, longitude, from_date, to_date
                FROM cached_reports ORDER BY created_at DESC
                """
            )
            rows = cursor.fetchall()
            return [self._row_to_cached_report(row) for row in rows]

    def get_cached_report(self, name: str) -> CachedReport | None:
        with sqlite3.connect(self.sqlite_db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT name, file_name, created_at,
                       location_name, latitude, longitude, from_date, to_date
                FROM cached_reports WHERE name = ?
                """,
                (name,),
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return self._row_to_cached_report(row)

    def delete_cached_report(self, name: str) -> None:
        with sqlite3.connect(self.sqlite_db) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cached_reports WHERE name = ?", (name,))
            conn.commit()
        
        
