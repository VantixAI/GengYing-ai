import sqlite3
from contextlib import closing
from datetime import datetime, timezone

from .config import settings


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(settings.database_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    with closing(connect()) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS memes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL UNIQUE,
                uploaded_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS clicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meme_id INTEGER NOT NULL,
                query TEXT NOT NULL,
                clicked_at TEXT NOT NULL,
                FOREIGN KEY (meme_id) REFERENCES memes(id)
            );
            """
        )
        connection.commit()


def register_meme(filename: str) -> int:
    now = datetime.now(timezone.utc).isoformat()
    with closing(connect()) as connection:
        connection.execute(
            "INSERT OR IGNORE INTO memes(filename, uploaded_at) VALUES (?, ?)",
            (filename, now),
        )
        row = connection.execute("SELECT id FROM memes WHERE filename = ?", (filename,)).fetchone()
        connection.commit()
    return int(row["id"])


def record_click(meme_id: int, query: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    with closing(connect()) as connection:
        connection.execute(
            "INSERT INTO clicks(meme_id, query, clicked_at) VALUES (?, ?, ?)",
            (meme_id, query, now),
        )
        connection.commit()

