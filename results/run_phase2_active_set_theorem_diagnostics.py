"""Evaluate Phase II primitive sign conditions on every generated active-set regime.

This is deliberately a diagnostic, not a theorem assertion: it reports whether
actual regime-selection output supplies the endpoint and curvature inequalities.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from model.convergence_analysis import CAPABILITIES, STATES
from model.heterogeneous_scenario import build_scenario

RESULTS = ROOT / "results"
BUDGET = 1.0
TOL = 1e-10


def matrix_lookup(matrix):
    return {
        state: {cap: float(matrix[i][j]) for j, cap in enumerate(CAPABILITIES)}
        for i, state in enumerate(STATES)
    }


def read_matrix(path):
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    return matrix_lookup(tuple(tuple(float(x) for x in row[1:]) for row in rows[1:]))


def read_vector(path):
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    return {row[0]: float(row[1]) for row in rows[1:]}


def cell(label):
    state, capability = label.split(":", 1)
    return state, capability


def regime_certificate(binding, marginal, gaps, weights, feasibility, costs):
    marginal_state, marginal_cap = cell(marginal) if marginal else (None, None)
    F = costs[marginal_state][marginal_cap] - 1.0 if marginal else 0.0

    p0 = -F * BUDGET
    P1 = -F * BUDGET
    curvature_sum = 0.0
    ordering_failures = 0
    p0_cell_failures = 0
    P1_cell_failures = 0
    curvature_cell_failures = 0

    for label in binding:
        state, cap = cell(label)
        g = gaps[state][cap]
        w = weights[cap]
        a = feasibility[state][cap] - 1.0
        d = costs[state][cap] - 1.0

        p0_term = g * (a * (w - 1.0) + F - d)
        P1_term = g * (
            w * a * (1.0 + F) ** 2
            - (a + d)
            - a * d * (2.0 + F)
            + F
        )
        p0 += p0_term
        P1 += P1_term
        curvature_sum += g * (a - F) * (d - F)

        if a * (w - 1.0) + F - d > TOL:
            p0_cell_failures += 1
        if (
            w * a * (1.0 + F) ** 2
            - (a + d)
            - a * d * (2.0 + F)
            + F
            > TOL
        ):
            P1_cell_failures += 1
        if (a - F) * (d - F) > TOL:
            curvature_cell_failures += 1

        if marginal:
            wm = weights[marginal_cap]
            if w / (1.0 + d) + TOL < wm / (1.0 + F):
                ordering_failures += 1

    q0 = 2.0 * (F * F * BUDGET - curvature_sum)
    return {
        "F": F,
        "p0": p0,
        "P1": P1,
        "q0": q0,
        "ordering_failures": ordering_failures,
        "p0_cell_failures": p0_cell_failures,
        "P1_cell_failures": P1_cell_failures,
        "curvature_cell_failures": curvature_cell_failures,
    }


def main():
    gaps = read_matrix(RESULTS / "capability_gap_positive_v2.csv")
    weights = read_vector(RESULTS / "capability_dispersion_weights_v2.csv")
    feasibility_raw, costs_raw = build_scenario(STATES, CAPABILITIES)
    feasibility = matrix_lookup(feasibility_raw)
    costs = matrix_lookup(costs_raw)

    with (RESULTS / "convergence_active_set_regime_formulas_v2.csv").open(encoding="utf-8", newline="") as f:
        regimes = list(csv.DictReader(f))

    out = RESULTS / "phase2_active_set_theorem_diagnostics_v1.csv"
    fields = [
        "regime", "lambda_start", "lambda_end", "marginal_cell", "F",
        "p0", "P1", "q0", "ordering_failures", "p0_cell_failures",
        "P1_cell_failures", "curvature_cell_failures",
    ]
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in regimes:
            binding = [x for x in row["binding_feasibility_cells"].split(";") if x]
            marginal = row["marginal_cell"]
            c = regime_certificate(binding, marginal, gaps, weights, feasibility, costs)
            writer.writerow({
                "regime": row["regime"],
                "lambda_start": row["lambda_start"],
                "lambda_end": row["lambda_end"],
                "marginal_cell": marginal,
                **c,
            })

    rows = list(csv.DictReader(out.open(encoding="utf-8", newline="")))
    print(f"Analysed {len(rows)} active-set regimes.")
    print(f"Endpoint p0 < 0: {sum(float(r['p0']) < -TOL for r in rows)}/{len(rows)}")
    print(f"Endpoint P1 < 0: {sum(float(r['P1']) < -TOL for r in rows)}/{len(rows)}")
    print(f"Curvature q0 >= 0: {sum(float(r['q0']) >= -TOL for r in rows)}/{len(rows)}")
    print(f"Active-set ordering violations: {sum(int(r['ordering_failures']) for r in rows)}")
    print(f"Cellwise p0 violations: {sum(int(r['p0_cell_failures']) for r in rows)}")
    print(f"Cellwise P1 violations: {sum(int(r['P1_cell_failures']) for r in rows)}")
    print(f"Cellwise curvature violations: {sum(int(r['curvature_cell_failures']) for r in rows)}")


if __name__ == "__main__":
    main()
