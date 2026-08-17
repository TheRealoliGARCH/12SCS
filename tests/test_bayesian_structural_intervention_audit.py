import csv
import tempfile
import unittest
from pathlib import Path

from results.run_bayesian_structural_intervention_audit import audit, load_cells


class BayesianStructuralInterventionAuditTests(unittest.TestCase):
    def test_structural_intervention_is_defined_but_empirical_ate_is_not(self):
        cells = [
            type("C", (), {"regime": 1, "state": "s", "capability": "c", "gap": 2.0, "weight": 1.0, "a": 0.2, "d": 0.5, "treatment_active": 1})(),
            type("C", (), {"regime": 1, "state": "s", "capability": "d", "gap": 1.0, "weight": 1.0, "a": 0.1, "d": 0.8, "treatment_active": 0})(),
        ]
        result = audit(cells)
        self.assertTrue(result.intervention_is_well_defined)
        self.assertTrue(result.outcome_is_pre_treatment)
        self.assertTrue(result.positivity)
        self.assertFalse(result.exchangeability_empirically_testable)
        self.assertFalse(result.empirical_ate_identified)
        self.assertTrue(result.structural_ate_identified)
        self.assertEqual(result.identification_status, "STRUCTURAL_INTERVENTION_IDENTIFIED_BUT_EMPIRICAL_ATE_NOT_IDENTIFIED")

    def test_invalid_negative_cost_rejects_structural_intervention(self):
        cell = type("C", (), {"regime": 1, "state": "s", "capability": "c", "gap": 2.0, "weight": 1.0, "a": 0.2, "d": -0.1, "treatment_active": 1})()
        result = audit([cell])
        self.assertFalse(result.intervention_is_well_defined)
        self.assertFalse(result.structural_ate_identified)


if __name__ == "__main__":
    unittest.main()
