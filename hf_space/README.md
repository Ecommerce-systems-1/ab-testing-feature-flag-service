---
title: A/B Testing & Feature Flag Service
emoji: 🧪
colorFrom: pink
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
---

# A/B Testing & Feature Flag Service

Deterministic hash-based variant assignment, impression/conversion tracking, and z-test significance on results.

The landing page is an interactive API console — click any endpoint to call the live API.

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/experiments` | Create experiment |
| PATCH | `/api/experiments/{id}` | Update status |
| GET | `/api/assign?user_id=&experiment=` | Assign a variant |
| POST | `/api/track` | Track impression/conversion |
| GET | `/api/experiments/{id}/results` | Results + p-values |
| GET | `/api/flags/evaluate?user_id=&flag=` | Evaluate a feature flag |

## Stack

Python 3.11 · FastAPI · SQLite · Pydantic v2 · Next.js 14 (static export) · Tailwind CSS · Docker
