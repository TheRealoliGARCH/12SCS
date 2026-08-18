import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BayesianRDSummaryHierarchicalPoolingTests(unittest.TestCase):
    def test_hierarchical_summary_pool_contract(self):
        subprocess.run([sys.executable, "results/run_rd_summary_bootstrap.py"], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "results/run_bayesian_rd_summary_hierarchical_pooling.py"], cwd=ROOT, check=True)
        path = ROOT / "results/bayesian_rd_summary_hierarchical_pooling_v1.csv"
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertEqual(r["analysis"], "three_country_summary_pool")
        self.assertEqual(int(r["country_count"]), 3)
        self.assertGreater(float(r["mu_prior_sd"]), 0.0)
        self.assertEqual(r["kappa_prior_family"], "HalfNormal")
        self.assertGreater(float(r["kappa_prior_sd"]), 0.0)
        self.assertGreater(int(r["kappa_grid_size"]), 100)
        self.assertGreater(float(r["posterior_mu_sd"]), 0.0)
        self.assertGreaterEqual(float(r["posterior_kappa_mean"]), 0.0)
        self.assertLessEqual(float(r["posterior_mu_q025_normal_approx"]), float(r["posterior_mu_median_approx"]))
        self.assertLessEqual(float(r["posterior_mu_median_approx"]), float(r["posterior_mu_q975_normal_approx"]))
        self.assertAlmostEqual(float(r["posterior_mu_prob_negative"]) + float(r["posterior_mu_prob_positive"]), 1.0, places=12)
        self.assertEqual(r["source_type"], "reported_estimate_and_standard_error")
        self.assertEqual(r["inference_level"], "summary_data_not_observation_level_rd")


if __name__ == "__main__":
    unittest.main()
