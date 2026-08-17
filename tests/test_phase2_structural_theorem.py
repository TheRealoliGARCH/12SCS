import unittest

from results.phase2_structural_theorem import Cell, certificates, interpret_curvature


class Phase2StructuralTheoremTests(unittest.TestCase):
    def test_exact_endpoint_and_curvature_forms(self):
        cells = [
            Cell(gap=0.20, weight=1.2, a=-0.20, d=0.80),
            Cell(gap=0.10, weight=1.1, a=-0.30, d=0.70),
        ]
        c = certificates(cells, budget=1.0, F=0.60)
        self.assertLess(c["p0"], 0.0)
        self.assertLess(c["P1"], 0.0)
        self.assertGreaterEqual(c["q0"], 0.0)
        self.assertTrue(c["p0_cellwise_nonpositive"])
        self.assertTrue(c["P1_cellwise_nonpositive"])
        self.assertTrue(c["curvature_cellwise_nonnegative"])

    def test_curvature_simplification_for_nonnegative_F(self):
        self.assertIn("d_i >= F", interpret_curvature(0.5))
        self.assertIn("full product", interpret_curvature(-0.2))


if __name__ == "__main__":
    unittest.main()
