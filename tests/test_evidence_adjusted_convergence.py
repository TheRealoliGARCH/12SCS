import unittest

from model.evidence_adjusted_convergence import _confidence, _latent_factor


class EvidenceAdjustedConvergenceTests(unittest.TestCase):
    def test_geometric_mean_uses_recognition_and_latent_fields(self):
        row = {
            "R": "4",
            "Q": "0.81",
            "P": "0.64",
            "U": "0.49",
            "D": "0.81",
            "evidence_confidence": "0.25",
        }
        factor, coverage = _latent_factor(row, strict=True)
        self.assertEqual(coverage, 5)
        self.assertAlmostEqual(
            factor, (1.0 * 0.81 * 0.64 * 0.49 * 0.81) ** 0.2, places=12
        )
        self.assertAlmostEqual(_confidence(row), 0.25, places=12)

    def test_partial_latent_coverage_is_explicit_not_zero_imputation(self):
        row = {"R": "4", "Q": "0.8", "P": "0.9"}
        factor, coverage = _latent_factor(row, strict=False)
        self.assertEqual(coverage, 3)
        self.assertAlmostEqual(factor, (1.0 * 0.8 * 0.9) ** (1 / 3), places=12)

    def test_strict_mode_rejects_missing_latent_fields(self):
        row = {"R": "4", "Q": "0.8", "P": "0.9", "U": "0.8"}
        with self.assertRaises(ValueError):
            _latent_factor(row, strict=True)

    def test_out_of_range_latent_field_rejected(self):
        row = {"R": "4", "Q": "1.2"}
        with self.assertRaises(ValueError):
            _latent_factor(row, strict=False)


if __name__ == "__main__":
    unittest.main()
