import unittest

from model.convergence_optimization import allocate_budget, total_cost, weighted_progress


class ConvergenceSensitivityTests(unittest.TestCase):
    def setUp(self):
        self.gaps = ((0.8, 0.4), (0.6, 0.9))
        self.weights = (0.6, 0.4)
        self.feasibility = ((1.0, 0.8), (0.7, 1.0))
        self.costs = ((1.0, 1.5), (1.25, 0.75))

    def test_level_zero_equivalent_to_unit_case(self):
        allocation = allocate_budget(
            self.gaps,
            self.weights,
            ((1.0, 1.0), (1.0, 1.0)),
            ((1.0, 1.0), (1.0, 1.0)),
            1.0,
        )
        self.assertAlmostEqual(total_cost(allocation, ((1.0, 1.0), (1.0, 1.0))), 1.0)
        self.assertAlmostEqual(weighted_progress(allocation, self.weights), 0.6)

    def test_budget_and_feasibility_invariants(self):
        allocation = allocate_budget(
            self.gaps, self.weights, self.feasibility, self.costs, 1.0
        )
        self.assertLessEqual(total_cost(allocation, self.costs), 1.0 + 1e-12)
        for i in range(2):
            for j in range(2):
                self.assertGreaterEqual(allocation[i][j], -1e-12)
                self.assertLessEqual(
                    allocation[i][j],
                    self.gaps[i][j] * self.feasibility[i][j] + 1e-12,
                )

    def test_higher_feasibility_cannot_reduce_attainable_progress(self):
        low = ((0.5, 0.5), (0.5, 0.5))
        high = ((1.0, 1.0), (1.0, 1.0))
        costs = ((1.0, 1.0), (1.0, 1.0))
        p_low = weighted_progress(
            allocate_budget(self.gaps, self.weights, low, costs, 1.0), self.weights
        )
        p_high = weighted_progress(
            allocate_budget(self.gaps, self.weights, high, costs, 1.0), self.weights
        )
        self.assertGreaterEqual(p_high + 1e-12, p_low)


if __name__ == "__main__":
    unittest.main()
