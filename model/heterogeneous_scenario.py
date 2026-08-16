"""Deterministic abstract cost-feasibility scenario for 12SCCM.

The scenario is synthetic and non-sensitive. It is intended to test how the
allocator behaves when feasibility and normalized intervention costs vary by
State-capability cell. It is not an empirical safety assessment or a policy
recommendation.
"""
from __future__ import annotations

from typing import Sequence


def build_scenario(states: Sequence[str], capabilities: Sequence[str]):
    """Return deterministic feasibility and cost matrices in [0,1] and >0."""
    n = len(states)
    k = len(capabilities)
    if n == 0 or k == 0:
        raise ValueError("states and capabilities must be non-empty")

    feasibility = []
    costs = []
    for i in range(n):
        f_row = []
        c_row = []
        for j in range(k):
            # Abstract scenario only: smooth deterministic heterogeneity.
            f = 0.35 + 0.60 * ((i + 2 * j + 1) % 11) / 10.0
            c = 0.75 + 1.50 * ((2 * i + j + 3) % 13) / 12.0
            f_row.append(min(1.0, f))
            c_row.append(c)
        feasibility.append(tuple(f_row))
        costs.append(tuple(c_row))
    return tuple(feasibility), tuple(costs)
