import unittest

from results.phase2_primitive_sign_analysis import Cell, derive


class Phase2PrimitiveSignTests(unittest.TestCase):
    def test_endpoint_and_curvature_identities(self):
        cells = [
            Cell(gap=0.20, weight=0.5, a=-0.20, d=0.20),
            Cell(gap=0.10, weight=0.5, a=-0.30, d=0.10),
        ]
        c = derive(cells, budget=1.0, marginal_d=0.40)

        self.assertAlmostEqual(c["p0"], c["B"] + c["D"] - c["F"] * c["C"])
        self.assertAlmostEqual(c["p1"], 2.0 * (c["B"] * c["F"] + c["E"]))
        self.assertAlmostEqual(c["p2"], c["F"] * (c["B"] * c["F"] + c["E"]))
        self.assertAlmostEqual(c["P1"], c["p0"] + c["p1"] + c["p2"])

        expected_q0 = 2.0 * (
            c["F"]**2 * 1.0
            - sum(cell.gap * (cell.a - c["F"]) * (cell.d - c["F"]) for cell in cells)
        )
        self.assertAlmostEqual(c["q0"], expected_q0)
        self.assertEqual(c["q1"], 0.0)
        self.assertEqual(c["q2"], 0.0)
        self.assertAlmostEqual(c["Q1"], c["q0"])


if __name__ == "__main__":
    unittest.main()
