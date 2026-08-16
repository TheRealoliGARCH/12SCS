"""Evidence-adjusted Twelve-State Capability Convergence estimator v2."""
from __future__ import annotations

from pathlib import Path
import csv
import math

from model.convergence_analysis import CAPABILITIES, DIMENSION_FILES, STATES


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _float(row: dict[str, str], *names: str) -> float | None:
    for name in names:
        raw = row.get(name, "")
        if raw is not None and str(raw).strip():
            value = float(raw)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"Latent field {name} outside [0,1]: {value}")
            return value
    return None


def _recognition(row: dict[str, str]) -> float | None:
    raw = row.get("R", "").strip() or row.get("recognition_level", "").strip()
    if not raw:
        return None
    value = float(raw)
    if not 0.0 <= value <= 4.0:
        raise ValueError(f"Recognition level outside [0,4]: {value}")
    return value / 4.0


def _confidence(row: dict[str, str]) -> float | None:
    return _float(row, "evidence_confidence", "confidence")


def _latent_factor(row: dict[str, str], strict: bool) -> tuple[float, int]:
    fields = [
        _float(row, "Q", "provisional_Q"),
        _float(row, "P", "provisional_P"),
        _float(row, "U", "provisional_U"),
        _float(row, "D", "provisional_D"),
        _confidence(row),
    ]
    available = [x for x in fields if x is not None]
    if strict and len(available) != 5:
        raise ValueError("Strict v2 estimation requires Q, P, U, D and evidence confidence")
    if not available:
        raise ValueError("No latent/evidence fields available")
    return math.prod(available) ** (1.0 / len(available)), len(available)


def load_evidence_adjusted_matrix(data_dir: str | Path, strict: bool = False):
    data_dir = Path(data_dir)
    values: dict[tuple[str, str], float] = {}
    coverage: dict[tuple[str, str], int] = {}
    for capability in CAPABILITIES:
        path = data_dir / DIMENSION_FILES[capability]
        if not path.exists():
            raise FileNotFoundError(path)
        expected_id = CAPABILITIES.index(capability) + 1
        for row in _read_rows(path):
            state = row.get("state", "").strip()
            if state not in STATES:
                continue
            cap_id = row.get("capability_id", "").strip()
            if cap_id and int(cap_id) != expected_id:
                continue
            r = _recognition(row)
            if r is None:
                continue
            factor, n = _latent_factor(row, strict)
            key = (state, capability)
            if key in values:
                raise ValueError(f"Duplicate observation: {key}")
            values[key] = r * factor
            coverage[key] = n
    missing = [(s, c) for s in STATES for c in CAPABILITIES if (s, c) not in values]
    if missing:
        raise ValueError(f"Incomplete v2 matrix; missing {len(missing)} cells: {missing}")
    scores = tuple(tuple(values[(s, c)] for c in CAPABILITIES) for s in STATES)
    cov = tuple(tuple(coverage[(s, c)] for c in CAPABILITIES) for s in STATES)
    return tuple(STATES), tuple(CAPABILITIES), scores, cov


def pairwise_euclidean(scores):
    return tuple(tuple(math.sqrt(sum((a-b)**2 for a,b in zip(xi,xj))) for xj in scores) for xi in scores)


def dimension_dispersion(scores):
    n = len(scores)
    k = len(scores[0])
    out = []
    for j in range(k):
        values = [row[j] for row in scores]
        mean = sum(values) / n
        out.append(math.sqrt(sum((v-mean)**2 for v in values) / n))
    return tuple(out)


def global_dispersion(scores):
    d = dimension_dispersion(scores)
    return math.sqrt(sum(x*x for x in d) / len(d))


def convergence_index(scores):
    return max(0.0, 1.0 - global_dispersion(scores) / 0.5)


def write_matrix_csv(states, capabilities, scores, path: str | Path) -> None:
    with Path(path).open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["state", *capabilities])
        writer.writerows([[s, *row] for s, row in zip(states, scores)])


def write_distance_csv(states, distances, path: str | Path) -> None:
    with Path(path).open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["state", *states])
        writer.writerows([[s, *row] for s, row in zip(states, distances)])
