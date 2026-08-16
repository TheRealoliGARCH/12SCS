"""Empirical Twelve-State Capability Convergence analysis."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import math

STATES = [
    "United States", "Russia", "United Kingdom", "France", "China", "India",
    "Pakistan", "North Korea", "Israel", "Switzerland", "Belgium", "Taiwan"
]
CAPABILITIES = ["N", "M", "E", "F", "T", "I", "R", "H", "L", "D", "A", "S"]
DIMENSION_FILES = {
    "N": "nuclear_strategic_deterrence_2026.csv",
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
    if not raw:
        return None
    value = int(float(raw))
    if not 0 <= value <= 4:
        raise ValueError(f"Recognition level outside [0,4]: {value}")
    return value


def load_complete_matrix(data_dir: str | Path) -> CapabilityMatrix:
    """Load all twelve dimensions and reject any missing or duplicate cell."""
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
            if row.get("capability_id", "").strip():
                expected = CAPABILITIES.index(capability) + 1
                if int(row["capability_id"]) != expected:
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
    recognition = tuple(tuple(values[(s, c)] for c in CAPABILITIES) for s in STATES)
    normalized = tuple(tuple(v / 4.0 for v in row) for row in recognition)
    return CapabilityMatrix(tuple(STATES), tuple(CAPABILITIES), recognition, normalized)


def pairwise_euclidean(matrix: CapabilityMatrix) -> tuple[tuple[float, ...], ...]:
    return tuple(tuple(math.sqrt(sum((a-b)**2 for a,b in zip(xi,xj))) for xj in matrix.normalized) for xi in matrix.normalized)


def centroid(matrix: CapabilityMatrix) -> tuple[float, ...]:
    return tuple(sum(row[j] for row in matrix.normalized) / matrix.n_states for j in range(matrix.n_capabilities))


def state_centroid_distances(matrix: CapabilityMatrix) -> tuple[float, ...]:
    c = centroid(matrix)
    return tuple(math.sqrt(sum((v-cj)**2 for v,cj in zip(row,c))) for row in matrix.normalized)


def dimension_dispersion(matrix: CapabilityMatrix) -> tuple[float, ...]:
    out = []
    for j in range(matrix.n_capabilities):
        values = [row[j] for row in matrix.normalized]
        mean = sum(values) / len(values)
        out.append(math.sqrt(sum((v-mean)**2 for v in values) / len(values)))
    return tuple(out)


def global_dispersion(matrix: CapabilityMatrix) -> float:
    d = dimension_dispersion(matrix)
    return math.sqrt(sum(x*x for x in d) / len(d))


def convergence_index(matrix: CapabilityMatrix) -> float:
    """Normalized convergence index: 1 = perfect cross-State convergence."""
    return max(0.0, min(1.0, 1.0 - global_dispersion(matrix) / 0.5))


def ideal_corridor_gap(matrix: CapabilityMatrix, lower: float = 0.75) -> tuple[float, ...]:
    gaps = []
    for row in matrix.normalized:
        gaps.append(math.sqrt(sum(max(lower-v, 0.0)**2 for v in row)))
    return tuple(gaps)


def write_matrix_csv(matrix: CapabilityMatrix, path: str | Path) -> None:
    with Path(path).open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["state", *matrix.capabilities])
        writer.writerows([[s, *row] for s,row in zip(matrix.states, matrix.recognition)])


def write_distance_csv(matrix: CapabilityMatrix, path: str | Path) -> None:
    distances = pairwise_euclidean(matrix)
    with Path(path).open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["state", *matrix.states])
        writer.writerows([[s, *row] for s,row in zip(matrix.states, distances)])
