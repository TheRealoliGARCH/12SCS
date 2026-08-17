import unittest
from pathlib import Path

from results.run_bayesian_v6_causal_audit import audit, load_v6


class BayesianV6CausalAuditTests(unittest.TestCase):
    def test_v6_has_variation_but_not_effect_identification(self):
        # Unit tests must not depend on generated workflow artifacts.  The
        # deterministic fixture mirrors the V6 regime-level schema and retains
        # the identification properties being tested.
        fixture = Path(__file__).parent / "fixtures" / "v6_causal_audit.csv"
        regimes = load_v6(fixture)
        result = audit(regimes)
        self.assertEqual(result.n, 13)
        self.assertTrue(result.treatment_varies)
        self.assertTrue(result.outcome_varies)
        self.assertTrue(result.positivity)
        self.assertTrue(result.temporal_ordering)
        self.assertFalse(result.adequate_sample_for_effect)


if __name__ == "__main__":
    unittest.main()
