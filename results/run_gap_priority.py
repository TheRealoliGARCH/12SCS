"""Generate the V2 capability-gap and convergence-priority outputs."""
from __future__ import annotations

import csv
from pathlib import Path

from model.capability_gap_priority import (
    capability_priorities,
    convergence_priority,
    dispersion_weights,
    positive_gap,
    signed_gap,
    state_priorities,
    weighted_benchmark,
)
from model.convergence_analysis import CAPABILITIES, STATES
from model.evidence_adjusted_convergence import weighted_dimension_dispersion

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def read_matrix(path: Path):
    with path.open("r", encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    if not rows or len(rows) != len(STATES) + 1:
        raise ValueError(f"Expected {len(STATES)} data rows in {path}")
    if rows[0][1:] != list(CAPABILITIES):
        raise ValueError(f"Capability header mismatch in {path}")
    states = [row[0] for row in rows[1:]]
    if states != list(STATES):
        raise ValueError(f"State ordering mismatch in {path}")
    return tuple(tuple(float(x) for x in row[1:]) for row in rows[1:])


def write_matrix(path: Path, row_label: str, headers, row_names, matrix):
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([row_label, *headers])
        writer.writerows([[name, *row] for name, row in zip(row_names, matrix)])


def write_vector(path: Path, label: str, headers, values):
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([label, "value"])
        writer.writerows([[name, value] for name, value in zip(headers, values)])


def main() -> None:
    scores = read_matrix(RESULTS / "capability_latent_matrix_v2.csv")
    confidence = read_matrix(RESULTS / "capability_confidence_matrix_v2.csv")
    dispersions = weighted_dimension_dispersion(scores, confidence)
    benchmark = weighted_benchmark(scores, confidence)
    gaps = signed_gap(scores, benchmark)
    positive = positive_gap(gaps)
    weights = dispersion_weights(dispersions)
    priorities = convergence_priority(positive, weights)

    write_vector(RESULTS / "capability_benchmark_v2.csv", "capability", CAPABILITIES, benchmark)
    write_matrix(RESULTS / "capability_gap_signed_v2.csv", "state", CAPABILITIES, STATES, gaps)
    write_matrix(RESULTS / "capability_gap_positive_v2.csv", "state", CAPABILITIES, STATES, positive)
    write_vector(RESULTS / "capability_dispersion_weights_v2.csv", "capability", CAPABILITIES, weights)
    write_matrix(RESULTS / "capability_priority_v2.csv", "state", CAPABILITIES, STATES, priorities)
    write_vector(RESULTS / "state_convergence_priority_v2.csv", "state", STATES, state_priorities(priorities))
    write_vector(RESULTS / "capability_convergence_priority_v2.csv", "capability", CAPABILITIES, capability_priorities(priorities))


if __name__ == "__main__":
    main()
