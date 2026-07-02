from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def setup_experiment():
    r = client.post("/api/experiments", json={
        "name": "track_test", "variants": ["control","treatment"],
        "traffic_split": [50, 50]
    })
    exp_id = r.json()["id"]
    client.patch(f"/api/experiments/{exp_id}", json={"status": "running"})
    return exp_id

def test_track_impression():
    exp_id = setup_experiment()
    resp = client.post("/api/track", json={
        "experiment_id": exp_id, "user_id": "u-1",
        "variant": "control", "event_type": "impression"
    })
    assert resp.status_code == 201

def test_track_conversion():
    exp_id = setup_experiment()
    client.post("/api/track", json={
        "experiment_id": exp_id, "user_id": "u-2",
        "variant": "treatment", "event_type": "impression"
    })
    resp = client.post("/api/track", json={
        "experiment_id": exp_id, "user_id": "u-2",
        "variant": "treatment", "event_type": "conversion"
    })
    assert resp.status_code == 201

def test_results_show_conversion_rates():
    exp_id = setup_experiment()
    for i in range(20):
        client.post("/api/track", json={"experiment_id": exp_id, "user_id": f"u-{i}",
            "variant": "control", "event_type": "impression"})
    for i in range(4):
        client.post("/api/track", json={"experiment_id": exp_id, "user_id": f"u-{i}",
            "variant": "control", "event_type": "conversion"})
    resp = client.get(f"/api/experiments/{exp_id}/results")
    assert resp.status_code == 200
    variants = resp.json()["variants"]
    control = next(v for v in variants if v["variant"] == "control")
    assert control["conversion_rate"] == pytest.approx(0.20, abs=0.01)