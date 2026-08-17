"""Derive regime-wise symbolic allocation/value formulas for the synthetic allocator."""
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
TOL = 1e-12

def read_vector(path):
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    return tuple(float(r[1]) for r in rows[1:])

def read_matrix(path):
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    return tuple(tuple(float(x) for x in r[1:]) for r in rows[1:])

def solve(level, positive, weights, feasibility_base, costs_base):
    feasibility = tuple(tuple(1.0 + level * (x - 1.0) for x in row) for row in feasibility_base)
    costs = tuple(tuple(1.0 + level * (x - 1.0) for x in row) for row in costs_base)
    alloc = allocate_budget(positive, weights, feasibility, costs, BUDGET)
    progress = sum(weights[j] * alloc[i][j] for i in range(len(STATES)) for j in range(len(CAPABILITIES)))
    return alloc, progress

def active_signature(alloc):
    return tuple((i, j) for i in range(len(STATES)) for j in range(len(CAPABILITIES)) if alloc[i][j] > TOL)

def main():
    positive = read_matrix(RESULTS / "capability_gap_positive_v2.csv")
    weights = read_vector(RESULTS / "capability_dispersion_weights_v2.csv")
    feasibility_base, costs_base = build_scenario(STATES, CAPABILITIES)
    with (RESULTS / "convergence_active_set_regimes_v2.csv").open(encoding="utf-8", newline="") as f:
        regimes = list(csv.DictReader(f))
    out = RESULTS / "convergence_active_set_regime_formulas_v2.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["regime", "lambda_start", "lambda_end", "active_cell_count", "marginal_cells", "binding_feasibility_cells", "progress_start", "progress_mid", "progress_end", "continuity_error"])
        for row in regimes:
            left, right = float(row["lambda_start"]), float(row["lambda_end"])
            mid = (left + right) / 2.0
            a0, p0 = solve(left, positive, weights, feasibility_base, costs_base)
            am, pm = solve(mid, positive, weights, feasibility_base, costs_base)
            a1, p1 = solve(right, positive, weights, feasibility_base, costs_base)
            marginal = []
            binding = []
            for i, j in zip(*__import__('numpy').where(am > TOL)):
                cap = positive[i][j] * (1.0 + mid * (feasibility_base[i][j] - 1.0))
                if abs(am[i][j] - cap) > 1e-9:
                    marginal.append(f"{STATES[i]}:{CAPABILITIES[j]}")
                if abs(am[i][j] - cap) <= 1e-9:
                    binding.append(f"{STATES[i]}:{CAPABILITIES[j]}")
            writer.writerow([row["regime"], left, right, row["active_cell_count"], ";".join(marginal), ";".join(binding), p0, pm, p1, abs(p1 - p0)])
    print(f"Derived regime diagnostics for {len(regimes)} active-set regimes.")

if __name__ == "__main__":
    main()
