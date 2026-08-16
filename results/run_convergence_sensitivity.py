"""Run a fine-grid comparative-statics sensitivity analysis."""
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
HETEROGENEITY_LEVELS = tuple(i / 20.0 for i in range(21))
BASELINE_PROGRESS = 0.1220059357126264
TOL = 1e-12


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
        if spent > BUDGET + TOL:
            raise AssertionError("sensitivity allocation exceeds budget")
        for i in range(len(STATES)):
            for j in range(len(CAPABILITIES)):
                cap = positive[i][j] * feasibility[i][j]
                if allocation[i][j] < -TOL or allocation[i][j] > cap + TOL:
                    raise AssertionError("sensitivity allocation violates feasibility cap")
        rows.append((level, spent, progress, progress / BASELINE_PROGRESS))

    if abs(rows[0][2] - BASELINE_PROGRESS) > TOL:
        raise AssertionError("level-zero sensitivity baseline changed")

    progresses = [row[2] for row in rows]
    monotone = all(progresses[i + 1] <= progresses[i] + TOL for i in range(len(progresses) - 1))
    first_differences = [progresses[i + 1] - progresses[i] for i in range(len(progresses) - 1)]
    second_differences = [first_differences[i + 1] - first_differences[i] for i in range(len(first_differences) - 1)]
    nondecreasing_slopes = all(x >= -TOL for x in second_differences)
    nonincreasing_slopes = all(x <= TOL for x in second_differences)
    if nondecreasing_slopes and not nonincreasing_slopes:
        curvature = "convex"
    elif nonincreasing_slopes and not nondecreasing_slopes:
        curvature = "concave"
    elif nondecreasing_slopes and nonincreasing_slopes:
        curvature = "linear"
    else:
        curvature = "neither"

    with (RESULTS / "convergence_sensitivity_summary_v2.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["heterogeneity_level", "total_cost", "weighted_progress", "normalized_progress"])
        writer.writerows(rows)

    with (RESULTS / "convergence_sensitivity_characterization_v2.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["metric", "value"])
        writer.writerow(["grid_points", len(rows)])
        writer.writerow(["baseline_progress", progresses[0]])
        writer.writerow(["terminal_progress", progresses[-1]])
        writer.writerow(["terminal_normalized_progress", progresses[-1] / progresses[0]])
        writer.writerow(["monotone_nonincreasing", int(monotone)])
        writer.writerow(["minimum_first_difference", min(first_differences)])
        writer.writerow(["maximum_first_difference", max(first_differences)])
        writer.writerow(["minimum_second_difference", min(second_differences)])
        writer.writerow(["maximum_second_difference", max(second_differences)])
        writer.writerow(["curvature_classification", curvature])


if __name__ == "__main__":
    main()
