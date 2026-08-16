import math

import pytest

from model.capability_gap_priority import (
    capability_priorities,
    convergence_priority,
    dispersion_weights,
    positive_gap,
    signed_gap,
    state_priorities,
    weighted_benchmark,
)


def test_weighted_benchmark_and_gaps():
    scores = ((0.2, 0.8), (0.6, 0.4))
    confidence = ((1.0, 2.0), (1.0, 1.0))
    benchmark = weighted_benchmark(scores, confidence)
    assert benchmark == pytest.approx((0.4, 0.6666666666666666))
    gaps = signed_gap(scores, benchmark)
    assert gaps == pytest.approx(((0.2, -0.1333333333333333), (-0.2, 0.2666666666666666)))
    assert positive_gap(gaps) == pytest.approx(((0.2, 0.0), (0.0, 0.2666666666666666)))


def test_dispersion_weights():
    assert dispersion_weights((2.0, 1.0, 1.0)) == pytest.approx((0.5, 0.25, 0.25))
    assert dispersion_weights((0.0, 0.0)) == pytest.approx((0.5, 0.5))


def test_priority_with_feasibility():
    gaps = ((0.2, 0.0), (0.0, 0.4))
    weights = (0.75, 0.25)
    feasibility = ((1.0, 0.5), (0.25, 0.5))
    priorities = convergence_priority(gaps, weights, feasibility)
    assert priorities == pytest.approx(((0.15, 0.0), (0.0, 0.05)))
    assert state_priorities(priorities) == pytest.approx((0.15, 0.05))
    assert capability_priorities(priorities) == pytest.approx((0.15, 0.05))


def test_invalid_feasibility():
    with pytest.raises(ValueError):
        convergence_priority(((0.1,),), (1.0,), ((1.1,),))
