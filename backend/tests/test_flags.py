from services.flags import FlagService

def test_disabled_flag_returns_false():
    flag = {"name": "new_checkout", "enabled": 0, "rollout_pct": 100}
    svc = FlagService()
    assert svc.evaluate(user_id="user-1", flag=flag) is False

def test_100pct_rollout_always_true():
    flag = {"name": "new_checkout", "enabled": 1, "rollout_pct": 100}
    svc = FlagService()
    for i in range(50):
        assert svc.evaluate(user_id=f"user-{i}", flag=flag) is True

def test_0pct_rollout_always_false():
    flag = {"name": "new_checkout", "enabled": 1, "rollout_pct": 0}
    svc = FlagService()
    for i in range(50):
        assert svc.evaluate(user_id=f"user-{i}", flag=flag) is False