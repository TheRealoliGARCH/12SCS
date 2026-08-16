"""Capability-gap and convergence-priority functions for 12SCCM v2.

The module turns the verified latent capability matrix into signed gaps,
positive deficits, dispersion-based capability weights, and State/capability
priority scores. It deliberately does not prescribe capability-transfer
mechanisms.
"""
from __future__ import annotations

from math import fsum
from typing import Sequence

Matrix = Sequence[Sequence[float]]


def _shape(x: Matrix) -> tuple[int, int]:
    rows = len(x)
    cols = len(x[0]) if rows else 0
    if rows == 0 or cols == 0 or any(len(row) != cols for row in x):
        raise ValueError("matrix must be non-empty and rectangular")
    return rows, cols


def weighted_benchmark(scores: Matrix, confidence: Matrix) -> tuple[float, ...]:
    """Compute the confidence-weighted benchmark for each capability."""
    n, k = _shape(scores)
    if _shape(confidence) != (n, k):
        raise ValueError("scores and confidence must have identical shapes")
    out = []
    for j in range(k):
        weights = [float(confidence[i][j]) for i in range(n)]
        if any(w < 0 for w in weights) or fsum(weights) <= 0:
            raise ValueError("confidence weights must be non-negative with positive column totals")
        out.append(fsum(weights[i] * float(scores[i][j]) for i in range(n)) / fsum(weights))
    return tuple(out)


def signed_gap(scores: Matrix, benchmark: Sequence[float]) -> tuple[tuple[float, ...], ...]:
    """Return G_ij = benchmark_j - x_ij."""
    n, k = _shape(scores)
    if len(benchmark) != k:
        raise ValueError("benchmark length must equal the number of capabilities")
    return tuple(tuple(float(benchmark[j]) - float(scores[i][j]) for j in range(k)) for i in range(n))


def positive_gap(gaps: Matrix) -> tuple[tuple[float, ...], ...]:
    """Return G^+_ij = max(G_ij, 0)."""
    n, k = _shape(gaps)
    return tuple(tuple(max(float(gaps[i][j]), 0.0) for j in range(k)) for i in range(n))


def dispersion_weights(dispersions: Sequence[float]) -> tuple[float, ...]:
    """Normalize non-negative capability dispersions into systemic weights."""
    if not dispersions:
        raise ValueError("dispersions must be non-empty")
    values = tuple(float(x) for x in dispersions)
    if any(x < 0 for x in values):
        raise ValueError("dispersions must be non-negative")
    total = fsum(values)
    if total <= 0:
        return tuple(1.0 / len(values) for _ in values)
    return tuple(x / total for x in values)


def convergence_priority(
    positive_gaps: Matrix,
    capability_weights: Sequence[float],
    feasibility: Matrix | None = None,
) -> tuple[tuple[float, ...], ...]:
    """Compute P_ij = G^+_ij * omega_j * kappa_ij."""
    n, k = _shape(positive_gaps)
    if len(capability_weights) != k:
        raise ValueError("capability_weights length mismatch")
    omega = tuple(float(x) for x in capability_weights)
    if any(x < 0 for x in omega):
        raise ValueError("capability weights must be non-negative")
    if feasibility is None:
        kappa = tuple(tuple(1.0 for _ in range(k)) for _ in range(n))
    else:
        if _shape(feasibility) != (n, k):
            raise ValueError("feasibility must match the gap matrix")
        kappa = tuple(tuple(float(x) for x in row) for row in feasibility)
        if any(x < 0 or x > 1 for row in kappa for x in row):
            raise ValueError("feasibility coefficients must lie in [0,1]")
    return tuple(
        tuple(float(positive_gaps[i][j]) * omega[j] * kappa[i][j] for j in range(k))
        for i in range(n)
    )


def state_priorities(priorities: Matrix) -> tuple[float, ...]:
    """Aggregate capability priorities by State."""
    return tuple(fsum(float(x) for x in row) for row in priorities)


def capability_priorities(priorities: Matrix) -> tuple[float, ...]:
    """Aggregate convergence priorities by capability."""
    n, k = _shape(priorities)
    return tuple(fsum(float(priorities[i][j]) for i in range(n)) for j in range(k))
