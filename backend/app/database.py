import os
import sqlite3

DB_PATH = os.getenv("DB_PATH", ":memory:")

_conn: sqlite3.Connection | None = None

SCHEMA = """
CREATE TABLE IF NOT EXISTS experiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    variants TEXT NOT NULL,
    traffic_split TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft'
        CHECK(status IN ('draft','running','completed')),
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id INTEGER NOT NULL REFERENCES experiments(id),
    user_id TEXT NOT NULL,
    variant TEXT NOT NULL,
    event_type TEXT NOT NULL CHECK(event_type IN ('impression','conversion')),
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_events_exp ON events(experiment_id, variant, event_type);
CREATE TABLE IF NOT EXISTS flags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    enabled INTEGER NOT NULL DEFAULT 0,
    rollout_pct INTEGER NOT NULL DEFAULT 0 CHECK(rollout_pct BETWEEN 0 AND 100),
    created_at TEXT NOT NULL
);
"""


def get_db() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        if DB_PATH != ":memory:":
            os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _conn.executescript(SCHEMA)
        _conn.commit()
    return _conn
