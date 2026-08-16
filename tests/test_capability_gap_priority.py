import unittest

from model.capability_gap_priority import (
    capability_priorities,
    convergence_priority,
    dispersion_weights,
    positive_gap,
    signed_gap,
    state_priorities,
    weighted_benchmark,
)


class CapabilityGapPriorityTests(unittest.TestCase):
    def assertMatrixAlmostEqual(self, actual, expected, places=12):
        self.assertEqual(len(actual), len(expected))
        for arow, erow in zip(actual, expected):
            self.assertEqual(len(arow), len(erow))
            for a, e in zip(arow, erow):
                self.assertAlmostEqual(a, e, places=places)

    def test_weighted_benchmark_and_gaps(self):
        scores = ((0.2, 0.8), (0.6, 0.4))
        confidence = ((1.0, 2.0), (1.0, 1.0))
        benchmark = weighted_benchmark(scores, confidence)
        self.assertAlmostEqual(benchmark[0], 0.4)
        self.assertAlmostEqual(benchmark[1], 2.0 / 3.0)
        gaps = signed_gap(scores, benchmark)
        self.assertMatrixAlmostEqual(gaps, ((0.2, -1.0 / 7.5), (-0.2, 0.2666666666666667)))
        self.assertMatrixAlmostEqual(positive_gap(gaps), ((0.2, 0.0), (0.0, 0.2666666666666667)))

    def test_dispersion_weights(self):
        self.assertEqual(dispersion_weights((2.0, 1.0, 1.0)), (0.5, 0.25, 0.25))
        self.assertEqual(dispersion_weights((0.0, 0.0)), (0.5, 0.5))

    def test_priority_with_feasibility(self):
        gaps = ((0.2, 0.0), (0.0, 0.4))
        weights = (0.75, 0.25)
        feasibility = ((1.0, 0.5), (0.25, 0.5))
        priorities = convergence_priority(gaps, weights, feasibility)
        self.assertMatrixAlmostEqual(priorities, ((0.15, 0.0), (0.0, 0.05)))
        self.assertEqual(state_priorities(priorities), (0.15, 0.05))
        self.assertEqual(capability_priorities(priorities), (0.15, 0.05))

    def test_invalid_feasibility(self):
        with self.assertRaises(ValueError):
            convergence_priority(((0.1,),), (1.0,), ((1.1,),))


if __name__ == "__main__":
    unittest.main()
