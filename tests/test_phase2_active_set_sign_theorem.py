import unittest

from results.phase2_active_set_sign_theorem import (
    PrimitiveCell,
    aggregate_certificates,
    ordering_holds,
    simple_sufficient_conditions,
)


class Phase2ActiveSetSignTests(unittest.TestCase):
    def test_certificates_match_direct_formula(self):
        cells = [
            PrimitiveCell(gap=0.20, weight=1.2, a=-0.20, d=0.40),
            PrimitiveCell(gap=0.10, weight=1.1, a=-0.30, d=0.50),
        ]
        F = 0.60
        budget = 1.0
        c = aggregate_certificates(cells, budget, F)
        self.assertAlmostEqual(c["p0_margin"], F * budget - sum(
            x.gap * (x.weight*x.a - x.a - x.d + F) for x in cells))
        self.assertAlmostEqual(c["P1_margin"], F * budget - sum(
            x.gap * (x.weight*x.a*(1+F)**2 - (x.a+x.d)
                     - x.a*x.d*(2+F) + F) for x in cells))
        self.assertAlmostEqual(c["q0"], 2*c["q0_half"])

    def test_ordering_and_cellwise_signs(self):
        # The previous d=0.4 fixture satisfied the ordering but not the p0
        # cellwise condition.  This fixture satisfies all three conditions.
        cell = PrimitiveCell(gap=0.2, weight=1.2, a=-0.2, d=0.8)
        F = 0.6
        self.assertTrue(ordering_holds(cell, F))
        signs = simple_sufficient_conditions(F, cell)
        self.assertTrue(signs["p0_cell_nonpositive"])
        self.assertTrue(signs["P1_cell_nonpositive"])
        self.assertTrue(signs["q0_cell_safe"])


if __name__ == "__main__":
    unittest.main()
