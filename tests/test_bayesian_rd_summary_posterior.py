import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BayesianRDSummaryPosteriorTests(unittest.TestCase):
    def test_conjugate_summary_posteriors(self):
        subprocess.run([sys.executable, "results/run_rd_summary_bootstrap.py"], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "results/run_bayesian_rd_summary_posterior.py"], cwd=ROOT, check=True)
        path = ROOT / "results/bayesian_rd_summary_posterior_v1.csv"
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        self.assertEqual(len(rows), 3)
        self.assertEqual({r["country"] for r in rows}, {"Pakistan", "Israel", "North Korea"})
        for r in rows:
            estimate = float(r["estimate"])
            post_mean = float(r["posterior_mean"])
            post_sd = float(r["posterior_sd"])
            self.assertGreater(post_sd, 0.0)
            self.assertLess(abs(post_mean), abs(estimate))
            self.assertLessEqual(float(r["posterior_q025"]), float(r["posterior_median"]))
            self.assertLessEqual(float(r["posterior_median"]), float(r["posterior_q975"]))
            pneg = float(r["posterior_prob_negative"])
            ppos = float(r["posterior_prob_positive"])
            self.assertGreaterEqual(pneg, 0.0)
            self.assertLessEqual(pneg, 1.0)
            self.assertAlmostEqual(pneg + ppos, 1.0, places=12)
            self.assertEqual(r["source_type"], "reported_estimate_and_standard_error")


if __name__ == "__main__":
    unittest.main()
