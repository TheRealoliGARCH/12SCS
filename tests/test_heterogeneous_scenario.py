import unittest

from model.convergence_analysis import CAPABILITIES, STATES
from model.heterogeneous_scenario import build_scenario


class HeterogeneousScenarioTests(unittest.TestCase):
    def test_shape_and_bounds(self):
        feasibility, costs = build_scenario(STATES, CAPABILITIES)
        self.assertEqual(len(feasibility), len(STATES))
        self.assertEqual(len(costs), len(STATES))
        for row in feasibility:
            self.assertEqual(len(row), len(CAPABILITIES))
            self.assertTrue(all(0.0 <= x <= 1.0 for x in row))
        for row in costs:
            self.assertEqual(len(row), len(CAPABILITIES))
            self.assertTrue(all(x > 0.0 for x in row))

    def test_determinism(self):
        first = build_scenario(STATES, CAPABILITIES)
        second = build_scenario(STATES, CAPABILITIES)
        self.assertEqual(first, second)

    def test_heterogeneity_is_nontrivial(self):
        feasibility, costs = build_scenario(STATES, CAPABILITIES)
        self.assertGreater(len({x for row in feasibility for x in row}), 1)
        self.assertGreater(len({x for row in costs for x in row}), 1)


if __name__ == "__main__":
    unittest.main()
