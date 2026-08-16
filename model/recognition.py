"""Recognition, evidence, uniqueness and concentration functions."""

from __future__ import annotations

import numpy as np


def recognition_intensity(Q, P, U, D):
    """Compute rho_ij = Q_ij P_ij U_ij D_ij, elementwise."""
    arrays = [np.asarray(x, dtype=float) for x in (Q, P, U, D)]
    shape = arrays[0].shape
    if any(x.shape != shape for x in arrays):
        raise ValueError("Q, P, U and D must have identical shapes")
    if any(np.any((x < 0) | (x > 1)) for x in arrays):
        raise ValueError("recognition components must lie in [0, 1]")
    return np.prod(arrays, axis=0)


def recognition_level(rho, thresholds=(0.2, 0.4, 0.7, 0.9)):
    """Map latent recognition intensity to Charter levels 0--4.

    Thresholds are explicit calibration parameters, not country observations.
    Level 0 is below the first threshold; Levels 1--4 occupy successive bands.
    """
    rho = np.asarray(rho, dtype=float)
    if np.any((rho < 0) | (rho > 1)):
        raise ValueError("rho must lie in [0, 1]")
    t = tuple(float(x) for x in thresholds)
    if len(t) != 4 or not (0 <= t[0] < t[1] < t[2] < t[3] <= 1):
        raise ValueError("thresholds must satisfy 0 <= t0 < t1 < t2 < t3 <= 1")
    return np.select(
        [rho < t[0], rho < t[1], rho < t[2], rho < t[3]],
        [0, 1, 2, 3],
        default=4,
    ).astype(int)


def demonstrated_capability(evidence):
    """Independent-evidence aggregator D = 1 - product(1-d_m)."""
    x = np.asarray(evidence, dtype=float)
    if np.any((x < 0) | (x > 1)):
        raise ValueError("evidence contributions must lie in [0, 1]")
    return 1.0 - np.prod(1.0 - x, axis=0)


def persistence(duration, rate):
    """P = 1 - exp(-lambda * duration)."""
    duration = np.asarray(duration, dtype=float)
    rate = np.asarray(rate, dtype=float)
    if np.any(duration < 0) or np.any(rate <= 0):
        raise ValueError("duration must be non-negative and rate positive")
    return 1.0 - np.exp(-rate * duration)


def uniqueness(capability, substitutability, epsilon=1e-12):
    """U_ij = 1 / (1 + sum_{k != i} s_ikj * normalized X_kj)."""
    X = np.asarray(capability, dtype=float)
    S = np.asarray(substitutability, dtype=float)
    if X.ndim != 2:
        raise ValueError("capability must be a state x capability matrix")
    if S.shape != (X.shape[0], X.shape[0], X.shape[1]):
        raise ValueError("substitutability must have shape (states, states, capabilities)")
    if np.any(X < 0) or np.any((S < 0) | (S > 1)):
        raise ValueError("capability must be non-negative and substitutability in [0,1]")
    share = X / (X.sum(axis=0, keepdims=True) + epsilon)
    return 1.0 / (1.0 + np.einsum("ikj,kj->ij", S, share))


def concentration_index(R):
    """H_j = sum_i (R_ij / sum_i R_ij)^2 for each capability."""
    R = np.asarray(R, dtype=float)
    if R.ndim != 2:
        raise ValueError("R must be a state x capability matrix")
    totals = R.sum(axis=0)
    H = np.full(R.shape[1], np.nan, dtype=float)
    mask = totals > 0
    H[mask] = ((R[:, mask] / totals[mask]) ** 2).sum(axis=0)
    return H
