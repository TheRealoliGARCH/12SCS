import unittest

from model.convergence_mechanism import (
    effective_priority,
    feasibility_complement,
    validate_feasibility,
)


class ConvergenceMechanismTests(unittest.TestCase):
    def assertMatrixAlmostEqual(self, actual, expected, places=12):
        self.assertEqual(len(actual), len(expected))
        for arow, erow in zip(actual, expected):
            self.assertEqual(len(arow), len(erow))
            for a, e in zip(arow, erow):
                self.assertAlmostEqual(a, e, places=places)

    def test_validation(self):
        matrix = validate_feasibility(((1.0, 0.5), (0.0, 0.25)), (2, 2))
        self.assertMatrixAlmostEqual(matrix, ((1.0, 0.5), (0.0, 0.25)))

    def test_invalid_values_and_shape(self):
        with self.assertRaises(ValueError):
            validate_feasibility(((1.1,),))
        with self.assertRaises(ValueError):
            validate_feasibility(((0.5,),), (1, 2))

    def test_effective_priority(self):
        gaps = ((0.2, 0.0), (0.0, 0.4))
        weights = (0.75, 0.25)
        feasibility = ((1.0, 0.5), (0.25, 0.5))
        self.assertMatrixAlmostEqual(
            effective_priority(gaps, weights, feasibility),
            ((0.15, 0.0), (0.0, 0.05)),
        )

    def test_complement(self):
        self.assertMatrixAlmostEqual(
            feasibility_complement(((1.0, 0.25), (0.0, 0.5))),
            ((0.0, 0.75), (1.0, 0.5)),
        )


if __name__ == "__main__":
    unittest.main()
