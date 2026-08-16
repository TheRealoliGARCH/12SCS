"""Peaceful nuclear participation model.

This module deliberately models only lawful peaceful cooperation, qualification,
verification, safety/security, compliance and participation. It contains no
weapons-transfer or weapons-construction model.
"""

from __future__ import annotations

import numpy as np


def eligibility_gate(gates):
    """G = product of mandatory binary eligibility gates."""
    g = np.asarray(gates, dtype=int)
    if np.any((g != 0) & (g != 1)):
        raise ValueError("eligibility gates must be binary")
    return int(np.prod(g))


def peaceful_qualification(Q, V, C, S, D, exponents=None):
    """q_N = Q^a V^b C^c S^d D^e."""
    x = np.asarray([Q, V, C, S, D], dtype=float)
    if np.any((x < 0) | (x > 1)):
        raise ValueError("nuclear qualification inputs must lie in [0,1]")
    a = np.ones(5) if exponents is None else np.asarray(exponents, dtype=float)
    if a.shape != (5,) or np.any(a < 0):
        raise ValueError("exponents must be a non-negative vector of length 5")
    return float(np.prod(x ** a))


def peaceful_transfer(qualification, gate, scale=1.0):
    """Conceptual peaceful cooperation intensity T_N = G * scale * q_N."""
    if not 0 <= qualification <= 1 or gate not in (0, 1) or scale < 0:
        raise ValueError("invalid peaceful-transfer inputs")
    return float(gate * scale * qualification)


def participation_surplus(benefit_peaceful, benefit_other, compliance_cost, outside_utility):
    """Omega = U_join - U_outside."""
    return float(benefit_peaceful + benefit_other - compliance_cost - outside_utility)
