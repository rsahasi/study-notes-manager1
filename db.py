import sqlite3
from datetime import datetime
from typing import List

DB_PATH = "notes.db"


def init_db(db_path: str = DB_PATH) -> None:
    """Initialize the database and create the notes table if it doesn't exist."""
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """)
        conn.commit()


def add_note_to_db(text: str, db_path: str = DB_PATH) -> None:
    """Add a note to the database."""
    init_db(db_path)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT INTO notes (text, created_at) VALUES (?, ?)",
            (text, timestamp)
        )
        conn.commit()


def get_all_notes(db_path: str = DB_PATH) -> List[str]:
    """Get all notes from the database, returning just the text."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("SELECT text FROM notes ORDER BY id")
        notes = [row[0] for row in cursor.fetchall()]
    return notes


def delete_note_by_id(note_id: int, db_path: str = DB_PATH) -> bool:
    """Delete a note by its ID. Returns True if successful."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        return cursor.rowcount > 0


def get_note_id_by_index(index: int, db_path: str = DB_PATH) -> int | None:
    """Get the database ID of a note by its display index (1-based)."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("SELECT id FROM notes ORDER BY id LIMIT 1 OFFSET ?", (index - 1,))
        row = cursor.fetchone()
        return row[0] if row else None


def get_all_notes_with_ids(db_path: str = DB_PATH) -> List[tuple[int, str]]:
    """Get all notes with their IDs. Returns list of (id, text) tuples."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("SELECT id, text, created_at FROM notes ORDER BY id")
        return cursor.fetchall()

def get_note_by_id(note_id: int, db_path: str = DB_PATH) -> tuple[int, str, str] | None:
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            "SELECT id, text, created_at FROM notes WHERE id = ?",
            (note_id,)
        )
        return cursor.fetchone()
