import unittest

from model.convergence_optimization import (
    allocate_budget,
    total_cost,
    weighted_progress,
)


class ConvergenceOptimizationTests(unittest.TestCase):
    def test_budgeted_fractional_allocation(self):
        gaps = ((0.4, 0.2), (0.1, 0.3))
        weights = (0.75, 0.25)
        feasibility = ((1.0, 1.0), (1.0, 1.0))
        costs = ((1.0, 2.0), (4.0, 1.0))
        allocation = allocate_budget(gaps, weights, feasibility, costs, 0.5)
        self.assertAlmostEqual(total_cost(allocation, costs), 0.5, places=12)
        self.assertAlmostEqual(allocation[0][0], 0.4, places=12)
        self.assertAlmostEqual(allocation[1][1], 0.1, places=12)

    def test_feasibility_caps_allocation(self):
        gaps = ((0.4,),)
        weights = (1.0,)
        feasibility = ((0.25,),)
        costs = ((1.0,),)
        allocation = allocate_budget(gaps, weights, feasibility, costs, 1.0)
        self.assertAlmostEqual(allocation[0][0], 0.1, places=12)
        self.assertAlmostEqual(total_cost(allocation, costs), 0.1, places=12)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            allocate_budget(((0.1,),), (1.0,), ((1.1,),), ((1.0,),), 1.0)
        with self.assertRaises(ValueError):
            allocate_budget(((0.1,),), (1.0,), ((1.0,),), ((0.0,),), 1.0)
        with self.assertRaises(ValueError):
            allocate_budget(((0.1,),), (1.0,), ((1.0,),), ((1.0,),), -1.0)

    def test_weighted_progress(self):
        allocation = ((0.2, 0.1), (0.0, 0.3))
        self.assertAlmostEqual(weighted_progress(allocation, (0.75, 0.25)), 0.25, places=12)


if __name__ == "__main__":
    unittest.main()
