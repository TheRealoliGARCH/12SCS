"""Phase II symbolic primitive sign analysis for a fixed active-set regime.

The regime has binding cells i and at most one marginal cell m.  Write

    a_i = kappa_i^0 - 1,
    d_i = c_i^0 - 1,
    F   = d_m,

and let g_i be the positive gap, w_i the capability weight, and B0 the budget.
The exact rational progress function is

    Pi(lambda) = A + B lambda + (C + D lambda + E lambda^2)/(1 + F lambda),

with
    A = sum_i w_i g_i,
    B = sum_i w_i g_i a_i,
    C = B0 - sum_i g_i,
    D = -sum_i g_i(a_i+d_i),
    E = -sum_i g_i a_i d_i.

This module records the exact primitive forms of the derivative numerators.
A crucial correction to the earlier Phase-II draft is that the second derivative
numerator is CONSTANT: q1=q2=0 identically.  Thus q0+q1+q2=q0.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Cell:
    gap: float
    weight: float
    a: float
    d: float


@dataclass(frozen=True)
class PrimitiveMap:
    A: float
    B: float
    C: float
    D: float
    E: float
    F: float
    p0: float
    p1: float
    p2: float
    q0: float
    q1: float
    q2: float
    P1: float
    Q1: float


def derive(cells: Sequence[Cell], budget: float, marginal_d: float) -> PrimitiveMap:
    """Return exact coefficient-level quantities from primitive cell data."""
    A = sum(x.weight * x.gap for x in cells)
    B = sum(x.weight * x.gap * x.a for x in cells)
    C = budget - sum(x.gap for x in cells)
    D = -sum(x.gap * (x.a + x.d) for x in cells)
    E = -sum(x.gap * x.a * x.d for x in cells)
    F = marginal_d

    p0 = B + D - F * C
    S = B * F + E
    p1 = 2.0 * S
    p2 = F * S

    # Direct differentiation of P(lambda)/(1+F lambda)^2 gives
    # Pi''(lambda) = q0/(1+F lambda)^3.  All lambda-dependent terms cancel.
    q0 = 2.0 * (E - F * D + F * F * C)
    q1 = 0.0
    q2 = 0.0

    P1 = p0 + p1 + p2
    Q1 = q0 + q1 + q2
    return PrimitiveMap(A, B, C, D, E, F, p0, p1, p2, q0, q1, q2, P1, Q1)


def primitive_forms(cells: Sequence[Cell], budget: float, marginal_d: float) -> dict[str, str]:
    """Return human-readable exact primitive expressions used in Phase II."""
    # These strings are deliberately algebraic rather than calibration-specific.
    return {
        "p0": "sum_i g_i[w_i a_i - (a_i+d_i) + F] - F B0",
        "P1": (
            "sum_i g_i[w_i a_i(1+F)^2 "
            "- (a_i+d_i)(1+2F) - a_i d_i(2+F) + F] - F B0"
        ),
        "q0": "2[F^2 B0 - sum_i g_i(a_i-F)(d_i-F)]",
        "Q1": "2[F^2 B0 - sum_i g_i(a_i-F)(d_i-F)]",
        "q1": "0 identically",
        "q2": "0 identically",
    }


def sign_restrictions() -> dict[str, str]:
    """Return primitive restrictions and what they do (and do not) imply."""
    return {
        "denominator": "F > -1 implies 1+F lambda > 0 on [0,1]",
        "a": "kappa_i^0 in [0,1] implies -1 <= a_i <= 0",
        "d": "c_i^0 > 0 implies d_i > -1",
        "p0": "sign is not implied by the primitive box alone; p0 requires an additional inequality",
        "P1": "sign is not implied by the primitive box alone; P1 requires an additional inequality",
        "q0": "sign is equivalent to F^2 B0 >= sum_i g_i(a_i-F)(d_i-F) for q0 >= 0",
    }


if __name__ == "__main__":
    print("Phase II primitive sign analysis loaded.")
