"""Derive regime-wise binding and marginal allocation diagnostics."""
from __future__ import annotations
import csv
import sys
from pathlib import Path
from model.convergence_optimization import allocate_budget, total_cost, weighted_progress
from model.convergence_analysis import CAPABILITIES, STATES
from model.heterogeneous_scenario import build_scenario
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
RESULTS = ROOT / "results"
BUDGET = 1.0
TOL = 1e-10

def read_vector(path):
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    return tuple(float(r[1]) for r in rows[1:])

def read_matrix(path):
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    return tuple(tuple(float(x) for x in r[1:]) for r in rows[1:])

def scenario(level, feasibility_base, costs_base):
    feasibility = tuple(tuple(1.0 + level * (x - 1.0) for x in row) for row in feasibility_base)
    costs = tuple(tuple(1.0 + level * (x - 1.0) for x in row) for row in costs_base)
    return feasibility, costs

def solve(level, positive, weights, feasibility_base, costs_base):
    feasibility, costs = scenario(level, feasibility_base, costs_base)
    allocation = allocate_budget(positive, weights, feasibility, costs, BUDGET)
    return allocation, feasibility, costs

def classify(allocation, positive, feasibility):
    active = []
    binding = []
    marginal = []
    for i in range(len(STATES)):
        for j in range(len(CAPABILITIES)):
            x = allocation[i][j]
            cap = positive[i][j] * feasibility[i][j]
            if x > TOL:
                label = f"{STATES[i]}:{CAPABILITIES[j]}"
                active.append(label)
                if abs(x - cap) <= TOL:
                    binding.append(label)
                else:
                    marginal.append(label)
    return active, binding, marginal

def main():
    positive = read_matrix(RESULTS / "capability_gap_positive_v2.csv")
    weights = read_vector(RESULTS / "capability_dispersion_weights_v2.csv")
    feasibility_base, costs_base = build_scenario(STATES, CAPABILITIES)
    with (RESULTS / "convergence_active_set_regimes_v2.csv").open(encoding="utf-8", newline="") as f:
        regimes = list(csv.DictReader(f))
    out = RESULTS / "convergence_active_set_regime_formulas_v2.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "regime", "lambda_start", "lambda_end", "active_cell_count",
            "active_cells", "marginal_cell", "binding_feasibility_cells",
            "budget_residual", "progress_start", "progress_mid", "progress_end",
        ])
        for row in regimes:
            left, right = float(row["lambda_start"]), float(row["lambda_end"])
            mid = (left + right) / 2.0
            allocations = []
            for level in (left, mid, right):
                allocation, feasibility, costs = solve(level, positive, weights, feasibility_base, costs_base)
                allocations.append((allocation, feasibility, costs))
            alloc_mid, feas_mid, costs_mid = allocations[1]
            active, binding, marginal = classify(alloc_mid, positive, feas_mid)
            if len(marginal) > 1:
                raise RuntimeError(f"Regime {row['regime']} has multiple marginal cells: {marginal}")
            residual = BUDGET - total_cost(alloc_mid, costs_mid)
            p0 = weighted_progress(allocations[0][0], weights)
            pm = weighted_progress(alloc_mid, weights)
            p1 = weighted_progress(allocations[2][0], weights)
            writer.writerow([
                row["regime"], left, right, len(active), ";".join(active),
                marginal[0] if marginal else "", ";".join(binding), residual,
                p0, pm, p1,
            ])
    print(f"Derived binding/marginal diagnostics for {len(regimes)} active-set regimes.")

if __name__ == "__main__":
    main()
