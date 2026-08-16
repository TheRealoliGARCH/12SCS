"""Capability adequacy and convergence metrics."""

from __future__ import annotations

import numpy as np


def capability_deficit(r, floors):
    """CD = sum_ij w_j max(0, L_j-r_ij), using unit state weights."""
    R = np.asarray(r, dtype=float)
    L = np.asarray(floors, dtype=float)
    if R.ndim != 2 or L.shape != (R.shape[1],):
        raise ValueError("r must be state x capability and floors capability-sized")
    return np.maximum(0.0, L[None, :] - R).sum()


def dispersion(r, weights=None):
    """Sigma_R = sum_j w_j std_i(r_ij)."""
    R = np.asarray(r, dtype=float)
    if R.ndim != 2:
        raise ValueError("r must be a state x capability matrix")
    if weights is None:
        w = np.full(R.shape[1], 1.0 / R.shape[1])
    else:
        w = np.asarray(weights, dtype=float)
        if w.shape != (R.shape[1],) or np.any(w < 0) or w.sum() <= 0:
            raise ValueError("weights must be non-negative and capability-sized")
        w = w / w.sum()
    return float(np.dot(w, R.std(axis=0)))


def convergence_distance(r, target, tolerance):
    """Distance outside an ideal capability corridor."""
    R = np.asarray(r, dtype=float)
    target = np.asarray(target, dtype=float)
    tol = np.asarray(tolerance, dtype=float)
    if R.ndim != 2 or target.shape != tol.shape or target.shape != (R.shape[1],):
        raise ValueError("target and tolerance must be capability-sized")
    if np.any(tol < 0):
        raise ValueError("tolerance must be non-negative")
    excess = np.maximum(0.0, np.abs(R - target[None, :]) - tol[None, :])
    return float(np.mean(np.sqrt((excess ** 2).sum(axis=1))))
