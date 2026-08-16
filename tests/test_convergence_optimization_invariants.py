import unittest

from model.convergence_optimization import allocate_budget, total_cost, weighted_progress


class ConvergenceOptimizationInvariantTests(unittest.TestCase):
    def setUp(self):
        self.gaps = (
            (0.8, 0.4),
            (0.2, 0.6),
        )
        self.weights = (0.6, 0.4)
        self.feasibility = (
            (0.5, 1.0),
            (1.0, 0.25),
        )
        self.costs = (
            (2.0, 1.0),
            (4.0, 2.0),
        )

    def test_allocation_respects_feasibility_caps(self):
        allocation = allocate_budget(
            self.gaps, self.weights, self.feasibility, self.costs, budget=100.0
        )
        for i in range(2):
            for j in range(2):
                self.assertGreaterEqual(allocation[i][j], 0.0)
                self.assertLessEqual(
                    allocation[i][j],
                    self.gaps[i][j] * self.feasibility[i][j] + 1e-12,
                )

    def test_budget_is_never_exceeded(self):
        allocation = allocate_budget(
            self.gaps, self.weights, self.feasibility, self.costs, budget=1.5
        )
        self.assertLessEqual(total_cost(allocation, self.costs), 1.5 + 1e-12)

    def test_zero_budget_gives_zero_allocation(self):
        allocation = allocate_budget(
            self.gaps, self.weights, self.feasibility, self.costs, budget=0.0
        )
        self.assertEqual(allocation, ((0.0, 0.0), (0.0, 0.0)))

    def test_progress_is_monotone_in_budget(self):
        previous = -1.0
        for budget in (0.0, 0.25, 0.5, 1.0, 2.0, 5.0, 100.0):
            allocation = allocate_budget(
                self.gaps, self.weights, self.feasibility, self.costs, budget=budget
            )
            progress = weighted_progress(allocation, self.weights)
            self.assertGreaterEqual(progress + 1e-12, previous)
            previous = progress

    def test_zero_feasibility_produces_zero_allocation(self):
        zero = ((0.0, 0.0), (0.0, 0.0))
        allocation = allocate_budget(
            self.gaps, self.weights, zero, self.costs, budget=100.0
        )
        self.assertEqual(allocation, ((0.0, 0.0), (0.0, 0.0)))

    def test_removing_actionable_gap_cannot_increase_progress(self):
        full = allocate_budget(
            self.gaps, self.weights, self.feasibility, self.costs, budget=2.0
        )
        reduced_gaps = ((0.0, self.gaps[0][1]), self.gaps[1])
        reduced = allocate_budget(
            reduced_gaps, self.weights, self.feasibility, self.costs, budget=2.0
        )
        self.assertLessEqual(
            weighted_progress(reduced, self.weights),
            weighted_progress(full, self.weights) + 1e-12,
        )


if __name__ == "__main__":
    unittest.main()
