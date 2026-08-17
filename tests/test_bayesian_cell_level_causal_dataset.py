import unittest

from results.run_bayesian_cell_level_causal_dataset import CellObservation, audit_identification


class BayesianCellLevelCausalDatasetTests(unittest.TestCase):
    def test_identification_audit_is_conservative(self):
        rows = [
            CellObservation(1, "S1", "N", 0.0, 0.5, 0.25, 1, "binding", 0.2, 1.0, -0.2, 0.3, 0.19, -0.1),
            CellObservation(1, "S1", "S", 0.0, 0.5, 0.25, 0, "inactive", 0.1, 1.0, -0.3, 0.2, 0.0, -0.1),
            CellObservation(2, "S1", "N", 0.5, 1.0, 0.75, 0, "inactive", 0.2, 1.0, -0.2, 0.3, 0.0, -0.2),
            CellObservation(2, "S1", "S", 0.5, 1.0, 0.75, 1, "marginal", 0.1, 1.0, -0.3, 0.2, 0.0775, -0.2),
        ]
        a = audit_identification(rows)
        self.assertTrue(a["treatment_varies"])
        self.assertTrue(a["outcome_varies"])
        self.assertTrue(a["within_regime_positivity"])
        self.assertTrue(a["temporal_ordering"])
        self.assertFalse(a["intervention_defined"])
        self.assertTrue(a["outcome_mechanically_post_treatment"])
        self.assertFalse(a["causal_effect_identified"])

    def test_empty_dataset_rejected(self):
        with self.assertRaises(ValueError):
            audit_identification([])


if __name__ == "__main__":
    unittest.main()
