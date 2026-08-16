"""Evidence-adjusted Twelve-State Capability Convergence estimator v2.

The v2 estimator separates two concepts that must not be conflated:

1. latent capability, constructed from R/4 and the available Q, P, U, D fields;
2. evidence confidence, used as an observation weight in convergence statistics.

Confidence therefore cannot mechanically turn an uncertain capability into a
low capability. This prevents epistemic uncertainty from becoming a substantive
capability penalty.
"""
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
                raise ValueError(f"Field {name} outside [0,1]: {value}")
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


def _confidence(row: dict[str, str]) -> float:
    value = _float(row, "evidence_confidence", "confidence")
    return 1.0 if value is None else value


def _latent_factor(row: dict[str, str], strict: bool) -> tuple[float, int]:
    """Geometric mean of R/4 plus supplied Q/P/U/D latent components."""
    fields = [
        _recognition(row),
        _float(row, "Q", "provisional_Q"),
        _float(row, "P", "provisional_P"),
        _float(row, "U", "provisional_U"),
        _float(row, "D", "provisional_D"),
    ]
    available = [x for x in fields if x is not None]
    if strict and len(available) != 5:
        raise ValueError("Strict v2 estimation requires R, Q, P, U and D")
    if not available:
        raise ValueError("No capability fields available")
    return math.prod(available) ** (1.0 / len(available)), len(available)


def load_evidence_adjusted_matrix(data_dir: str | Path, strict: bool = False):
    """Return states, capabilities, latent scores, confidence weights and coverage."""
    data_dir = Path(data_dir)
    values: dict[tuple[str, str], float] = {}
    weights: dict[tuple[str, str], float] = {}
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
            recognition = _recognition(row)
            if recognition is None:
                continue
            score, n = _latent_factor(row, strict)
            key = (state, capability)
            if key in values:
                raise ValueError(f"Duplicate observation: {key}")
            values[key] = score
            weights[key] = _confidence(row)
            coverage[key] = n
    missing = [(s, c) for s in STATES for c in CAPABILITIES if (s, c) not in values]
    if missing:
        raise ValueError(f"Incomplete v2 matrix; missing {len(missing)} cells: {missing}")
    scores = tuple(tuple(values[(s, c)] for c in CAPABILITIES) for s in STATES)
    confidence = tuple(tuple(weights[(s, c)] for c in CAPABILITIES) for s in STATES)
    cov = tuple(tuple(coverage[(s, c)] for c in CAPABILITIES) for s in STATES)
    return tuple(STATES), tuple(CAPABILITIES), scores, confidence, cov


def pairwise_euclidean(scores):
    return tuple(tuple(math.sqrt(sum((a-b)**2 for a,b in zip(xi,xj))) for xj in scores) for xi in scores)


def weighted_dimension_dispersion(scores, confidence):
    k = len(scores[0])
    out = []
    for j in range(k):
        vals = [scores[i][j] for i in range(len(scores))]
        ws = [confidence[i][j] for i in range(len(scores))]
        total = sum(ws)
        mean = sum(w*v for w, v in zip(ws, vals)) / total
        out.append(math.sqrt(sum(w*(v-mean)**2 for w, v in zip(ws, vals)) / total))
    return tuple(out)


def global_dispersion(scores, confidence):
    d = weighted_dimension_dispersion(scores, confidence)
    return math.sqrt(sum(x*x for x in d) / len(d))


def convergence_index(scores, confidence):
    return max(0.0, 1.0 - global_dispersion(scores, confidence) / 0.5)


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
