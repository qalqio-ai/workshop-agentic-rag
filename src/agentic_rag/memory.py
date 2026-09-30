import sqlite3
import time
from pathlib import Path


class SessionMemory:
    def __init__(self, db_path: str, ttl_seconds: int):
        self.db_path = db_path
        self.ttl_seconds = ttl_seconds
        if db_path != ":memory:":
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS turns ("
                "session_id TEXT PRIMARY KEY, use_case_id TEXT NOT NULL, "
                "context TEXT NOT NULL, updated_at REAL NOT NULL)"
            )

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def get(self, session_id: str, use_case_id: str) -> str | None:
        cutoff = time.time() - self.ttl_seconds
        with self._connect() as db:
            row = db.execute(
                "SELECT context, updated_at FROM turns WHERE session_id=? AND use_case_id=?",
                (session_id, use_case_id),
            ).fetchone()
            if not row:
                return None
            if row[1] < cutoff:
                db.execute("DELETE FROM turns WHERE session_id=?", (session_id,))
                return None
            return str(row[0])

    def put(self, session_id: str, use_case_id: str, context: str) -> None:
        with self._connect() as db:
            db.execute(
                "INSERT INTO turns VALUES (?, ?, ?, ?) "
                "ON CONFLICT(session_id) DO UPDATE SET use_case_id=excluded.use_case_id, "
                "context=excluded.context, updated_at=excluded.updated_at",
                (session_id, use_case_id, context[:2_000], time.time()),
            )

    def delete(self, session_id: str) -> None:
        with self._connect() as db:
            db.execute("DELETE FROM turns WHERE session_id=?", (session_id,))
