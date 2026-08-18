import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BayesianRDSummaryHierarchicalInfluenceTests(unittest.TestCase):
    def test_influence_contract_and_reproducibility(self):
        for script in [
            "results/run_rd_summary_bootstrap.py",
            "results/run_bayesian_rd_summary_hierarchical_pooling.py",
            "results/run_bayesian_rd_summary_hierarchical_leave_one_out.py",
            "results/run_bayesian_rd_summary_hierarchical_influence.py",
        ]:
            subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        path = ROOT / "results/bayesian_rd_summary_hierarchical_influence_v1.csv"
        first = path.read_bytes()
        subprocess.run([sys.executable, "results/run_bayesian_rd_summary_hierarchical_influence.py"], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        self.assertEqual(len(rows), 3)
        self.assertEqual({r["omitted_country"] for r in rows}, {"Pakistan", "Israel", "North Korea"})
        for r in rows:
            full_mu = float(r["full_posterior_mu_mean"])
            loo_mu = float(r["leave_one_out_posterior_mu_mean"])
            full_sd = float(r["full_posterior_mu_sd"])
            loo_sd = float(r["leave_one_out_posterior_mu_sd"])
            self.assertGreater(full_sd, 0.0)
            self.assertGreater(loo_sd, 0.0)
            self.assertAlmostEqual(float(r["delta_posterior_mu_mean"]), loo_mu - full_mu, places=12)
            self.assertAlmostEqual(float(r["delta_posterior_mu_sd"]), loo_sd - full_sd, places=12)
            self.assertAlmostEqual(float(r["standardized_mean_shift_full_sd"]), (loo_mu - full_mu) / full_sd, places=12)
            self.assertAlmostEqual(float(r["absolute_mean_shift"]), abs(loo_mu - full_mu), places=12)
            p0 = float(r["full_posterior_mu_prob_negative"])
            p1 = float(r["leave_one_out_posterior_mu_prob_negative"])
            self.assertTrue(0.0 <= p0 <= 1.0)
            self.assertTrue(0.0 <= p1 <= 1.0)
            self.assertAlmostEqual(float(r["delta_posterior_mu_prob_negative"]), p1 - p0, places=12)
            self.assertAlmostEqual(float(r["absolute_sign_probability_shift"]), abs(p1 - p0), places=12)
            self.assertEqual(r["source_type"], "reported_estimate_and_standard_error")
            self.assertEqual(r["inference_level"], "summary_data_hierarchical_influence")


if __name__ == "__main__":
    unittest.main()
