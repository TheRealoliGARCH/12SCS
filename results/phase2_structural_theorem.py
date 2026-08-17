"""Phase II structural theorem characterization.

This module separates identities, exact sign conditions, and genuinely sufficient
primitive restrictions.  It deliberately does not promote an active-set ratio
ordering into a sign theorem unless the missing primitive inequalities are also
present.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Cell:
    gap: float
    weight: float
    a: float
    d: float


def endpoint_terms(cell: Cell, F: float) -> tuple[float, float]:
    """Return the cell contributions to p0 and P(1)."""
    p0_term = cell.gap * (cell.a * (cell.weight - 1.0) + F - cell.d)
    p1_term = cell.gap * (
        cell.weight * cell.a * (1.0 + F) ** 2
        - (cell.a + cell.d)
        - cell.a * cell.d * (2.0 + F)
        + F
    )
    return p0_term, p1_term


def certificates(cells: list[Cell], budget: float, F: float) -> dict[str, float | bool]:
    """Evaluate exact endpoint and curvature certificates."""
    p0 = sum(endpoint_terms(c, F)[0] for c in cells) - F * budget
    P1 = sum(endpoint_terms(c, F)[1] for c in cells) - F * budget
    curvature_core = F * F * budget - sum(
        c.gap * (c.a - F) * (c.d - F) for c in cells
    )
    return {
        "p0": p0,
        "P1": P1,
        "q0": 2.0 * curvature_core,
        "p0_cellwise_nonpositive": all(endpoint_terms(c, F)[0] <= 0 for c in cells),
        "P1_cellwise_nonpositive": all(endpoint_terms(c, F)[1] <= 0 for c in cells),
        "curvature_cellwise_nonnegative": all(
            (c.a - F) * (c.d - F) <= 0 for c in cells
        ),
    }


def theorem_conditions(F: float) -> dict[str, str]:
    """State transparent sufficient conditions without overclaiming."""
    return {
        "denominator": "F > -1 => 1+F lambda > 0 on [0,1]",
        "decrease_at_zero": "F > -1 and p0 < 0",
        "decrease_at_one": "F > -1 and P1 < 0",
        "global_decrease_convex_P": "p2 >= 0, p0 < 0, P1 < 0",
        "global_decrease_concave_P": "p2 < 0 and Delta_P < 0",
        "convexity": "F > -1 and q0 >= 0",
        "cellwise_convexity": "(a_i-F)(d_i-F) <= 0 for every binding i",
    }


def interpret_curvature(F: float) -> str:
    """Give the useful primitive simplification when F >= 0."""
    if F >= 0:
        return (
            "Because a_i <= 0, F >= 0 implies a_i-F <= 0; therefore "
            "d_i >= F for every binding cell is sufficient for cellwise convexity."
        )
    return "For F < 0, the curvature sign requires the full product condition."


if __name__ == "__main__":
    print("Phase II structural theorem characterization loaded.")
