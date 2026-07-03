from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.database import get_db
from app.services.flags import FlagService

router = APIRouter(prefix="/api/flags", tags=["flags"])
_flags = FlagService()


class FlagCreate(BaseModel):
    name: str = Field(..., min_length=1)
    enabled: bool = False
    rollout_pct: int = Field(0, ge=0, le=100)


@router.post("", status_code=201)
def create_flag(payload: FlagCreate):
    db = get_db()
    now = datetime.now(timezone.utc).isoformat()
    try:
        cur = db.execute(
            "INSERT INTO flags (name, enabled, rollout_pct, created_at) VALUES (?,?,?,?)",
            (payload.name, int(payload.enabled), payload.rollout_pct, now),
        )
    except Exception:
        raise HTTPException(409, f"Flag '{payload.name}' already exists")
    db.commit()
    return dict(db.execute("SELECT * FROM flags WHERE id=?", (cur.lastrowid,)).fetchone())


@router.get("")
def list_flags():
    db = get_db()
    return [dict(r) for r in db.execute("SELECT * FROM flags ORDER BY id").fetchall()]


@router.get("/evaluate")
def evaluate(user_id: str, flag: str):
    db = get_db()
    row = db.execute("SELECT * FROM flags WHERE name=?", (flag,)).fetchone()
    if not row:
        raise HTTPException(404, f"Flag '{flag}' not found")
    enabled = _flags.evaluate(
        user_id, {"name": row["name"], "enabled": bool(row["enabled"]), "rollout_pct": row["rollout_pct"]}
    )
    return {"flag": flag, "user_id": user_id, "enabled": enabled}
