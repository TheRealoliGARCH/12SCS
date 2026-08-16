import pytest

from model.evidence_adjusted_convergence import _latent_factor


def test_geometric_mean_of_all_evidence_fields():
    row = {"Q": "0.81", "P": "0.64", "U": "0.49", "D": "0.81", "evidence_confidence": "1.00"}
    factor, coverage = _latent_factor(row, strict=True)
    assert coverage == 5
    assert factor == pytest.approx((0.81 * 0.64 * 0.49 * 0.81) ** 0.25)


def test_partial_coverage_is_explicit_not_zero_imputation():
    row = {"Q": "0.8", "P": "0.9"}
    factor, coverage = _latent_factor(row, strict=False)
    assert coverage == 2
    assert factor == pytest.approx((0.8 * 0.9) ** 0.5)


def test_strict_mode_rejects_missing_fields():
    row = {"Q": "0.8", "P": "0.9", "U": "0.8", "D": "0.9"}
    with pytest.raises(ValueError):
        _latent_factor(row, strict=True)


def test_out_of_range_latent_field_rejected():
    row = {"Q": "1.2"}
    with pytest.raises(ValueError):
        _latent_factor(row, strict=False)
