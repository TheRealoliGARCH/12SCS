import unittest

from results.run_bayesian_structural_counterfactual import audit


class BayesianStructuralCounterfactualTests(unittest.TestCase):
    def setUp(self):
        self.gaps = {
            "s1": {"c1": 0.2, "c2": 0.1},
        }
        self.weights = {"c1": 0.5, "c2": 0.5}
        self.feasibility = {
            "s1": {"c1": 0.8, "c2": 0.7},
        }
        self.costs = {
            "s1": {"c1": 1.2, "c2": 1.3},
        }

    def test_cost_enters_canonical_objective_and_changes_it(self):
        rows = [{
            "regime": "0",
            "lambda_start": "0.0",
            "lambda_end": "0.5",
            "binding_cells": "s1:c1",
            "marginal_cell": "s1:c2",
        }]
        result = audit(rows, self.gaps, self.weights, self.feasibility, self.costs)
        self.assertEqual(result.n_regimes, 1)
        self.assertEqual(result.n_cells, 24)
        self.assertEqual(result.n_admissible_cells, 24)
        self.assertEqual(result.n_excluded_cells, 0)
        self.assertTrue(result.outcome_responds_to_d)
        self.assertGreater(result.n_nonzero_cell_effects, 0)
        self.assertGreater(result.max_abs_effect, 0.0)
        self.assertTrue(result.structural_estimand_defined)
        self.assertFalse(result.empirical_ate_identified)

    def test_negative_cost_cells_are_excluded_not_silently_intervened_on(self):
        costs = {
            "s1": {"c1": 1.2, "c2": 0.8},
        }
        rows = [{
            "regime": "0",
            "lambda_start": "0.0",
            "lambda_end": "0.5",
            "binding_cells": "s1:c1",
            "marginal_cell": "s1:c2",
        }]
        result = audit(rows, self.gaps, self.weights, self.feasibility, costs)
        self.assertEqual(result.n_admissible_cells, 12)
        self.assertEqual(result.n_excluded_cells, 12)
        self.assertFalse(result.empirical_ate_identified)


if __name__ == "__main__":
    unittest.main()
