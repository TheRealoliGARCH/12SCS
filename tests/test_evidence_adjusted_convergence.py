import pytest

from model.evidence_adjusted_convergence import _confidence, _latent_factor


def test_geometric_mean_uses_recognition_and_latent_fields():
    row = {"R": "4", "Q": "0.81", "P": "0.64", "U": "0.49", "D": "0.81", "evidence_confidence": "0.25"}
    factor, coverage = _latent_factor(row, strict=True)
    assert coverage == 5
    assert factor == pytest.approx((0.81 * 0.64 * 0.49 * 0.81) ** 0.25)
    assert _confidence(row) == pytest.approx(0.25)


def test_partial_latent_coverage_is_explicit_not_zero_imputation():
    row = {"R": "4", "Q": "0.8", "P": "0.9"}
    factor, coverage = _latent_factor(row, strict=False)
    assert coverage == 3
    assert factor == pytest.approx((1.0 * 0.8 * 0.9) ** (1 / 3))


def test_strict_mode_rejects_missing_latent_fields():
    row = {"R": "4", "Q": "0.8", "P": "0.9", "U": "0.8"}
    with pytest.raises(ValueError):
        _latent_factor(row, strict=True)


def test_out_of_range_latent_field_rejected():
    row = {"R": "4", "Q": "1.2"}
    with pytest.raises(ValueError):
        _latent_factor(row, strict=False)
