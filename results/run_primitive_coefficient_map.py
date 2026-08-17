"""Derive the primitive coefficient map for the Phase II rational regime.

Within a fixed active-set regime, binding cells are saturated at
    delta_ij = g_ij (1 + a_ij lambda),
while one marginal cell m absorbs the residual budget at cost
    c_m(lambda) = 1 + F lambda.
The resulting progress function has the exact form
    A + B lambda + (C + D lambda + E lambda^2)/(1 + F lambda).

No calibration-specific coefficient values are hard-coded here.
"""
from __future__ import annotations

import csv
from pathlib import Path

from model.convergence_analysis import CAPABILITIES, STATES
from model.heterogeneous_scenario import build_scenario

ROOT = Path(__file__).resolve().parents[1]
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
    state, capability = label.split(":", 1)
    return state, capability


def derive(binding_labels, marginal_label, gaps, weights, feasibility_base, costs_base):
    """Return exact primitive and rational coefficients for one regime."""
    A = 0.0
    B = 0.0
    r0 = BUDGET
    r1 = 0.0
    r2 = 0.0

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
        _, marginal_capability = parse_cell(marginal_label)
        _, marginal_state = parse_cell(marginal_label)
        # The state is retained explicitly above to make the primitive map auditable.
        state, capability = marginal_state, marginal_capability
        F = costs_base[state][capability] - 1.0
    else:
        F = 0.0

    C, D, E = r0, r1, r2
    p0 = B + D - F * C
    p1 = 2.0 * (B * F + E)
    p2 = F * (B * F + E)
    q0 = 2.0 * (E - D * F + C * F * F)
    q1 = 2.0 * F * (D * F - 2.0 * E)
    q2 = 2.0 * F * F * E
    delta_p = p1 * p1 - 4.0 * p2 * p0
    delta_q = q1 * q1 - 4.0 * q2 * q0

    # Structural identities. The residual-budget polynomial is
    # R(lambda)=r0+r1 lambda+r2 lambda^2.
    S = B * F + E
    T = E - F * D + F * F * C
    assert abs(p1 - 2.0 * S) < 1e-10
    assert abs(p2 - F * S) < 1e-10
    assert abs(delta_p - 4.0 * S * T) < 1e-8
    assert abs(q0 - 2.0 * T) < 1e-10
    assert abs(delta_p - 2.0 * (B * F + E) * q0) < 1e-8

    return dict(A=A, B=B, C=C, D=D, E=E, F=F,
                p0=p0, p1=p1, p2=p2, q0=q0, q1=q1, q2=q2,
                Delta_P=delta_p, Delta_Q=delta_q,
                S=S, T=T, r0=r0, r1=r1, r2=r2)


def main():
    gaps = read_matrix(RESULTS / "capability_gap_positive_v2.csv")
    weights = read_vector(RESULTS / "capability_dispersion_weights_v2.csv")
    feasibility_base, costs_base = build_scenario(STATES, CAPABILITIES)

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
            writer.writerow({k: row[k] if k in row else coeff[k] for k in fields})

    text = RESULTS / "primitive_coefficient_map_v1.txt"
    text.write_text(
        """12SCS PHASE II -- PRIMITIVE COEFFICIENT MAP\n\n"
        "Fix an active-set regime with binding cells i in I and at most one\n"
        "marginal cell m. Write g_i for the positive capability gap, w_i for\n"
        "the capability weight, a_i = kappa_i^0 - 1, and d_i = c_i^0 - 1.\n"
        "Then kappa_i(lambda)=1+a_i lambda and c_i(lambda)=1+d_i lambda.\n\n"
        "For binding cells, the progress contribution is w_i g_i(1+a_i lambda),\n"
        "and their budget expenditure is g_i(1+a_i lambda)(1+d_i lambda).\n"
        "Define the residual-budget polynomial R(lambda)=r0+r1 lambda+r2 lambda^2,\n"
        "where\n"
        "  r0 = B0 - sum_i g_i,\n"
        "  r1 = -sum_i g_i(a_i+d_i),\n"
        "  r2 = -sum_i g_i a_i d_i.\n\n"
        "For marginal cell m, F=d_m and the exact rational coefficients are\n"
        "  A = sum_i w_i g_i,\n"
        "  B = sum_i w_i g_i a_i,\n"
        "  C = r0,  D = r1,  E = r2.\n"
        "Hence Pi(lambda)=A+B lambda+(C+D lambda+E lambda^2)/(1+F lambda).\n\n"
        "The primitive restrictions include g_i >= 0, w_i >= 0, kappa_i^0 in [0,1],\n"
        "and c_i^0 > 0. Therefore a_i in [-1,0], d_i > -1, and F > -1.\n"
        "The last inequality makes the rational denominator strictly positive on\n"
        "[0,1] without any calibration-specific numerical assumption.\n\n"
        "The first-order numerator satisfies\n"
        "  p0=B+D-FC, p1=2(BF+E), p2=F(BF+E).\n"
        "Put S=BF+E and T=E-FD+F^2 C. Then\n"
        "  Delta_P=4ST=2(BF+E)q0,  q0=2T.\n"
        "Moreover\n"
        "  Delta_Q=4F^4(r1^2-4r0 r2).\n"
        "Thus the discriminants are not independent objects: both are generated\n"
        "by the residual-budget polynomial and the marginal-cell cost slope.\n\n"
        "A useful endogenous sign implication is\n"
        "  q2 = -2F^2 sum_i g_i a_i d_i.\n"
        "Consequently, if every binding cell has c_i^0 >= 1 (d_i >= 0), then\n"
        "q2 >= 0. If every binding cell has c_i^0 <= 1, then q2 <= 0.\n"
        "This converts a curvature coefficient sign into a primitive cost-feasibility\n"
        "condition. Analogous primitive inequalities can be tested directly for\n"
        "p0, p0+p1+p2, and T to obtain parameter-free monotonicity/curvature theorems.\n"
        """, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
