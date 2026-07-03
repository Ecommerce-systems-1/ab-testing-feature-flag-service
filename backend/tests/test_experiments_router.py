from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_experiment():
    resp = client.post("/api/experiments", json={
        "name": "cta_color_test",
        "variants": ["control", "blue_cta"],
        "traffic_split": [50, 50],
        "description": "Test blue CTA button"
    })
    assert resp.status_code == 201
    assert resp.json()["status"] == "draft"

def test_assign_returns_valid_variant():
    # Create and start experiment first
    client.post("/api/experiments", json={
        "name": "nav_test", "variants": ["v1","v2"], "traffic_split": [50,50]
    })
    client.patch("/api/experiments/1", json={"status": "running"})
    resp = client.get("/api/assign?user_id=user-42&experiment=nav_test")
    assert resp.status_code == 200
    assert resp.json()["variant"] in ("v1", "v2")

def test_results_endpoint():
    resp = client.get("/api/experiments/1/results")
    assert resp.status_code == 200
    data = resp.json()
    assert "variants" in data
    assert isinstance(data["variants"], list)