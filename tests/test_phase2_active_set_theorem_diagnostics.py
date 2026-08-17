import unittest

from results.run_phase2_active_set_theorem_diagnostics import regime_certificate


class Phase2ActiveSetDiagnosticTests(unittest.TestCase):
    def test_certificate_matches_primitive_formulas(self):
        gaps = {"S1": {"N": 0.20}}
        weights = {"N": 1.20}
        feasibility = {"S1": {"N": 0.80}, "M": {"N": 0.60}}
        # The binding cell must have at least as good weighted benefit per
        # unit cost as the marginal cell for the ordering certificate.
        costs = {"S1": {"N": 1.20}, "M": {"N": 1.40}}
        c = regime_certificate(["S1:N"], "M:N", gaps, weights, feasibility, costs)

        F = 0.40
        g = 0.20
        a = -0.20
        d = 0.20
        expected_p0 = g * (a * (weights["N"] - 1.0) + F - d) - F
        expected_P1 = g * (
            weights["N"] * a * (1.0 + F) ** 2
            - (a + d) - a * d * (2.0 + F) + F
        ) - F
        expected_q0 = 2.0 * (F * F - g * (a - F) * (d - F))

        self.assertAlmostEqual(c["p0"], expected_p0)
        self.assertAlmostEqual(c["P1"], expected_P1)
        self.assertAlmostEqual(c["q0"], expected_q0)
        self.assertEqual(c["ordering_failures"], 0)


if __name__ == "__main__":
    unittest.main()
