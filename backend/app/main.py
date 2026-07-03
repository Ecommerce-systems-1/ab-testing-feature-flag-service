from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import pathlib
from app.database import get_db
from app.routers import experiments, tracking, flags

app = FastAPI(title="A/B Testing & Feature Flag Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(experiments.router)
app.include_router(tracking.router)
app.include_router(flags.router)

get_db()  # initialise schema at import; tests use TestClient without lifespan


@app.get("/health")
def health():
    db = get_db()
    experiments_count = db.execute("SELECT COUNT(*) FROM experiments").fetchone()[0]
    flags_count = db.execute("SELECT COUNT(*) FROM flags").fetchone()[0]
    return {"status": "ok", "experiments": experiments_count, "flags": flags_count}


static_dir = pathlib.Path("/app/frontend/out")
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
