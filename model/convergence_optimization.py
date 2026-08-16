"""Deterministic baseline for constrained capability convergence.

This module provides a solver-independent fractional budget allocator. It is a
transparent baseline, not a claim of globally optimal nonlinear reduction of
the V2 dispersion statistic. Each allocation is bounded by the measured
positive gap and its abstract feasibility coefficient.
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


def allocate_budget(positive_gaps: Matrix, capability_weights: Sequence[float], feasibility: Matrix, costs: Matrix, budget: float) -> tuple[tuple[float, ...], ...]:
    """Allocate a finite budget by descending weighted benefit per cost."""
    n, k = _shape(positive_gaps)
    if len(capability_weights) != k:
        raise ValueError("capability_weights length mismatch")
    if _shape(feasibility) != (n, k) or _shape(costs) != (n, k):
        raise ValueError("feasibility and costs must match the gap matrix")
    if budget < 0:
        raise ValueError("budget must be non-negative")
    omega = tuple(float(x) for x in capability_weights)
    if any(x < 0 for x in omega):
        raise ValueError("capability weights must be non-negative")
    kappa = tuple(tuple(float(x) for x in row) for row in feasibility)
    cost = tuple(tuple(float(x) for x in row) for row in costs)
    gap = tuple(tuple(float(x) for x in row) for row in positive_gaps)
    if any(x < 0 or x > 1 for row in kappa for x in row):
        raise ValueError("feasibility coefficients must lie in [0,1]")
    if any(x < 0 for row in cost for x in row):
        raise ValueError("costs must be non-negative")
    if any(kappa[i][j] > 0 and gap[i][j] > 0 and cost[i][j] <= 0 for i in range(n) for j in range(k)):
        raise ValueError("actionable cells must have strictly positive costs")
    candidates = []
    for i in range(n):
        for j in range(k):
            cap = gap[i][j] * kappa[i][j]
            if cap > 0:
                candidates.append((omega[j] / cost[i][j], i, j, cap))
    candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
    allocation = [[0.0 for _ in range(k)] for _ in range(n)]
    remaining = float(budget)
    for _, i, j, cap in candidates:
        if remaining <= 0:
            break
        spend = min(remaining, cap * cost[i][j])
        allocation[i][j] = spend / cost[i][j]
        remaining -= spend
    return tuple(tuple(row) for row in allocation)


def total_cost(allocation: Matrix, costs: Matrix) -> float:
    """Return total cost of an allocation."""
    if _shape(allocation) != _shape(costs):
        raise ValueError("allocation and costs must have identical shapes")
    return fsum(float(allocation[i][j]) * float(costs[i][j]) for i in range(len(allocation)) for j in range(len(allocation[0])))


def weighted_progress(allocation: Matrix, capability_weights: Sequence[float]) -> float:
    """Return the weighted linear convergence-progress proxy."""
    n, k = _shape(allocation)
    if len(capability_weights) != k:
        raise ValueError("capability_weights length mismatch")
    return fsum(float(allocation[i][j]) * float(capability_weights[j]) for i in range(n) for j in range(k))
