import math
from dataclasses import dataclass

@dataclass
class VariantResult:
    variant: str
    impressions: int
    conversions: int
    conversion_rate: float | None
    lift: float | None
    p_value: float | None
    significant: bool

class ResultsService:
    def compute_variant_result(self, impressions: int, conversions: int) -> VariantResult:
        rate = (conversions / impressions) if impressions > 0 else None
        return VariantResult("", impressions, conversions, rate, None, None, False)

    def compute_lift(self, control_rate: float, treatment_rate: float) -> float | None:
        if control_rate is None or control_rate == 0:
            return None
        return (treatment_rate - control_rate) / control_rate

    def z_test_p_value(self, n1: int, c1: int, n2: int, c2: int) -> float | None:
        if n1 == 0 or n2 == 0:
            return None
        p1, p2 = c1 / n1, c2 / n2
        p_pool = (c1 + c2) / (n1 + n2)
        se = math.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
        if se == 0:
            return 1.0
        z = abs(p2 - p1) / se
        # Approximation: p-value from z via erfc
        p_val = math.erfc(z / math.sqrt(2))
        return p_val

    def build_results(self, db, experiment_id: int, variants: list[str]) -> list[VariantResult]:
        results = []
        control_rate = None
        for i, variant in enumerate(variants):
            row = db.execute(
                """SELECT
                    SUM(CASE WHEN event_type='impression' THEN 1 ELSE 0 END),
                    SUM(CASE WHEN event_type='conversion' THEN 1 ELSE 0 END)
                   FROM events WHERE experiment_id=? AND variant=?""",
                (experiment_id, variant)
            ).fetchone()
            impr, conv = row[0] or 0, row[1] or 0
            rate = (conv / impr) if impr > 0 else None
            if i == 0:
                control_rate = rate
            lift = self.compute_lift(control_rate, rate) if i > 0 and rate is not None else None
            p_val = self.z_test_p_value(
                results[0].impressions, results[0].conversions, impr, conv
            ) if i > 0 and results else None
            results.append(VariantResult(variant, impr, conv, rate, lift, p_val, (p_val or 1) < 0.05))
        return results