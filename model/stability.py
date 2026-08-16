"""Systemic stability and local dynamics."""

from __future__ import annotations

import numpy as np


def stability_margin(A):
    """SM = 1 - spectral radius(A)."""
    A = np.asarray(A, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A must be square")
    rho = float(np.max(np.abs(np.linalg.eigvals(A))))
    return 1.0 - rho


def systemic_stability(adequacy, convergence, resilience, substitution,
                       diplomacy, concentration, nuclear_risk, weights=None):
    """Weighted SSI from the frozen specification."""
    x = np.asarray([
        adequacy, convergence, resilience, substitution,
        diplomacy, concentration, nuclear_risk
    ], dtype=float)
    if np.any((x < 0) | (x > 1)):
        raise ValueError("all normalized SSI components must lie in [0,1]")
    w = np.asarray(weights if weights is not None else np.ones(7) / 7, dtype=float)
    if w.shape != (7,) or np.any(w < 0) or w.sum() <= 0:
        raise ValueError("weights must be a non-negative length-7 vector")
    w = w / w.sum()
    return float(np.dot(w[:5], x[:5]) - w[5] * x[5] - w[6] * x[6])
