"""Run a transparent unit-feasibility constrained-convergence baseline on V2 outputs.

The baseline is diagnostic only: kappa_ij = 1, c_ij = 1, and B = 1.
It does not prescribe or encode any real-world capability-transfer mechanism.
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
    if not path.exists():
        raise FileNotFoundError(f"Required input not found: {path}")
    with path.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    if len(rows) != len(CAPABILITIES) + 1:
        raise ValueError(f"Expected {len(CAPABILITIES)} data rows in {path}")
    return tuple(float(row[1]) for row in rows[1:])


def read_matrix(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Required input not found: {path}")
    with path.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    if len(rows) != len(STATES) + 1:
        raise ValueError(f"Expected {len(STATES)} data rows in {path}")
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
    with (RESULTS / "convergence_baseline_summary_v2.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["metric", "value"])
        writer.writerow(["budget", BUDGET])
        writer.writerow(["total_cost", spent])
        writer.writerow(["weighted_progress", progress])


if __name__ == "__main__":
    main()
