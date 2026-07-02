from services.results import ResultsService, VariantResult

def test_conversion_rate_calculation():
    svc = ResultsService()
    r = svc.compute_variant_result(impressions=100, conversions=10)
    assert r.conversion_rate == pytest.approx(0.10, abs=0.001)

def test_lift_vs_control():
    svc = ResultsService()
    control = svc.compute_variant_result(100, 10)
    treatment = svc.compute_variant_result(100, 15)
    lift = svc.compute_lift(control.conversion_rate, treatment.conversion_rate)
    assert lift == pytest.approx(0.50, abs=0.01)  # 50% lift

def test_significant_result():
    svc = ResultsService()
    p = svc.z_test_p_value(n1=500, c1=50, n2=500, c2=100)
    assert p < 0.05

def test_not_significant_result():
    svc = ResultsService()
    p = svc.z_test_p_value(n1=50, c1=5, n2=50, c2=6)
    assert p > 0.05

def test_zero_impressions_returns_none():
    import pytest
    svc = ResultsService()
    r = svc.compute_variant_result(impressions=0, conversions=0)
    assert r.conversion_rate is None
    assert r.p_value is None