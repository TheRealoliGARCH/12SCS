import unittest
from pathlib import Path

from results.run_bayesian_v6_causal_audit import audit, load_v6


class BayesianV6CausalAuditTests(unittest.TestCase):
    def test_v6_has_variation_but_not_effect_identification(self):
        regimes = load_v6(Path("results/convergence_primitive_coefficient_map_v1.csv"))
        result = audit(regimes)
        # V6 contains thirteen active-set regimes in the reproducibility artifact.
        # The audit deliberately does not treat this small regime-level sample as
        # sufficient for a substantive causal-effect estimate.
        self.assertEqual(result.n, 13)
        self.assertTrue(result.treatment_varies)
        self.assertTrue(result.outcome_varies)
        self.assertTrue(result.positivity)
        self.assertTrue(result.temporal_ordering)
        self.assertFalse(result.adequate_sample_for_effect)


if __name__ == "__main__":
    unittest.main()
