import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCALES = [1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0]


class BayesianRDSummaryPriorSensitivityTests(unittest.TestCase):
    def test_prior_scale_grid_and_posterior_contract(self):
        subprocess.run([sys.executable, "results/run_rd_summary_bootstrap.py"], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "results/run_bayesian_rd_summary_prior_sensitivity.py"], cwd=ROOT, check=True)
        path = ROOT / "results/bayesian_rd_summary_prior_sensitivity_v1.csv"
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        self.assertEqual(len(rows), 21)
        self.assertEqual({r["country"] for r in rows}, {"Pakistan", "Israel", "North Korea"})
        self.assertEqual(sorted({float(r["prior_sd"]) for r in rows}), SCALES)
        for country in {r["country"] for r in rows}:
            subset = sorted((r for r in rows if r["country"] == country), key=lambda r: float(r["prior_sd"]))
            means = [abs(float(r["posterior_mean"])) for r in subset]
            self.assertTrue(all(a <= b + 1e-12 for a, b in zip(means, means[1:])))
            for r in subset:
                self.assertGreater(float(r["posterior_sd"]), 0.0)
                self.assertLessEqual(float(r["posterior_q025"]), float(r["posterior_median"]))
                self.assertLessEqual(float(r["posterior_median"]), float(r["posterior_q975"]))
                self.assertAlmostEqual(float(r["posterior_prob_negative"]) + float(r["posterior_prob_positive"]), 1.0, places=12)
                self.assertEqual(r["source_type"], "reported_estimate_and_standard_error")


if __name__ == "__main__":
    unittest.main()
