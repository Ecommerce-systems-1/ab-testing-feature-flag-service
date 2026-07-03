import json
from datetime import datetime, timezone
from typing import Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.database import get_db
from app.services.assignment import AssignmentService

router = APIRouter(prefix="/api", tags=["tracking"])
_assigner = AssignmentService()


class TrackEvent(BaseModel):
    experiment_id: int
    user_id: str = Field(..., min_length=1)
    variant: str = Field(..., min_length=1)
    event_type: Literal["impression", "conversion"]


@router.post("/track", status_code=201)
def track(payload: TrackEvent):
    db = get_db()
    exp = db.execute("SELECT * FROM experiments WHERE id=?", (payload.experiment_id,)).fetchone()
    if not exp:
        raise HTTPException(404, "Experiment not found")
    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        "INSERT INTO events (experiment_id, user_id, variant, event_type, created_at) VALUES (?,?,?,?,?)",
        (payload.experiment_id, payload.user_id, payload.variant, payload.event_type, now),
    )
    db.commit()
    return {"tracked": True, "experiment_id": payload.experiment_id, "event_type": payload.event_type}


@router.get("/assign")
def assign(user_id: str, experiment: str):
    db = get_db()
    row = db.execute(
        "SELECT * FROM experiments WHERE name=? ORDER BY id DESC LIMIT 1", (experiment,)
    ).fetchone()
    if not row:
        raise HTTPException(404, f"Experiment '{experiment}' not found")
    exp = {
        "id": row["id"],
        "variants": json.loads(row["variants"]),
        "traffic_split": json.loads(row["traffic_split"]),
    }
    variant = _assigner.assign(user_id, exp)
    return {"experiment": experiment, "user_id": user_id, "variant": variant}
