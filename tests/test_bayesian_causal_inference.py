import unittest

from results.run_bayesian_causal_inference import (
    Observation,
    posterior_parameters,
    posterior_summary,
)


class BayesianCausalInferenceTests(unittest.TestCase):
    def setUp(self):
        self.obs = [
            Observation(0, 0, 0, 35), Observation(0, 0, 1, 15),
            Observation(0, 1, 0, 25), Observation(0, 1, 1, 25),
            Observation(1, 0, 0, 30), Observation(1, 0, 1, 20),
            Observation(1, 1, 0, 20), Observation(1, 1, 1, 30),
        ]
        self.weights = [0.5, 0.5]

    def test_dirichlet_prior_is_explicit(self):
        alpha = posterior_parameters(self.obs, 2, prior=1.0)
        self.assertEqual(alpha[0], [36.0, 16.0, 26.0, 26.0])
        self.assertEqual(alpha[1], [31.0, 21.0, 21.0, 31.0])

    def test_posterior_summary_is_deterministic(self):
        a = posterior_summary(self.obs, self.weights, draws=2000, seed=123)
        b = posterior_summary(self.obs, self.weights, draws=2000, seed=123)
        self.assertEqual(a, b)
        self.assertGreater(a.ate_sd, 0.0)
        self.assertGreaterEqual(a.p_ate_positive, 0.0)
        self.assertLessEqual(a.p_ate_positive, 1.0)

    def test_validation_rejects_non_normalized_weights(self):
        with self.assertRaises(ValueError):
            posterior_summary(self.obs, [0.7, 0.7], draws=100)


if __name__ == "__main__":
    unittest.main()
