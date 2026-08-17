"""Capability-network functions."""

from __future__ import annotations

import numpy as np


def effective_dependency(dependency, substitutability):
    """P_eff = P * (1 - S)."""
    P = np.asarray(dependency, dtype=float)
    S = np.asarray(substitutability, dtype=float)
    if P.shape != S.shape:
        raise ValueError("dependency and substitutability must have identical shapes")
    if np.any((P < 0) | (P > 1)) or np.any((S < 0) | (S > 1)):
        raise ValueError("dependency and substitutability must lie in [0,1]")
    return P * (1.0 - S)


def systemic_criticality(functionality, leave_one_out):
    r"""K = [Phi(G)-Phi(G\{cell})] / Phi(G)."""
    phi = float(functionality)
    loo = np.asarray(leave_one_out, dtype=float)
    if phi <= 0:
        raise ValueError("baseline functionality must be positive")
    return (phi - loo) / phi


def vulnerability(criticality, effective_dependency, resilience):
    """V = K * P_eff * (1 - resilience)."""
    K = np.asarray(criticality, dtype=float)
    P = np.asarray(effective_dependency, dtype=float)
    R = np.asarray(resilience, dtype=float)
    if not (K.shape == P.shape == R.shape):
        raise ValueError("all vulnerability inputs must have identical shapes")
    if np.any(K < 0) or np.any((P < 0) | (P > 1)) or np.any((R < 0) | (R > 1)):
        raise ValueError("invalid criticality, dependency or resilience values")
    return K * P * (1.0 - R)
