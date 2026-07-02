# Data Model — AB Testing & Feature Flag Service

```sql
CREATE TABLE IF NOT EXISTS feature_flags (id TEXT PRIMARY KEY, name TEXT NOT NULL UNIQUE, description TEXT, enabled INTEGER DEFAULT 0, rollout_percentage INTEGER DEFAULT 100, created_at TEXT DEFAULT (datetime('now')), updated_at TEXT DEFAULT (datetime('now')));
```
