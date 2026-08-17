"""Reduce pairwise ranking crossovers to genuine active-set regimes."""
from __future__ import annotations
import csv
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from model.convergence_analysis import CAPABILITIES, STATES
from model.convergence_optimization import allocate_budget
from model.heterogeneous_scenario import build_scenario
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

def active_signature(alloc):
    return tuple((i, j) for i in range(len(STATES)) for j in range(len(CAPABILITIES)) if alloc[i][j] > TOL)

def solve(level, positive, weights, feasibility_base, costs_base):
    feasibility = tuple(tuple(1.0 + level * (x - 1.0) for x in row) for row in feasibility_base)
    costs = tuple(tuple(1.0 + level * (x - 1.0) for x in row) for row in costs_base)
    alloc = allocate_budget(positive, weights, feasibility, costs, BUDGET)
    progress = sum(weights[j] * alloc[i][j] for i in range(len(STATES)) for j in range(len(CAPABILITIES)))
    return active_signature(alloc), progress

def main():
    positive = read_matrix(RESULTS / "capability_gap_positive_v2.csv")
    weights = read_vector(RESULTS / "capability_dispersion_weights_v2.csv")
    feasibility_base, costs_base = build_scenario(STATES, CAPABILITIES)
    with (RESULTS / "convergence_active_set_breakpoints_v2.csv").open(encoding="utf-8", newline="") as f:
        points = sorted({float(r["lambda"]) for r in csv.DictReader(f)})
    bounds = sorted({0.0, *points, 1.0})
    regimes = []
    previous = None
    for left, right in zip(bounds[:-1], bounds[1:]):
        if right - left <= TOL:
            continue
        mid = (left + right) / 2.0
        signature, _ = solve(mid, positive, weights, feasibility_base, costs_base)
        if signature != previous:
            regimes.append([left, right, signature])
            previous = signature
        else:
            regimes[-1][1] = right
    out = RESULTS / "convergence_active_set_regimes_v2.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["regime", "lambda_start", "lambda_end", "active_cell_count", "active_cells", "progress_start", "progress_mid", "progress_end"])
        for k, (left, right, signature) in enumerate(regimes):
            mid = (left + right) / 2.0
            _, p0 = solve(left, positive, weights, feasibility_base, costs_base)
            _, pm = solve(mid, positive, weights, feasibility_base, costs_base)
            _, p1 = solve(right, positive, weights, feasibility_base, costs_base)
            cells = ";".join(f"{STATES[i]}:{CAPABILITIES[j]}" for i, j in signature)
            writer.writerow([k, left, right, len(signature), cells, p0, pm, p1])
    print(f"Reduced {len(bounds) - 2} ranking crossover locations to {len(regimes)} active-set regimes.")

if __name__ == "__main__":
    main()
