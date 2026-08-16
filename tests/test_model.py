import numpy as np

from model.dimensions import STATES, CAPABILITIES
from model.recognition import (
    concentration_index,
    demonstrated_capability,
    recognition_intensity,
    recognition_level,
    uniqueness,
)
from model.network import effective_dependency
from model.convergence import dispersion
from model.nuclear import eligibility_gate, peaceful_transfer
from model.stability import stability_margin


def test_dimensions():
    assert len(STATES) == 12
    assert len(CAPABILITIES) == 12


def test_recognition_bounds_and_levels():
    x = recognition_intensity(.9, .8, .7, .6)
    assert 0 <= x <= 1
    assert recognition_level(np.array([0., .2, .5, .8, 1.])).tolist() == [0, 1, 2, 4, 4]


def test_evidence_aggregator():
    assert np.isclose(demonstrated_capability([0.5, 0.5]), 0.75)


def test_concentration_bounds():
    R = np.ones((12, 1))
    assert np.isclose(concentration_index(R)[0], 1 / 12)
    R[1:, 0] = 0
    assert np.isclose(concentration_index(R)[0], 1.0)


def test_effective_dependency():
    assert np.isclose(effective_dependency([.8], [1.0])[0], 0.0)
    assert np.isclose(effective_dependency([.8], [0.0])[0], .8)


def test_convergence():
    R = np.ones((12, 12)) * .75
    assert np.isclose(dispersion(R), 0.0)


def test_nuclear_gate_and_transfer():
    assert eligibility_gate([1, 1, 1]) == 1
    assert eligibility_gate([1, 0, 1]) == 0
    assert peaceful_transfer(.8, 1) == .8
    assert peaceful_transfer(.8, 0) == 0.0


def test_stability_margin_identity():
    assert np.isclose(stability_margin(np.eye(2)), 0.0)
