import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BayesianRDSummaryHierarchicalLeaveOneOutTests(unittest.TestCase):
    def test_leave_one_out_contract_and_reproducibility(self):
        subprocess.run([sys.executable, "results/run_rd_summary_bootstrap.py"], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "results/run_bayesian_rd_summary_hierarchical_leave_one_out.py"], cwd=ROOT, check=True)
        path = ROOT / "results/bayesian_rd_summary_hierarchical_leave_one_out_v1.csv"
        first = path.read_bytes()
        subprocess.run([sys.executable, "results/run_bayesian_rd_summary_hierarchical_leave_one_out.py"], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        self.assertEqual(len(rows), 3)
        self.assertEqual({r["omitted_country"] for r in rows}, {"Pakistan", "Israel", "North Korea"})
        for r in rows:
            self.assertEqual(int(r["included_country_count"]), 2)
            self.assertGreater(float(r["posterior_mu_sd"]), 0.0)
            self.assertLessEqual(float(r["posterior_mu_q025_normal_approx"]), float(r["posterior_mu_median_approx"]))
            self.assertLessEqual(float(r["posterior_mu_median_approx"]), float(r["posterior_mu_q975_normal_approx"]))
            self.assertGreaterEqual(float(r["posterior_kappa_mean"]), 0.0)
            self.assertAlmostEqual(float(r["posterior_mu_prob_negative"]) + float(r["posterior_mu_prob_positive"]), 1.0, places=12)
            self.assertEqual(r["source_type"], "reported_estimate_and_standard_error")
            self.assertEqual(r["inference_level"], "summary_data_hierarchical_leave_one_out")


if __name__ == "__main__":
    unittest.main()
