import tempfile
import unittest
from pathlib import Path

import numpy as np

from model.empirical_matrix import (
    build_matrix,
    corridor_gap,
    dispersion,
    pairwise_euclidean,
)


class EmpiricalMatrixTests(unittest.TestCase):
    def test_pairwise_distance_zero_on_diagonal(self):
        X = np.array([[0.0, 0.5], [0.5, 0.5], [1.0, 1.0]])
        D = pairwise_euclidean(X)
        self.assertTrue(np.allclose(np.diag(D), 0.0))
        self.assertTrue(np.allclose(D, D.T))

    def test_missing_rows_are_not_silently_compared(self):
        X = np.array([[0.0, 0.5], [0.5, np.nan], [1.0, 1.0]])
        D = pairwise_euclidean(X)
        self.assertTrue(np.isnan(D[0, 1]))
        self.assertTrue(np.isnan(D[1, 2]))
        self.assertTrue(np.isfinite(D[0, 2]))

    def test_dispersion_zero_for_identical_capabilities(self):
        X = np.full((12, 12), 0.75)
        self.assertAlmostEqual(dispersion(X), 0.0, places=12)

    def test_corridor_gap_zero_inside_tolerance(self):
        X = np.array([[0.49, 0.51], [0.50, 0.50]])
        target = np.array([0.50, 0.50])
        tolerance = np.array([0.02, 0.02])
        self.assertTrue(np.allclose(corridor_gap(X, target, tolerance), 0.0))

    def test_matrix_builder_normalizes_recognition(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "dimension.csv"
            path.write_text(
                "state_id,state,capability_id,capability,R,evidence_confidence\n"
                "1,A,1,Nuclear,4,0.9\n",
                encoding="utf-8",
            )
            result = build_matrix([path])
            self.assertAlmostEqual(result.matrix[0, 0], 1.0, places=12)
            self.assertAlmostEqual(result.confidence[0, 0], 0.9, places=12)
            self.assertTrue(result.observed[0, 0])
            self.assertTrue(np.isnan(result.matrix[1, 1]))

    def test_matrix_builder_rejects_duplicate_observations(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "dimension.csv"
            path.write_text(
                "state_id,state,capability_id,capability,R,evidence_confidence\n"
                "1,A,1,Nuclear,4,0.9\n"
                "1,A,1,Nuclear,3,0.8\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "Duplicate observation"):
                build_matrix([path])


if __name__ == "__main__":
    unittest.main()
