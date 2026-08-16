"""Empirical Twelve-State Capability Convergence analysis.

Consumes the dimension-specific recognition datasets and produces a complete
12 x 12 normalized capability matrix, State centroids, pairwise distances,
and convergence diagnostics. Missing observations are rejected rather than
implicitly treated as zero.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import csv
import math

STATES = [
    "United States", "Russia", "United Kingdom", "France", "China", "India",
    "Pakistan", "North Korea", "Israel", "Switzerland", "Belgium", "Taiwan"
]

CAPABILITIES = [
    "N", "M", "E", "F", "T", "I", "R", "H", "L", "D", "A", "S"
]

DIMENSION_FILES = {
    "N": "capability_recognition.csv",
    "M": "conventional_military_2025.csv",
    "E": "economic_production_2025.csv",
    "F": "financial_monetary_power_2026.csv",
    "T": "science_technology_2025.csv",
    "I": "advanced_industrial_capacity_2025.csv",
    "R": "energy_resource_security_2026.csv",
    "H": "food_water_humanitarian_resilience_2026.csv",
    "L": "infrastructure_logistics_2026.csv",
    "D": "diplomatic_institutional_power_2026.csv",
    "A": "information_cyber_ai_2026.csv",
    "S": "civilizational_social_resilience_2026.csv",
}


@dataclass(frozen=True)
class CapabilityMatrix:
    states: tuple[str, ...]
    capabilities: tuple[str, ...]
    recognition: tuple[tuple[int, ...], ...]
    normalized: tuple[tuple[float, ...], ...]

    @property
    def n_states(self) -> int:
        return len(self.states)

    @property
    def n_capabilities(self) -> int:
        return len(self.capabilities)


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _recognition_from_row(row: dict[str, str]) -> int | None:
    raw = row.get("R", "").strip()
    if raw == "":
        return None
    value = int(float(raw))
    if not 0 <= value <= 4:
        raise ValueError(f"Recognition level outside [0,4]: {value}")
    return value


def load_complete_matrix(data_dir: str | Path) -> CapabilityMatrix:
    """Load all twelve dimensions and fail loudly if any cell is absent."""
    data_dir = Path(data_dir)
    values: dict[tuple[str, str], int] = {}

    for capability in CAPABILITIES:
        path = data_dir / DIMENSION_FILES[capability]
        if not path.exists():
            raise FileNotFoundError(f"Missing dimension dataset: {path}")
        for row in _read_rows(path):
            state = row.get("state", "").strip()
            if state not in STATES:
                continue
            row_capability = row.get("capability_id", "").strip()
            if row_capability and int(row_capability) != CAPABILITIES.index(capability) + 1:
                continue
            recognition = _recognition_from_row(row)
            if recognition is None:
                continue
            key = (state, capability)
            if key in values:
                raise ValueError(f"Duplicate observation: {key}")
            values[key] = recognition

    missing = [(s, c) for s in STATES for c in CAPABILITIES if (s, c) not in values]
    if missing:
        raise ValueError(f"Incomplete capability matrix; missing {len(missing)} cells: {missing}")

    matrix = tuple(tuple(values[(s, c)] for c in CAPABILITIES) for s in STATES)
    normalized = tuple(tuple(v / 4.0 for v in row) for row in matrix)
    return CapabilityMatrix(tuple(STATES), tuple(CAPABILITIES), matrix, normalized)


def pairwise_euclidean(matrix: CapabilityMatrix) -> tuple[tuple[float, ...], ...]:
    x = matrix.normalized
    return tuple(
        tuple(math.sqrt(sum((a - b) ** 2 for a, b in zip(xi, xj))) for xj in x)
        for xi in x
    )


def centroid(matrix: CapabilityMatrix) -> tuple[float, ...]:
    return tuple(
        sum(row[j] for row in matrix.normalized) / matrix.n_states
        for j in range(matrix.n_capabilities)
    )


def state_centroid_distances(matrix: CapabilityMatrix) -> tuple[float, ...]:
    c = centroid(matrix)
    return tuple(math.sqrt(sum((v - cj) ** 2 for v, cj in zip(row, c))) for row in matrix.normalized)


def dimension_dispersion(matrix: CapabilityMatrix) -> tuple[float, ...]:
    result = []
    for j in range(matrix.n_capabilities):
        values = [row[j] for row in matrix.normalized]
        mean = sum(values) / len(values)
        result.append(math.sqrt(sum((v - mean) ** 2 for v in values) / len(values)))
    return tuple(result)


def global_dispersion(matrix: CapabilityMatrix) -> float:
    dispersions = dimension_dispersion(matrix)
    return math.sqrt(sum(d * d for d in dispersions) / len(dispersions))


def ideal_corridor_gap(matrix: CapabilityMatrix, lower: float = 0.75, upper: float = 1.0) -> tuple[float, ...]:
    """Mean L2 distance of each State to the capability corridor [lower, upper]."""
    gaps = []
    for row in matrix.normalized:
        squared = 0.0
        for value in row:
            if value < lower:
                squared += (lower - value) ** 2
            elif value > upper:
                squared += (value - upper) ** 2
        gaps.append(math.sqrt(squared))
    return tuple(gaps)


def convergence_index(matrix: CapabilityMatrix) -> float:
    """Map global dispersion to [0,1], where 1 denotes perfect convergence."""
    # Maximum cross-sectional standard deviation for variables in [0,1] is 0.5.
    return max(0.0, 1.0 - global_dispersion(matrix) / 0.5)


def write_matrix_csv(matrix: CapabilityMatrix, path: str | Path) -> None:
    path = Path(path)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["state", *matrix.capabilities])
        writer.writerows([[state, *row] for state, row in zip(matrix.states, matrix.recognition)])


def write_distance_csv(matrix: CapabilityMatrix, path: str | Path) -> None:
    distances = pairwise_euclidean(matrix)
    path = Path(path)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["state", *matrix.states])
        writer.writerows([[state, *row] for state, row in zip(matrix.states, distances)])
