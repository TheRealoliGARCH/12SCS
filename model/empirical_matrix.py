"""Empirical 12SCCM matrix construction and convergence diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import math

import numpy as np


@dataclass(frozen=True)
class MatrixResult:
    """Normalized capability matrix and evidence coverage."""

    matrix: np.ndarray
    confidence: np.ndarray
    observed: np.ndarray


def _number(value: str | None) -> float:
    if value is None or value.strip() == "":
        return math.nan
    return float(value)


def load_dimension_csv(path: str | Path) -> list[dict]:
    """Read rows from one empirical dimension CSV."""
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_matrix(paths: list[str | Path], n_states: int = 12, n_capabilities: int = 12) -> MatrixResult:
    """Build an N x K matrix from supplied dimension-specific datasets.

    R is normalized from the Charter's 0--4 recognition scale to [0,1].
    Missing observations remain NaN; no implicit imputation is performed.
    Duplicate observations are rejected and require explicit adjudication.
    """
    matrix = np.full((n_states, n_capabilities), np.nan, dtype=float)
    confidence = np.full_like(matrix, np.nan)
    observed = np.zeros_like(matrix, dtype=bool)

    for path in paths:
        for row in load_dimension_csv(path):
            try:
                i = int(row["state_id"]) - 1
                j = int(row["capability_id"]) - 1
            except (KeyError, ValueError) as exc:
                raise ValueError(f"Invalid state/capability identifiers in {path}") from exc
            if not (0 <= i < n_states and 0 <= j < n_capabilities):
                raise ValueError(f"Out-of-range state/capability in {path}: {i + 1}, {j + 1}")
            raw_r = _number(row.get("R"))
            if math.isnan(raw_r):
                continue
            if not 0.0 <= raw_r <= 4.0:
                raise ValueError(f"R must lie in [0,4], got {raw_r} in {path}")
            if observed[i, j]:
                raise ValueError(f"Duplicate observation for state {i + 1}, capability {j + 1}")
            matrix[i, j] = raw_r / 4.0
            confidence[i, j] = _number(row.get("evidence_confidence"))
            observed[i, j] = True

    return MatrixResult(matrix, confidence, observed)


def pairwise_euclidean(matrix: np.ndarray) -> np.ndarray:
    """Pairwise Euclidean distances on complete capability vectors only."""
    X = np.asarray(matrix, dtype=float)
    if X.ndim != 2:
        raise ValueError("matrix must be two-dimensional")
    complete = np.all(np.isfinite(X), axis=1)
    distances = np.full((X.shape[0], X.shape[0]), np.nan, dtype=float)
    idx = np.flatnonzero(complete)
    if len(idx):
        Y = X[idx]
        diff = Y[:, None, :] - Y[None, :, :]
        distances[np.ix_(idx, idx)] = np.sqrt(np.sum(diff * diff, axis=2))
    return distances


def dispersion(matrix: np.ndarray) -> float:
    """Mean cross-sectional standard deviation across observed dimensions."""
    X = np.asarray(matrix, dtype=float)
    if X.ndim != 2:
        raise ValueError("matrix must be two-dimensional")
    dimension_sd = np.nanstd(X, axis=0)
    valid = np.isfinite(dimension_sd)
    return float(np.mean(dimension_sd[valid])) if np.any(valid) else math.nan


def centroid_distance(matrix: np.ndarray) -> np.ndarray:
    """Each State's distance from the observed capability centroid."""
    X = np.asarray(matrix, dtype=float)
    centroid = np.nanmean(X, axis=0)
    out = np.full(X.shape[0], np.nan, dtype=float)
    for i, row in enumerate(X):
        valid = np.isfinite(row) & np.isfinite(centroid)
        if np.any(valid):
            out[i] = float(np.sqrt(np.sum((row[valid] - centroid[valid]) ** 2)))
    return out


def corridor_gap(matrix: np.ndarray, target: np.ndarray, tolerance: np.ndarray) -> np.ndarray:
    """State-level distance outside an ideal capability corridor."""
    X = np.asarray(matrix, dtype=float)
    target = np.asarray(target, dtype=float)
    tolerance = np.asarray(tolerance, dtype=float)
    if X.ndim != 2 or target.shape != (X.shape[1],) or tolerance.shape != target.shape:
        raise ValueError("target and tolerance must match the capability dimension")
    if np.any(tolerance < 0):
        raise ValueError("tolerance must be non-negative")
    out = np.full(X.shape[0], np.nan, dtype=float)
    for i, row in enumerate(X):
        valid = np.isfinite(row) & np.isfinite(target)
        if np.any(valid):
            excess = np.maximum(0.0, np.abs(row[valid] - target[valid]) - tolerance[valid])
            out[i] = float(np.sqrt(np.sum(excess ** 2)))
    return out
