import numpy as np
import pytest

from model.empirical_matrix import (
    build_matrix,
    corridor_gap,
    dispersion,
    pairwise_euclidean,
)


def test_pairwise_distance_zero_on_diagonal():
    X = np.array([[0.0, 0.5], [0.5, 0.5], [1.0, 1.0]])
    D = pairwise_euclidean(X)
    assert np.allclose(np.diag(D), 0.0)
    assert np.allclose(D, D.T)


def test_missing_rows_are_not_silently_compared():
    X = np.array([[0.0, 0.5], [0.5, np.nan], [1.0, 1.0]])
    D = pairwise_euclidean(X)
    assert np.isnan(D[0, 1])
    assert np.isnan(D[1, 2])
    assert np.isfinite(D[0, 2])


def test_dispersion_zero_for_identical_capabilities():
    X = np.full((12, 12), 0.75)
    assert dispersion(X) == pytest.approx(0.0)


def test_corridor_gap_zero_inside_tolerance():
    X = np.array([[0.49, 0.51], [0.50, 0.50]])
    target = np.array([0.50, 0.50])
    tolerance = np.array([0.02, 0.02])
    assert np.allclose(corridor_gap(X, target, tolerance), 0.0)


def test_matrix_builder_normalizes_recognition(tmp_path):
    path = tmp_path / "dimension.csv"
    path.write_text(
        "state_id,state,capability_id,capability,R,evidence_confidence\n"
        "1,A,1,Nuclear,4,0.9\n",
        encoding="utf-8",
    )
    result = build_matrix([path])
    assert result.matrix[0, 0] == pytest.approx(1.0)
    assert result.confidence[0, 0] == pytest.approx(0.9)
    assert result.observed[0, 0]
    assert np.isnan(result.matrix[1, 1])


def test_matrix_builder_rejects_duplicate_observations(tmp_path):
    path = tmp_path / "dimension.csv"
    path.write_text(
        "state_id,state,capability_id,capability,R,evidence_confidence\n"
        "1,A,1,Nuclear,4,0.9\n"
        "1,A,1,Nuclear,3,0.8\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="Duplicate observation"):
        build_matrix([path])
