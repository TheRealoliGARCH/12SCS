"""Run the abstract heterogeneous cost-feasibility convergence scenario."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from model.convergence_analysis import CAPABILITIES, STATES
from model.convergence_optimization import allocate_budget, total_cost, weighted_progress
from model.heterogeneous_scenario import build_scenario

RESULTS = ROOT / "results"
BUDGET = 1.0


def read_vector(path: Path):
    with path.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    return tuple(float(row[1]) for row in rows[1:])


def read_matrix(path: Path):
    with path.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    return tuple(tuple(float(x) for x in row[1:]) for row in rows[1:])


def write_matrix(path: Path, header, row_names, matrix):
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([header, *CAPABILITIES])
        writer.writerows([[name, *row] for name, row in zip(row_names, matrix)])


def main() -> None:
    positive = read_matrix(RESULTS / "capability_gap_positive_v2.csv")
    weights = read_vector(RESULTS / "capability_dispersion_weights_v2.csv")
    feasibility, costs = build_scenario(STATES, CAPABILITIES)
    allocation = allocate_budget(positive, weights, feasibility, costs, BUDGET)
    spent = total_cost(allocation, costs)
    progress = weighted_progress(allocation, weights)

    if spent > BUDGET + 1e-12:
        raise AssertionError("heterogeneous allocation exceeds budget")
    for i in range(len(STATES)):
        for j in range(len(CAPABILITIES)):
            cap = positive[i][j] * feasibility[i][j]
            if allocation[i][j] < -1e-12 or allocation[i][j] > cap + 1e-12:
                raise AssertionError("heterogeneous allocation violates feasibility cap")

    write_matrix(RESULTS / "convergence_allocation_heterogeneous_v2.csv", "state", STATES, allocation)
    write_matrix(RESULTS / "convergence_feasibility_heterogeneous_v2.csv", "state", STATES, feasibility)
    write_matrix(RESULTS / "convergence_cost_heterogeneous_v2.csv", "state", STATES, costs)
    with (RESULTS / "convergence_heterogeneous_summary_v2.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["metric", "value"])
        writer.writerow(["budget", BUDGET])
        writer.writerow(["total_cost", spent])
        writer.writerow(["weighted_progress", progress])


if __name__ == "__main__":
    main()
