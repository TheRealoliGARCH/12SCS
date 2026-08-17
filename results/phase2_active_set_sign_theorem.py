"""Phase II: active-set primitive sign conditions.

For a fixed regime, binding cells i are filled to capacity and one marginal
cell m absorbs the residual budget.  Define
    a_i = kappa_i^0 - 1, d_i = c_i^0 - 1, F = d_m,
with -1 <= a_i <= 0 and F > -1.

The allocation ordering is based on benefit/cost ratios
    w_i/(1+d_i) >= w_m/(1+F)
for every binding cell i.

The purpose of this module is deliberately modest: it derives exact
cellwise sufficient conditions for endpoint monotonicity and curvature.  The
ordering inequality alone is NOT asserted to imply those signs.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class PrimitiveCell:
    gap: float
    weight: float
    a: float
    d: float


def p0_terms(cell: PrimitiveCell, F: float) -> float:
    """The cell contribution to p0, excluding the common -F*B0 term."""
    return cell.gap * (cell.weight * cell.a - cell.a - cell.d + F)


def p1_endpoint_terms(cell: PrimitiveCell, F: float) -> float:
    """The cell contribution to P(1), excluding the common -F*B0 term."""
    a, d, w = cell.a, cell.d, cell.weight
    return cell.gap * (w * a * (1.0 + F) ** 2
                       - (a + d)
                       - a * d * (2.0 + F)
                       + F)


def q0_cell_term(cell: PrimitiveCell, F: float) -> float:
    """The cell term inside q0/2, before the minus sign."""
    return cell.gap * (cell.a - F) * (cell.d - F)


def ordering_holds(cell: PrimitiveCell, F: float) -> bool:
    """Check the active-set benefit/cost ordering against the marginal cell."""
    return cell.weight / (1.0 + cell.d) >= 1.0 / (1.0 + F)


def simple_sufficient_conditions(F: float, cell: PrimitiveCell) -> dict[str, bool]:
    """Return elementary cellwise conditions for the three target signs."""
    a, d, w = cell.a, cell.d, cell.weight
    # p0 contribution <= 0 iff a(w-1) + F-d <= 0.
    p0_ok = a * (w - 1.0) + F - d <= 0.0

    # P(1) contribution <= 0. This is exact for each cell.
    p1_ok = (w * a * (1.0 + F) ** 2
             - (a + d)
             - a * d * (2.0 + F)
             + F) <= 0.0

    # q0 >= 0 is guaranteed cellwise when (a-F)(d-F) <= 0,
    # since the aggregate formula is q0/2 = F^2 B0 - sum cell terms.
    q0_ok = (a - F) * (d - F) <= 0.0
    return {"p0_cell_nonpositive": p0_ok,
            "P1_cell_nonpositive": p1_ok,
            "q0_cell_safe": q0_ok}


def aggregate_certificates(cells: Sequence[PrimitiveCell], budget: float, F: float) -> dict[str, float]:
    """Return exact aggregate certificate margins."""
    p0_margin = F * budget - sum(p0_terms(c, F) for c in cells)
    P1_margin = F * budget - sum(p1_endpoint_terms(c, F) for c in cells)
    q0_half = F * F * budget - sum(q0_cell_term(c, F) for c in cells)
    return {
        "p0_margin": p0_margin,
        "P1_margin": P1_margin,
        "q0_half": q0_half,
        "q0": 2.0 * q0_half,
    }


def theorem_statement() -> str:
    return (
        "If every binding cell satisfies a_i(w_i-1)+F-d_i <= 0, then p0 <= 0; "
        "if at least one is strict or F*B0>0, then p0<0. "
        "If every binding cell satisfies "
        "w_i a_i(1+F)^2-(a_i+d_i)-a_i d_i(2+F)+F <= 0, "
        "then P(1)<=0; strictness gives P(1)<0. "
        "Finally, q0>=0 iff F^2 B0 >= sum_i g_i(a_i-F)(d_i-F). "
        "A sufficient cellwise condition for the latter is (a_i-F)(d_i-F)<=0 for every i. "
        "The benefit/cost ordering w_i/(1+d_i)>=w_m/(1+F) is recorded separately "
        "and is not, by itself, claimed to imply these sign conditions."
    )


if __name__ == "__main__":
    print(theorem_statement())
