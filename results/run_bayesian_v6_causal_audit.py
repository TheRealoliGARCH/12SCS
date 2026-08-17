"""Bayesian causal-identification audit on the verified V6 regime data.

This audit deliberately does not manufacture a causal effect from seven regimes.
It reports whether a substantive effect is identifiable from the available
regime-level artifact. A negative identification result is a successful audit
outcome, not a CI failure.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Regime:
    regime: int
    lambda_start: float
    lambda_end: float
    active_cell_count: int
    p0: float
    P1: float
    q0: float


@dataclass(frozen=True)
class Audit:
    n: int
    treated: int
    control: int
    outcomes_treated: int
    outcomes_control: int
    treatment_varies: bool
    outcome_varies: bool
    positivity: bool
    temporal_ordering: bool
    adequate_sample_for_effect: bool


def load_v6(path: Path) -> list[Regime]:
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    return [Regime(int(r["regime"]), float(r["lambda_start"]), float(r["lambda_end"]), int(r["active_cell_count"]), float(r["p0"]), float(r["P1"]), float(r["q0"])) for r in rows]


def audit(regimes: list[Regime]) -> Audit:
    if len(regimes) < 2:
        raise ValueError("at least two regimes are required")
    threshold = sorted(r.active_cell_count for r in regimes)[(len(regimes) - 1) // 2]
    treated = [r for r in regimes if r.active_cell_count >= threshold]
    control = [r for r in regimes if r.active_cell_count < threshold]
    y_t = sum(r.p0 >= 0.0 for r in treated)
    y_c = sum(r.p0 >= 0.0 for r in control)
    ordered = all(a.lambda_end <= b.lambda_start + 1e-12 for a, b in zip(regimes, regimes[1:]))
    adequate = len(regimes) >= 30 and y_t not in (0, len(treated)) and y_c not in (0, len(control))
    return Audit(len(regimes), len(treated), len(control), y_t, y_c, len({r.active_cell_count >= threshold for r in regimes}) == 2, len({r.p0 >= 0.0 for r in regimes}) == 2, bool(treated and control), ordered, adequate)


def main() -> None:
    result = audit(load_v6(Path("results/convergence_primitive_coefficient_map_v1.csv")))
    fields = list(result.__dataclass_fields__)
    out = Path("results/bayesian_v6_causal_identification_audit_v1.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(fields)
        w.writerow([getattr(result, x) for x in fields])
    print(out)
    print(result)
    print("CAUSAL_EFFECT_IDENTIFIED=" + str(result.adequate_sample_for_effect))


if __name__ == "__main__":
    main()
