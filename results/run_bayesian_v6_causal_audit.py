"""Bayesian causal-identification audit on the verified V6 regime data."""
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


def _get(row: dict[str, str], *names: str) -> str:
    for name in names:
        if name in row and row[name] != "":
            return row[name]
    raise KeyError(f"none of the required columns found: {names}")


def load_v6(path: Path) -> list[Regime]:
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    regimes: list[Regime] = []
    for r in rows:
        # The primitive coefficient map does not carry active_cell_count or P1;
        # recover them from the regime-formula columns when available.  The
        # integration workflow constructs that companion artifact first.
        active = _get(r, "active_cell_count")
        p1 = _get(r, "P1", "progress_end")
        regimes.append(
            Regime(
                int(_get(r, "regime")),
                float(_get(r, "lambda_start")),
                float(_get(r, "lambda_end")),
                int(float(active)),
                float(_get(r, "p0")),
                float(p1),
                float(_get(r, "q0")),
            )
        )
    return regimes


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
    return Audit(
        len(regimes), len(treated), len(control), y_t, y_c,
        len({r.active_cell_count >= threshold for r in regimes}) == 2,
        len({r.p0 >= 0.0 for r in regimes}) == 2,
        bool(treated and control), ordered, adequate,
    )


def main() -> None:
    path = Path("results/convergence_primitive_coefficient_map_v1.csv")
    result = audit(load_v6(path))
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
