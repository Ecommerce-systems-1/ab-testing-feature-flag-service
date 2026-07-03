import json
from datetime import datetime, timezone
from typing import Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, model_validator
from app.database import get_db
from app.services.results import ResultsService

router = APIRouter(prefix="/api/experiments", tags=["experiments"])
_results = ResultsService()


class ExperimentCreate(BaseModel):
    name: str = Field(..., min_length=1)
    variants: list[str] = Field(..., min_length=2)
    traffic_split: list[int] = Field(..., min_length=2)
    description: str | None = None

    @model_validator(mode="after")
    def check_split(self):
        if len(self.variants) != len(self.traffic_split):
            raise ValueError("variants and traffic_split must be the same length")
        if sum(self.traffic_split) > 100:
            raise ValueError("traffic_split must sum to at most 100")
        return self


class ExperimentUpdate(BaseModel):
    status: Literal["draft", "running", "completed"]


def _row_to_experiment(row) -> dict:
    d = dict(row)
    d["variants"] = json.loads(d["variants"])
    d["traffic_split"] = json.loads(d["traffic_split"])
    return d


@router.post("", status_code=201)
def create_experiment(payload: ExperimentCreate):
    db = get_db()
    now = datetime.now(timezone.utc).isoformat()
    cur = db.execute(
        "INSERT INTO experiments (name, description, variants, traffic_split, status, created_at) "
        "VALUES (?,?,?,?, 'draft', ?)",
        (payload.name, payload.description, json.dumps(payload.variants),
         json.dumps(payload.traffic_split), now),
    )
    db.commit()
    row = db.execute("SELECT * FROM experiments WHERE id=?", (cur.lastrowid,)).fetchone()
    return _row_to_experiment(row)


@router.get("")
def list_experiments():
    db = get_db()
    rows = db.execute("SELECT * FROM experiments ORDER BY id").fetchall()
    return [_row_to_experiment(r) for r in rows]


@router.patch("/{experiment_id}")
def update_experiment(experiment_id: int, payload: ExperimentUpdate):
    db = get_db()
    row = db.execute("SELECT * FROM experiments WHERE id=?", (experiment_id,)).fetchone()
    if not row:
        raise HTTPException(404, "Experiment not found")
    db.execute("UPDATE experiments SET status=? WHERE id=?", (payload.status, experiment_id))
    db.commit()
    return _row_to_experiment(
        db.execute("SELECT * FROM experiments WHERE id=?", (experiment_id,)).fetchone()
    )


@router.get("/{experiment_id}/results")
def experiment_results(experiment_id: int):
    db = get_db()
    row = db.execute("SELECT * FROM experiments WHERE id=?", (experiment_id,)).fetchone()
    if not row:
        raise HTTPException(404, "Experiment not found")
    exp = _row_to_experiment(row)
    results = _results.build_results(db, experiment_id, exp["variants"])
    return {
        "experiment_id": experiment_id,
        "name": exp["name"],
        "status": exp["status"],
        "variants": [vars(r) for r in results],
    }
