import unittest

from results.run_primitive_coefficient_map import derive


class PrimitiveCoefficientMapTests(unittest.TestCase):
    def test_exact_map_and_discriminant_identities(self):
        gaps = {"S1": {"N": 0.20}, "S2": {"N": 0.10}}
        weights = {"N": 0.5}
        feasibility = {
            "S1": {"N": 0.80},
            "S2": {"N": 0.70},
            "M": {"N": 0.60},
        }
        costs = {
            "S1": {"N": 1.20},
            "S2": {"N": 1.10},
            "M": {"N": 1.40},
        }
        c = derive(
            ["S1:N", "S2:N"],
            "M:N",
            gaps,
            weights,
            feasibility,
            costs,
        )
        self.assertAlmostEqual(c["C"], 0.70)
        self.assertAlmostEqual(c["D"], 0.05)
        self.assertAlmostEqual(c["E"], -0.016)
        self.assertAlmostEqual(c["F"], 0.40)
        self.assertAlmostEqual(c["p1"], 2.0 * c["S"])
        self.assertAlmostEqual(c["p2"], c["F"] * c["S"])
        self.assertAlmostEqual(c["Delta_P"], 4.0 * c["S"] * c["T"])
        self.assertAlmostEqual(c["q0"], 2.0 * c["T"])
        self.assertAlmostEqual(
            c["Delta_Q"],
            4.0 * c["F"]**4 * (c["r1"]**2 - 4.0*c["r0"]*c["r2"]),
        )


if __name__ == "__main__":
    unittest.main()
