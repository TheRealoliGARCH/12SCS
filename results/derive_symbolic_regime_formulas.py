"""Derive piecewise-rational regime value-function coefficients.

For a fixed active set with one residual marginal cell m, fully funded cells
contribute an affine term to progress. Their expenditure is quadratic in
lambda. The marginal allocation is residual budget divided by an affine cost,
so the regime value is rational with quadratic numerator and affine denominator.
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
from model.convergence_optimization import allocate_budget

RESULTS = ROOT / "results"
BUDGET = 1.0
TOL = 1e-9


def read_vector(path):
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    return tuple(float(r[1]) for r in rows[1:])


def read_matrix(path):
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    return tuple(tuple(float(x) for x in r[1:]) for r in rows[1:])


def affine(base, lam):
    return 1.0 + lam * (base - 1.0)


def classify(alloc, positive, feasibility):
    binding, marginal = [], []
    for i in range(len(STATES)):
        for j in range(len(CAPABILITIES)):
            if alloc[i][j] <= TOL:
                continue
            cap = positive[i][j] * feasibility[i][j]
            item = (i, j)
            if abs(alloc[i][j] - cap) <= TOL:
                binding.append(item)
            else:
                marginal.append(item)
    if len(marginal) > 1:
        raise AssertionError(f"multiple marginal cells: {marginal}")
    return binding, (marginal[0] if marginal else None)


def numerical_value(lam, positive, weights, feasibility_base, costs_base):
    feasibility = tuple(tuple(affine(x, lam) for x in row) for row in feasibility_base)
    costs = tuple(tuple(affine(x, lam) for x in row) for row in costs_base)
    alloc = allocate_budget(positive, weights, feasibility, costs, BUDGET)
    value = sum(weights[j] * alloc[i][j] for i in range(len(STATES)) for j in range(len(CAPABILITIES)))
    return value, alloc, feasibility, costs


def coefficients(binding, marginal, positive, weights, feasibility_base, costs_base):
    # Progress of fully funded cells: P0 + P1*lambda.
    p0 = 0.0
    p1 = 0.0
    e0 = 0.0
    e1 = 0.0
    e2 = 0.0
    for i, j in binding:
        g = positive[i][j]
        dk = feasibility_base[i][j] - 1.0
        dc = costs_base[i][j] - 1.0
        w = weights[j]
        p0 += w * g
        p1 += w * g * dk
        e0 += g
        e1 += g * (dk + dc)
        e2 += g * dk * dc
    if marginal is None:
        return p0, p1, 0.0, 0.0, 0.0, 0.0
    i, j = marginal
    w = weights[j]
    dc = costs_base[i][j] - 1.0
    c = w * (1.0 - e0)
    d = -w * e1
    e = -w * e2
    return p0, p1, c, d, e, dc


def value_formula(lam, coeff):
    a, b, c, d, e, f = coeff
    denominator = 1.0 + f * lam
    return a + b * lam + (c + d * lam + e * lam * lam) / denominator


def main():
    positive = read_matrix(RESULTS / "capability_gap_positive_v2.csv")
    weights = read_vector(RESULTS / "capability_dispersion_weights_v2.csv")
    feasibility_base, costs_base = build_scenario(STATES, CAPABILITIES)
    with (RESULTS / "convergence_active_set_regimes_v2.csv").open(encoding="utf-8", newline="") as f:
        regimes = list(csv.DictReader(f))
    out = RESULTS / "convergence_symbolic_regime_formulas_v2.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "regime", "lambda_start", "lambda_end", "binding_cells", "marginal_cell",
            "A", "B", "C", "D", "E", "F", "max_interior_error"
        ])
        for row in regimes:
            left, right = float(row["lambda_start"]), float(row["lambda_end"])
            mid = (left + right) / 2.0
            value, alloc, feasibility, _ = numerical_value(mid, positive, weights, feasibility_base, costs_base)
            binding, marginal = classify(alloc, positive, feasibility)
            coeff = coefficients(binding, marginal, positive, weights, feasibility_base, costs_base)
            # Validate at interior quartiles; these points remain inside the same regime.
            errors = []
            for lam in (left + 0.25 * (right - left), mid, left + 0.75 * (right - left)):
                numerical, _, _, _ = numerical_value(lam, positive, weights, feasibility_base, costs_base)
                errors.append(abs(numerical - value_formula(lam, coeff)))
            writer.writerow([
                row["regime"], left, right,
                ";".join(f"{STATES[i]}:{CAPABILITIES[j]}" for i, j in binding),
                "" if marginal is None else f"{STATES[marginal[0]]}:{CAPABILITIES[marginal[1]]}",
                *coeff, max(errors)
            ])
    print(f"Derived piecewise-rational formulas for {len(regimes)} regimes.")


if __name__ == "__main__":
    main()
