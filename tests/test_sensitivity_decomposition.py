import unittest

from model.convergence_analysis import CAPABILITIES, STATES
from model.convergence_optimization import allocate_budget, total_cost, weighted_progress
from model.heterogeneous_scenario import build_scenario


class SensitivityDecompositionTests(unittest.TestCase):
    def test_homogeneous_equivalence(self):
        positive = tuple(tuple(1.0 for _ in CAPABILITIES) for _ in STATES)
        weights = tuple(1.0 / len(CAPABILITIES) for _ in CAPABILITIES)
        ones = tuple(tuple(1.0 for _ in CAPABILITIES) for _ in STATES)
        allocation = allocate_budget(positive, weights, ones, ones, 1.0)
        self.assertAlmostEqual(total_cost(allocation, ones), 1.0, places=12)
        self.assertAlmostEqual(weighted_progress(allocation, weights), 1.0, places=12)

    def test_scenario_dimensions(self):
        feasibility, costs = build_scenario(STATES, CAPABILITIES)
        self.assertEqual(len(feasibility), len(STATES))
        self.assertEqual(len(costs), len(STATES))
        self.assertTrue(all(len(row) == len(CAPABILITIES) for row in feasibility))
        self.assertTrue(all(len(row) == len(CAPABILITIES) for row in costs))
        self.assertTrue(all(0.0 <= x <= 1.0 for row in feasibility for x in row))
        self.assertTrue(all(x > 0.0 for row in costs for x in row))


if __name__ == "__main__":
    unittest.main()
