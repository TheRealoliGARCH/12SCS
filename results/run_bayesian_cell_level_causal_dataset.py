"""Construct the V6 cell-level causal-analysis dataset and identification audit.

This stage is deliberately a data/identification layer.  It does not estimate
an ATE because the current treatment is active-set status and the structural
outcome proxy is mechanically generated from the same allocation rule.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from model.convergence_analysis import CAPABILITIES, STATES
from model.heterogeneous_scenario import build_scenario

R = ROOT / "results"


@dataclass(frozen=True)
class CellObservation:
    regime: int
    state: str
    capability: str
    lambda_start: float
    lambda_end: float
    lambda_mid: float
    treatment_active: int
    allocation_role: str
    gap: float
    weight: float
    a: float
    d: float
    local_progress_proxy: float
    p0_regime: float


def read_matrix(path: Path) -> dict[str, dict[str, float]]:
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    if not rows or rows[0][1:] != list(CAPABILITIES):
        raise ValueError(f"invalid capability matrix: {path}")
    return {r[0]: {c: float(r[j + 1]) for j, c in enumerate(CAPABILITIES)} for r in rows[1:]}


def read_vector(path: Path) -> dict[str, float]:
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    return {r[0]: float(r[1]) for r in rows[1:]}


def parse_cells(text: str) -> set[str]:
    return {x for x in text.split(";") if x}


def build_dataset(
    regimes: list[dict[str, str]],
    gaps: dict[str, dict[str, float]],
    weights: dict[str, float],
    feasibility: dict[str, dict[str, float]],
    costs: dict[str, dict[str, float]],
) -> list[CellObservation]:
    out: list[CellObservation] = []
    for r in regimes:
        binding = parse_cells(r["binding_cells"])
        marginal = r.get("marginal_cell", "")
        lo, hi = float(r["lambda_start"]), float(r["lambda_end"])
        mid = 0.5 * (lo + hi)
        for state in STATES:
            for capability in CAPABILITIES:
                label = f"{state}:{capability}"
                if label in binding:
                    role = "binding"
                elif label == marginal:
                    role = "marginal"
                else:
                    role = "inactive"
                active = int(role != "inactive")
                g = gaps[state][capability]
                w = weights[capability]
                a = feasibility[state][capability] - 1.0
                d = costs[state][capability] - 1.0
                proxy = w * g * (1.0 + a * mid) if active else 0.0
                out.append(CellObservation(
                    int(r["regime"]), state, capability, lo, hi, mid,
                    active, role, g, w, a, d, proxy, float(r["p0"]),
                ))
    return out


def audit_identification(rows: list[CellObservation]) -> dict[str, object]:
    if not rows:
        raise ValueError("empty cell-level dataset")
    treated = [r for r in rows if r.treatment_active]
    control = [r for r in rows if not r.treatment_active]
    outcome_varies = len({round(r.local_progress_proxy, 14) for r in rows}) > 1
    treatment_varies = bool(treated and control)
    # Positivity here is descriptive: both treatment states occur within at
    # least one regime. It is not sufficient for causal identification.
    regimes = sorted({r.regime for r in rows})
    positivity = any(
        any(r.regime == k and r.treatment_active for r in rows)
        and any(r.regime == k and not r.treatment_active for r in rows)
        for k in regimes
    )
    temporal = all(r.lambda_start <= r.lambda_mid <= r.lambda_end for r in rows)
    mechanically_post_treatment = True
    intervention_defined = False
    causal_identified = False
    return {
        "n_rows": len(rows),
        "n_regimes": len(regimes),
        "n_treated": len(treated),
        "n_control": len(control),
        "treatment_varies": treatment_varies,
        "outcome_varies": outcome_varies,
        "within_regime_positivity": positivity,
        "temporal_ordering": temporal,
        "intervention_defined": intervention_defined,
        "outcome_mechanically_post_treatment": mechanically_post_treatment,
        "causal_effect_identified": causal_identified,
    }


def main() -> None:
    primitive = R / "convergence_primitive_coefficient_map_v1.csv"
    gaps_path = R / "capability_gap_positive_v2.csv"
    weights_path = R / "capability_dispersion_weights_v2.csv"
    gaps = read_matrix(gaps_path)
    weights = read_vector(weights_path)
    feasibility_raw, costs_raw = build_scenario(STATES, CAPABILITIES)
    feasibility = {s: {c: float(feasibility_raw[i][j]) for j, c in enumerate(CAPABILITIES)} for i, s in enumerate(STATES)}
    costs = {s: {c: float(costs_raw[i][j]) for j, c in enumerate(CAPABILITIES)} for i, s in enumerate(STATES)}
    with primitive.open(encoding="utf-8", newline="") as f:
        regimes = list(csv.DictReader(f))
    rows = build_dataset(regimes, gaps, weights, feasibility, costs)

    out = R / "bayesian_cell_level_causal_dataset_v1.csv"
    fields = list(CellObservation.__dataclass_fields__)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: getattr(row, k) for k in fields})

    audit = audit_identification(rows)
    audit_path = R / "bayesian_cell_level_causal_identification_v1.csv"
    with audit_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(audit))
        w.writeheader()
        w.writerow(audit)

    print(out)
    print(audit_path)
    print(audit)


if __name__ == "__main__":
    main()
