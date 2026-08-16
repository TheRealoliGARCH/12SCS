"""Run a transparent baseline constrained-convergence allocation on V2 outputs.

This scenario is deliberately diagnostic rather than a policy prescription:
all feasibility coefficients are set to one, all intervention costs are set
to one, and the budget is one normalized cost unit. It therefore measures the
allocator's upper-bound ranking behavior without asserting that any particular
real-world transfer is safe, feasible, or desirable.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from model.convergence_analysis import CAPABILITIES, STATES
from model.convergence_optimization import allocate_budget, total_cost, weighted_progress

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


def write_matrix(path: Path, matrix) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["state", *CAPABILITIES])
        writer.writerows([[state, *row] for state, row in zip(STATES, matrix)])


def main() -> None:
    positive = read_matrix(RESULTS / "capability_gap_positive_v2.csv")
    weights = read_vector(RESULTS / "capability_dispersion_weights_v2.csv")
    feasibility = tuple(tuple(1.0 for _ in CAPABILITIES) for _ in STATES)
    costs = tuple(tuple(1.0 for _ in CAPABILITIES) for _ in STATES)

    allocation = allocate_budget(positive, weights, feasibility, costs, BUDGET)
    spent = total_cost(allocation, costs)
    progress = weighted_progress(allocation, weights)

    if spent > BUDGET + 1e-12:
        raise AssertionError("baseline allocation exceeds budget")
    for i in range(len(STATES)):
        for j in range(len(CAPABILITIES)):
            cap = positive[i][j] * feasibility[i][j]
            if allocation[i][j] < -1e-12 or allocation[i][j] > cap + 1e-12:
                raise AssertionError("baseline allocation violates feasibility cap")

    write_matrix(RESULTS / "convergence_allocation_baseline_v2.csv", allocation)
    with (RESULTS / "convergence_baseline_summary_v2.csv").open(
        "w", encoding="utf-8", newline=""
    ) as fh:
        writer = csv.writer(fh)
        writer.writerow(["metric", "value"])
        writer.writerow(["budget", BUDGET])
        writer.writerow(["total_cost", spent])
        writer.writerow(["weighted_progress", progress])


if __name__ == "__main__":
    main()
