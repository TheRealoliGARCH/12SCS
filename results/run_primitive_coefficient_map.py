"""Derive the primitive coefficient map for a fixed active-set regime."""
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


def read_matrix(path: Path):
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    if rows[0][1:] != list(CAPABILITIES):
        raise ValueError(f"Capability header mismatch in {path}")
    return {row[0]: {c: float(row[j + 1]) for j, c in enumerate(CAPABILITIES)}
            for row in rows[1:]}


def read_vector(path: Path):
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    return {row[0]: float(row[1]) for row in rows[1:]}


def parse_cell(label: str):
    return label.split(":", 1)


def matrix_to_lookup(matrix):
    return {state: {cap: float(matrix[i][j]) for j, cap in enumerate(CAPABILITIES)}
            for i, state in enumerate(STATES)}


def derive(binding_labels, marginal_label, gaps, weights, feasibility_base, costs_base):
    A = B = 0.0
    r0, r1, r2 = BUDGET, 0.0, 0.0
    for label in binding_labels:
        state, capability = parse_cell(label)
        g = gaps[state][capability]
        w = weights[capability]
        a = feasibility_base[state][capability] - 1.0
        d = costs_base[state][capability] - 1.0
        A += w * g
        B += w * g * a
        r0 -= g
        r1 -= g * (a + d)
        r2 -= g * a * d

    if marginal_label:
        state, capability = parse_cell(marginal_label)
        F = costs_base[state][capability] - 1.0
    else:
        F = 0.0

    C, D, E = r0, r1, r2
    p0 = B + D - F * C
    S = B * F + E
    p1 = 2.0 * S
    p2 = F * S

    # Exact cancellation in the second derivative.
    q0 = 2.0 * (E - F * D + F * F * C)
    q1 = 0.0
    q2 = 0.0

    delta_p = p1 * p1 - 4.0 * p2 * p0
    delta_q = 0.0
    T = E - F * D + F * F * C

    assert abs(p1 - 2.0 * S) < 1e-10
    assert abs(p2 - F * S) < 1e-10
    assert abs(delta_p - 4.0 * S * T) < 1e-8
    assert abs(q0 - 2.0 * T) < 1e-10
    assert q1 == 0.0 and q2 == 0.0
    assert delta_q == 0.0

    return dict(A=A, B=B, C=C, D=D, E=E, F=F,
                p0=p0, p1=p1, p2=p2, q0=q0, q1=q1, q2=q2,
                Delta_P=delta_p, Delta_Q=delta_q,
                S=S, T=T, r0=r0, r1=r1, r2=r2)


def main():
    gaps = read_matrix(RESULTS / "capability_gap_positive_v2.csv")
    weights = read_vector(RESULTS / "capability_dispersion_weights_v2.csv")
    feasibility_raw, costs_raw = build_scenario(STATES, CAPABILITIES)
    feasibility_base = matrix_to_lookup(feasibility_raw)
    costs_base = matrix_to_lookup(costs_raw)

    with (RESULTS / "convergence_active_set_regime_formulas_v2.csv").open(encoding="utf-8", newline="") as f:
        regimes = list(csv.DictReader(f))

    out = RESULTS / "convergence_primitive_coefficient_map_v1.csv"
    fields = ["regime", "lambda_start", "lambda_end", "binding_cells", "marginal_cell",
              "A", "B", "C", "D", "E", "F", "p0", "p1", "p2", "q0", "q1", "q2",
              "Delta_P", "Delta_Q", "S", "T", "r0", "r1", "r2"]
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in regimes:
            binding = [x for x in row["binding_feasibility_cells"].split(";") if x]
            marginal = row["marginal_cell"] or ""
            coeff = derive(binding, marginal, gaps, weights, feasibility_base, costs_base)
            output = {k: row[k] for k in ("regime", "lambda_start", "lambda_end")}
            output.update({"binding_cells": ";".join(binding), "marginal_cell": marginal})
            output.update({k: coeff[k] for k in fields if k in coeff})
            writer.writerow(output)

    (RESULTS / "primitive_coefficient_map_v1.txt").write_text(
        "12SCS PHASE II -- PRIMITIVE COEFFICIENT MAP\n\n"
        "For binding cells i, let a_i=kappa_i^0-1, d_i=c_i^0-1, gap g_i,\n"
        "weight w_i, and let F=d_m for the marginal cell. Then\n"
        "A=sum_i w_i g_i, B=sum_i w_i g_i a_i, C=B0-sum_i g_i,\n"
        "D=-sum_i g_i(a_i+d_i), E=-sum_i g_i a_i d_i.\n\n"
        "The first derivative numerator is P=p0+p1 lambda+p2 lambda^2 with\n"
        "p0=B+D-FC, p1=2(BF+E), p2=F(BF+E).\n"
        "Writing S=BF+E and T=E-FD+F^2 C gives Delta_P=4ST and q0=2T.\n"
        "The second derivative is exactly q0/(1+F lambda)^3; hence q1=q2=0\n"
        "and Delta_Q=0 identically.\n",
        encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
