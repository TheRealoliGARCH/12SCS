"""Verify structural integrity of a completed v2 result set."""
from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
STATES = [
    "United States", "Russia", "United Kingdom", "France", "China", "India",
    "Pakistan", "North Korea", "Israel", "Switzerland", "Belgium", "Taiwan"
]
CAPABILITIES = ["N", "M", "E", "F", "T", "I", "R", "H", "L", "D", "A", "S"]


def read_csv(name: str):
    path = RESULTS / name
    if not path.is_file():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.reader(fh))


def verify_matrix(name: str) -> None:
    rows = read_csv(name)
    if len(rows) != 13:
        raise AssertionError(f"{name}: expected 13 rows, found {len(rows)}")
    if rows[0] != ["state", *CAPABILITIES] and name == "capability_latent_matrix_v2.csv":
        raise AssertionError(f"{name}: unexpected header")
    states = [row[0] for row in rows[1:]]
    if states != STATES:
        raise AssertionError(f"{name}: unexpected State ordering")
    if any(len(row) != 13 for row in rows):
        raise AssertionError(f"{name}: malformed row length")
    for row in rows[1:]:
        for value in row[1:]:
            x = float(value)
            if not math.isfinite(x):
                raise AssertionError(f"{name}: non-finite value")


def verify_distance() -> None:
    rows = read_csv("capability_distance_matrix_v2.csv")
    if rows[0] != ["state", *STATES]:
        raise AssertionError("distance matrix header mismatch")
    matrix = [[float(x) for x in row[1:]] for row in rows[1:]]
    for i in range(12):
        if abs(matrix[i][i]) > 1e-12:
            raise AssertionError("distance diagonal is not zero")
        for j in range(12):
            if abs(matrix[i][j] - matrix[j][i]) > 1e-12:
                raise AssertionError("distance matrix is not symmetric")


def main() -> None:
    verify_matrix("capability_latent_matrix_v2.csv")
    verify_matrix("capability_confidence_matrix_v2.csv")
    verify_matrix("capability_coverage_v2.csv")
    verify_distance()
    diagnostics = read_csv("capability_convergence_diagnostics_v2.csv")
    if not diagnostics or diagnostics[0] != ["metric", "value"]:
        raise AssertionError("diagnostics header mismatch")
    metrics = {row[0]: float(row[1]) for row in diagnostics[1:]}
    if metrics.get("n_states") != 12 or metrics.get("n_capabilities") != 12:
        raise AssertionError("diagnostics do not report a 12 x 12 system")
    print("PASS: 144-cell v2 output structure and distance-matrix invariants verified.")


if __name__ == "__main__":
    main()
