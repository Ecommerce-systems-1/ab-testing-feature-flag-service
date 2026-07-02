from services.assignment import AssignmentService

EXP = {"id": 42, "variants": ["control", "treatment"], "traffic_split": [50, 50]}

def test_same_user_always_gets_same_variant():
    svc = AssignmentService()
    v1 = svc.assign(user_id="user-123", experiment=EXP)
    v2 = svc.assign(user_id="user-123", experiment=EXP)
    assert v1 == v2

def test_different_users_distribute_across_variants():
    svc = AssignmentService()
    results = [svc.assign(f"user-{i}", EXP) for i in range(1000)]
    control_pct = results.count("control") / 1000
    assert 0.45 < control_pct < 0.55, f"Unexpected split: {control_pct}"

def test_unequal_split():
    exp = {"id": 1, "variants": ["control", "treatment"], "traffic_split": [80, 20]}
    svc = AssignmentService()
    results = [svc.assign(f"user-{i}", exp) for i in range(2000)]
    control_pct = results.count("control") / 2000
    assert 0.75 < control_pct < 0.85

def test_excluded_when_splits_sum_below_100():
    exp = {"id": 1, "variants": ["control", "treatment"], "traffic_split": [10, 10]}
    svc = AssignmentService()
    results = [svc.assign(f"user-{i}", exp) for i in range(1000)]
    excluded = results.count(None)
    assert excluded > 700  # ~80% excluded