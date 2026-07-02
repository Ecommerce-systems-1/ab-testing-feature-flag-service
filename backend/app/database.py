import uuid
import aiosqlite
from typing import List, Dict, Any

class Database:
    def __init__(self, path: str = '/data/18_ab_testing_feature_flag_service.db'):
        self.path = path
        self._conn = None

    async def init(self):
        self._conn = await aiosqlite.connect(self.path)
        self._conn.row_factory = aiosqlite.Row
        await self._conn.execute('PRAGMA journal_mode=WAL')
        await self._conn.executescript('''
            CREATE TABLE IF NOT EXISTS feature_flags (id TEXT PRIMARY KEY, name TEXT NOT NULL UNIQUE, description TEXT, enabled INTEGER DEFAULT 0, rollout_percentage INTEGER DEFAULT 100, created_at TEXT DEFAULT (datetime('now')), updated_at TEXT DEFAULT (datetime('now')));
            CREATE TABLE IF NOT EXISTS experiments (id TEXT PRIMARY KEY, name TEXT NOT NULL, flag_id TEXT NOT NULL, variant_a TEXT NOT NULL, variant_b TEXT NOT NULL, traffic_percentage INTEGER DEFAULT 50, status TEXT DEFAULT 'draft', created_at TEXT DEFAULT (datetime('now')));
            CREATE TABLE IF NOT EXISTS experiment_events (id INTEGER PRIMARY KEY AUTOINCREMENT, experiment_id TEXT NOT NULL, user_id TEXT NOT NULL, variant TEXT NOT NULL, converted INTEGER DEFAULT 0, created_at TEXT DEFAULT (datetime('now')));
        ''')
        await self._conn.commit()

    async def close(self):
        if self._conn:
            await self._conn.close()
