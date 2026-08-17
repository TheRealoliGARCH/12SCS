"""Bayesian causal-identification audit on the verified V6 regime data.

This module deliberately does NOT manufacture a causal effect from seven
regimes.  It maps the V6 regime-level artifact into candidate treatment,
outcome, and stratification variables and reports the identification conditions
needed before a posterior causal effect can be interpreted.

Candidate treatment: high-complexity regime, active_cell_count >= median.
Candidate outcome: local monotonicity failure, p0 >= 0.
Stratification: regime parity (a deterministic diagnostic stratum).

These are diagnostic variables, not a substantive causal claim.  The audit
checks variation, positivity, temporal ordering, and sample size.  A failed
identification condition is a valid result and prevents posterior causal
interpretation.
"""
from __future__ import annotations

import csv
import math
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
    return [
        Regime(
            regime=int(r["regime"]),
            lambda_start=float(r["lambda_start"]),
            lambda_end=float(r["lambda_end"]),
            active_cell_count=int(r["active_cell_count"]),
            p0=float(r["p0"]),
            P1=float(r["P1"]),
            q0=float(r["q0"]),
        )
        for r in rows
    ]


def audit(regimes: list[Regime]) -> Audit:
    if len(regimes) < 2:
        raise ValueError("at least two regimes are required")
    threshold = sorted(r.active_cell_count for r in regimes)[(len(regimes) - 1) // 2]
    treated = [r for r in regimes if r.active_cell_count >= threshold]
    control = [r for r in regimes if r.active_cell_count < threshold]
    y_t = sum(r.p0 >= 0.0 for r in treated)
    y_c = sum(r.p0 >= 0.0 for r in control)
    treatment_values = {r.active_cell_count >= threshold for r in regimes}
    outcome_values = {r.p0 >= 0.0 for r in regimes}
    ordered = all(a.lambda_end <= b.lambda_start + 1e-12 for a, b in zip(regimes, regimes[1:]))
    # Seven regime-level observations are intentionally treated as inadequate
    # for a substantive causal effect estimate, even when binary variation exists.
    adequate = len(regimes) >= 30 and y_t not in (0, len(treated)) and y_c not in (0, len(control))
    return Audit(
        n=len(regimes),
        treated=len(treated),
        control=len(control),
        outcomes_treated=y_t,
        outcomes_control=y_c,
        treatment_varies=len(treatment_values) == 2,
        outcome_varies=len(outcome_values) == 2,
        positivity=len(treated) > 0 and len(control) > 0,
        temporal_ordering=ordered,
        adequate_sample_for_effect=adequate,
    )


def main() -> None:
    path = Path("results/convergence_primitive_coefficient_map_v1.csv")
    regimes = load_v6(path)
    result = audit(regimes)
    fields = ["n", "treated", "control", "outcomes_treated", "outcomes_control", "treatment_varies", "outcome_varies", "positivity", "temporal_ordering", "adequate_sample_for_effect"]
    out = Path("results/bayesian_v6_causal_identification_audit_v1.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(fields)
        w.writerow([getattr(result, x) for x in fields])
    print(out)
    print(result)
    if not result.treatment_varies:
        raise SystemExit("identification audit: treatment variation failed")
    if not result.outcome_varies:
        raise SystemExit("identification audit: outcome variation failed")
    if not result.positivity:
        raise SystemExit("identification audit: positivity failed")
    if not result.temporal_ordering:
        raise SystemExit("identification audit: temporal ordering failed")
    if not result.adequate_sample_for_effect:
        raise SystemExit("identification audit: substantive causal effect is not identified from seven regimes")


if __name__ == "__main__":
    main()
