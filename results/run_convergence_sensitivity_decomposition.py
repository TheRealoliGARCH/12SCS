"""Decompose convergence sensitivity into feasibility-only, cost-only, and joint effects."""
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
LEVELS = tuple(i / 20.0 for i in range(21))
TOL = 1e-12


def read_vector(path: Path):
    with path.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    return tuple(float(row[1]) for row in rows[1:])


def read_matrix(path: Path):
    with path.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    return tuple(tuple(float(x) for x in row[1:]) for row in rows[1:])


def blend(base, level, homogeneous):
    return tuple(
        tuple((1.0 - level) * homogeneous + level * float(x) for x in row)
        for row in base
    )


def evaluate(positive, weights, feasibility, costs):
    allocation = allocate_budget(positive, weights, feasibility, costs, BUDGET)
    spent = total_cost(allocation, costs)
    progress = weighted_progress(allocation, weights)
    if spent > BUDGET + TOL:
        raise AssertionError("allocation exceeds budget")
    for i in range(len(STATES)):
        for j in range(len(CAPABILITIES)):
            cap = positive[i][j] * feasibility[i][j]
            if allocation[i][j] < -TOL or allocation[i][j] > cap + TOL:
                raise AssertionError("allocation violates feasibility cap")
    return spent, progress


def monotone(values):
    return all(values[i + 1] <= values[i] + TOL for i in range(len(values) - 1))


def main() -> None:
    positive = read_matrix(RESULTS / "capability_gap_positive_v2.csv")
    weights = read_vector(RESULTS / "capability_dispersion_weights_v2.csv")
    feasibility_base, costs_base = build_scenario(STATES, CAPABILITIES)

    scenarios = {
        "feasibility_only": (True, False),
        "cost_only": (False, True),
        "joint": (True, True),
    }
    outputs = {}
    for name, (vary_feasibility, vary_costs) in scenarios.items():
        rows = []
        for level in LEVELS:
            feasibility = blend(feasibility_base, level, 1.0) if vary_feasibility else tuple(tuple(1.0 for _ in row) for row in positive)
            costs = blend(costs_base, level, 1.0) if vary_costs else tuple(tuple(1.0 for _ in row) for row in positive)
            spent, progress = evaluate(positive, weights, feasibility, costs)
            rows.append((level, spent, progress))
        outputs[name] = rows

    baseline = outputs["joint"][0][2]
    with (RESULTS / "convergence_sensitivity_decomposition_v2.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["heterogeneity_level", "feasibility_only", "cost_only", "joint", "feasibility_normalized", "cost_normalized", "joint_normalized"])
        for i, level in enumerate(LEVELS):
            vf = outputs["feasibility_only"][i][2]
            vc = outputs["cost_only"][i][2]
            vj = outputs["joint"][i][2]
            writer.writerow([level, vf, vc, vj, vf / baseline, vc / baseline, vj / baseline])

    with (RESULTS / "convergence_sensitivity_decomposition_characterization_v2.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["metric", "value"])
        for name, rows in outputs.items():
            values = [row[2] for row in rows]
            writer.writerow([f"{name}_baseline", values[0]])
            writer.writerow([f"{name}_terminal", values[-1]])
            writer.writerow([f"{name}_terminal_normalized", values[-1] / baseline])
            writer.writerow([f"{name}_monotone_nonincreasing", int(monotone(values))])
        writer.writerow(["joint_gap_to_feasibility_only_terminal", outputs["joint"][ -1][2] - outputs["feasibility_only"][ -1][2]])
        writer.writerow(["joint_gap_to_cost_only_terminal", outputs["joint"][ -1][2] - outputs["cost_only"][ -1][2]])


if __name__ == "__main__":
    main()
