"""Convergence mechanism and safety coefficients for 12SCCM.

This module separates measured capability deficits from intervention
feasibility.  A feasibility coefficient is an abstract policy-model input;
it does not prescribe a particular transfer mechanism or sensitive
technology.
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


def validate_feasibility(feasibility: Matrix, shape: tuple[int, int] | None = None) -> tuple[tuple[float, ...], ...]:
    """Validate an abstract mechanism/safety coefficient matrix K in [0,1]."""
    n, k = _shape(feasibility)
    if shape is not None and (n, k) != shape:
        raise ValueError("feasibility matrix has the wrong shape")
    out = tuple(tuple(float(x) for x in row) for row in feasibility)
    if any(x < 0.0 or x > 1.0 for row in out for x in row):
        raise ValueError("feasibility coefficients must lie in [0,1]")
    return out


def effective_priority(positive_gaps: Matrix, capability_weights: Sequence[float], feasibility: Matrix) -> tuple[tuple[float, ...], ...]:
    """Apply K to positive gaps: P*_ij = G+_ij * omega_j * kappa_ij."""
    n, k = _shape(positive_gaps)
    if len(capability_weights) != k:
        raise ValueError("capability_weights length mismatch")
    omega = tuple(float(x) for x in capability_weights)
    if any(x < 0.0 for x in omega):
        raise ValueError("capability weights must be non-negative")
    if fsum(omega) <= 0.0:
        raise ValueError("capability weights must have positive total")
    kappa = validate_feasibility(feasibility, (n, k))
    return tuple(
        tuple(float(positive_gaps[i][j]) * omega[j] * kappa[i][j] for j in range(k))
        for i in range(n)
    )


def feasibility_complement(feasibility: Matrix) -> tuple[tuple[float, ...], ...]:
    """Return 1-K, representing the residual constraint on an intervention."""
    kappa = validate_feasibility(feasibility)
    return tuple(tuple(1.0 - x for x in row) for row in kappa)
