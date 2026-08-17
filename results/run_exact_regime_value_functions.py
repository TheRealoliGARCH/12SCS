"""Derive and validate exact piecewise value functions for active-set regimes."""
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

def scenario(level, base):
    return tuple(tuple(1.0 + level * (x - 1.0) for x in row) for row in base)

def evaluate(level, positive, weights, feasibility_base, costs_base):
    feasibility = scenario(level, feasibility_base)
    costs = scenario(level, costs_base)
    alloc = allocate_budget(positive, weights, feasibility, costs, BUDGET)
    progress = sum(weights[j] * alloc[i][j] for i in range(len(STATES)) for j in range(len(CAPABILITIES)))
    return alloc, progress, feasibility, costs

def classify(alloc, positive, feasibility, tol=TOL):
    active, binding, marginal = [], [], []
    for i in range(len(STATES)):
        for j in range(len(CAPABILITIES)):
            if alloc[i][j] <= tol:
                continue
            active.append((i, j))
            cap = positive[i][j] * feasibility[i][j]
            label = f"{STATES[i]}:{CAPABILITIES[j]}"
            if abs(alloc[i][j] - cap) <= tol:
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
    out = RESULTS / "convergence_exact_regime_value_functions_v2.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["regime", "lambda_start", "lambda_end", "active_cells", "binding_cells", "marginal_cells", "progress_start", "progress_mid", "progress_end", "left_right_gap"])
        for row in regimes:
            left, right = float(row["lambda_start"]), float(row["lambda_end"])
            mid = (left + right) / 2.0
            values = []
            classifications = []
            for level in (left, mid, right):
                alloc, progress, feasibility, costs = evaluate(level, positive, weights, feasibility_base, costs_base)
                values.append(progress)
                classifications.append(classify(alloc, positive, feasibility))
            active, binding, marginal = classifications[1]
            # Regime interiors must have a stable active signature and at most one residual marginal cell.
            if len(marginal) > 1:
                raise AssertionError(f"regime {row['regime']} has multiple marginal cells: {marginal}")
            writer.writerow([
                row["regime"], left, right,
                ";".join(f"{STATES[i]}:{CAPABILITIES[j]}" for i, j in active),
                ";".join(binding), ";".join(marginal),
                values[0], values[1], values[2], abs(values[2] - values[0])
            ])
    print(f"Derived exact-regime diagnostics for {len(regimes)} regimes.")

if __name__ == "__main__":
    main()
