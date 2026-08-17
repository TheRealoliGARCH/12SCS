import unittest

from results.run_bayesian_admissible_intervention_audit import audit


class BayesianAdmissibleInterventionAuditTests(unittest.TestCase):
    def test_restricting_to_nonnegative_costs_identifies_structural_intervention(self):
        cells = [
            type("C", (), {"regime": 1, "state": "s", "capability": "c", "gap": 2.0, "weight": 1.0, "a": 0.2, "d": 0.0, "treatment_active": 1})(),
            type("C", (), {"regime": 1, "state": "s", "capability": "d", "gap": 1.0, "weight": 1.0, "a": 0.1, "d": 0.8, "treatment_active": 0})(),
            type("C", (), {"regime": 1, "state": "s", "capability": "e", "gap": 1.5, "weight": 1.0, "a": 0.1, "d": -0.2, "treatment_active": 0})(),
        ]
        result = audit(cells)
        self.assertEqual(result.n_total, 3)
        self.assertEqual(result.n_admissible, 2)
        self.assertEqual(result.n_excluded, 1)
        self.assertTrue(result.intervention_well_defined)
        self.assertTrue(result.outcome_pre_treatment)
        self.assertTrue(result.structural_positivity)
        self.assertTrue(result.consistency)
        self.assertFalse(result.empirical_ate_identified)
        self.assertTrue(result.structural_ate_identified)
        self.assertEqual(result.identification_status, "ADMISSIBLE_STRUCTURAL_INTERVENTION_IDENTIFIED_BUT_EMPIRICAL_ATE_NOT_IDENTIFIED")

    def test_all_negative_costs_are_rejected_as_empty_target_population(self):
        cell = type("C", (), {"regime": 1, "state": "s", "capability": "c", "gap": 2.0, "weight": 1.0, "a": 0.2, "d": -0.1, "treatment_active": 1})()
        with self.assertRaises(ValueError):
            audit([cell])


if __name__ == "__main__":
    unittest.main()
