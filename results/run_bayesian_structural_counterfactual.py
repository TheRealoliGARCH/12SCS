"""Audit whether the canonical structural objective responds to d.

The V6 primitive map has
    Pi(lambda) = A + B lambda + (C + D lambda + E lambda^2)/(1 + F lambda).
The coefficient d enters D and E for binding cells and F for the marginal cell.
This stage computes the deterministic structural counterfactual
    do(d_cell <- 0.9 d_cell)
for admissible cells (d_cell >= 0) and verifies that the objective changes for
at least one admissible cell. It makes no empirical causal claim.
"""
from __future__ import annotations

import csv
import math
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from model.convergence_analysis import CAPABILITIES, STATES
from model.heterogeneous_scenario import build_scenario
from results.run_primitive_coefficient_map import read_matrix, read_vector, parse_cell

RESULTS = ROOT / "results"
LAMBDA_TOL = 1e-12
EFFECT_TOL = 1e-12


@dataclass(frozen=True)
class CounterfactualAudit:
    n_regimes: int
    n_cells: int
    n_admissible_cells: int
    n_excluded_cells: int
    n_nonzero_cell_effects: int
    max_abs_effect: float
    objective_definition: str
    intervention: str
    outcome_responds_to_d: bool
    structural_estimand_defined: bool
    empirical_ate_identified: bool
    status: str


def _matrix_lookup(matrix):
    return {
        state: {cap: float(matrix[i][j]) for j, cap in enumerate(CAPABILITIES)}
        for i, state in enumerate(STATES)
    }


def _coefficient_map(binding, marginal, gaps, weights, feasibility, costs, overrides):
    a_sum = b_sum = 0.0
    r0, r1, r2 = 1.0, 0.0, 0.0
    for label in binding:
        state, capability = parse_cell(label)
        g = gaps[state][capability]
        w = weights[capability]
        a = feasibility[state][capability] - 1.0
        d = overrides.get(label, costs[state][capability] - 1.0)
        a_sum += w * g
        b_sum += w * g * a
        r0 -= g
        r1 -= g * (a + d)
        r2 -= g * a * d
    if marginal:
        state, capability = parse_cell(marginal)
        F = overrides.get(marginal, costs[state][capability] - 1.0)
    else:
        F = 0.0
    C, D, E = r0, r1, r2
    return a_sum, b_sum, C, D, E, F


def _objective(coeff, lam):
    A, B, C, D, E, F = coeff
    denominator = 1.0 + F * lam
    if denominator <= 0.0:
        raise ValueError("structural objective denominator is non-positive")
    return A + B * lam + (C + D * lam + E * lam * lam) / denominator


def audit(rows, gaps, weights, feasibility, costs, delta=0.10):
    if not rows or not (0.0 < delta < 1.0):
        raise ValueError("non-empty regimes and 0 < delta < 1 are required")
    all_labels = [f"{s}:{c}" for s in STATES for c in CAPABILITIES]
    d_values = {
        label: costs[s][c] - 1.0
        for s in STATES for c in CAPABILITIES
        for label in [f"{s}:{c}"]
    }
    admissible = {label for label, d in d_values.items() if d >= 0.0}
    excluded = set(all_labels) - admissible
    effects = []
    for row in rows:
        binding = [x for x in row["binding_cells"].split(";") if x]
        marginal = row.get("marginal_cell", "")
        lo, hi = float(row["lambda_start"]), float(row["lambda_end"])
        lam = 0.5 * (lo + hi)
        baseline = _coefficient_map(binding, marginal, gaps, weights, feasibility, costs, {})
        base_value = _objective(baseline, lam)
        active_d_labels = set(binding)
        if marginal:
            active_d_labels.add(marginal)
        for label in sorted(admissible):
            if label not in active_d_labels:
                continue
            d = d_values[label]
            overrides = {label: (1.0 - delta) * d}
            cf = _coefficient_map(binding, marginal, gaps, weights, feasibility, costs, overrides)
            effect = _objective(cf, lam) - base_value
            if not math.isfinite(effect):
                raise ValueError(f"non-finite counterfactual effect for {label}")
            effects.append(effect)
    nonzero = sum(abs(x) > EFFECT_TOL for x in effects)
    maximum = max((abs(x) for x in effects), default=0.0)
    responds = nonzero > 0
    structural = responds and bool(admissible)
    status = (
        "STRUCTURAL_ESTIMAND_DEFINED_BUT_EMPIRICAL_ATE_NOT_IDENTIFIED"
        if structural else "STRUCTURAL_ESTIMAND_NOT_ESTABLISHED"
    )
    return CounterfactualAudit(
        len(rows), len(all_labels), len(admissible), len(excluded), nonzero,
        maximum,
        "Pi(lambda)=A+B*lambda+(C+D*lambda+E*lambda^2)/(1+F*lambda)",
        "do(d_cell <- 0.9*d_cell)", responds, structural, False, status,
    )


def main():
    gaps = read_matrix(RESULTS / "capability_gap_positive_v2.csv")
    weights = read_vector(RESULTS / "capability_dispersion_weights_v2.csv")
    feasibility_raw, costs_raw = build_scenario(STATES, CAPABILITIES)
    feasibility = _matrix_lookup(feasibility_raw)
    costs = _matrix_lookup(costs_raw)
    with (RESULTS / "convergence_primitive_coefficient_map_v1.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    result = audit(rows, gaps, weights, feasibility, costs)
    out = RESULTS / "bayesian_structural_counterfactual_estimand_audit_v1.csv"
    fields = list(result.__dataclass_fields__)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        writer.writerow([getattr(result, field) for field in fields])
    print(out)
    print(result)


if __name__ == "__main__":
    main()
