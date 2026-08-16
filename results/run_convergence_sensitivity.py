"""Run deterministic sensitivity analysis over abstract K and C heterogeneity."""
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
HETEROGENEITY_LEVELS = (0.0, 0.25, 0.50, 0.75, 1.0)


def read_vector(path: Path):
    with path.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    return tuple(float(row[1]) for row in rows[1:])


def read_matrix(path: Path):
    with path.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    return tuple(tuple(float(x) for x in row[1:]) for row in rows[1:])


def blend_matrix(base, level, homogeneous):
    return tuple(
        tuple((1.0 - level) * homogeneous + level * float(x) for x in row)
        for row in base
    )


def main() -> None:
    positive = read_matrix(RESULTS / "capability_gap_positive_v2.csv")
    weights = read_vector(RESULTS / "capability_dispersion_weights_v2.csv")
    feasibility_base, costs_base = build_scenario(STATES, CAPABILITIES)

    rows = []
    for level in HETEROGENEITY_LEVELS:
        feasibility = blend_matrix(feasibility_base, level, 1.0)
        costs = blend_matrix(costs_base, level, 1.0)
        allocation = allocate_budget(positive, weights, feasibility, costs, BUDGET)
        spent = total_cost(allocation, costs)
        progress = weighted_progress(allocation, weights)
        for i in range(len(STATES)):
            for j in range(len(CAPABILITIES)):
                cap = positive[i][j] * feasibility[i][j]
                if allocation[i][j] < -1e-12 or allocation[i][j] > cap + 1e-12:
                    raise AssertionError("sensitivity allocation violates feasibility cap")
        if spent > BUDGET + 1e-12:
            raise AssertionError("sensitivity allocation exceeds budget")
        rows.append((level, spent, progress))

    # At level zero the scenario is exactly the unit-feasibility/unit-cost case.
    if abs(rows[0][2] - 0.1220059357126264) > 1e-12:
        raise AssertionError("level-zero sensitivity baseline changed")

    with (RESULTS / "convergence_sensitivity_summary_v2.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["heterogeneity_level", "total_cost", "weighted_progress"])
        writer.writerows(rows)


if __name__ == "__main__":
    main()
