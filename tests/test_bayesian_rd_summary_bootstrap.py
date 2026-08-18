import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BayesianRDSummaryBootstrapTests(unittest.TestCase):
    def test_summary_bootstrap_is_complete_and_directionally_consistent(self):
        subprocess.run([sys.executable, "results/run_bayesian_rd_summary_bootstrap.py"], cwd=ROOT, check=True)
        path = ROOT / "results/bayesian_rd_summary_bootstrap_v1.csv"
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        self.assertEqual(len(rows), 3)
        by_unit = {r["unit"]: r for r in rows}
        self.assertEqual(set(by_unit), {"Pakistan", "Israel", "North_Korea"})
        for row in rows:
            self.assertEqual(int(row["bootstrap_replicates"]), 10000)
            self.assertLess(float(row["q025"]), float(row["q500"]))
            self.assertLess(float(row["q500"]), float(row["q975"]))
            self.assertAlmostEqual(float(row["prob_negative"]) + float(row["prob_positive"]), 1.0, places=12)
        self.assertGreater(float(by_unit["Pakistan"]["prob_negative"]), 0.95)
        self.assertGreater(float(by_unit["Israel"]["prob_positive"]), 0.95)
        self.assertGreater(float(by_unit["North_Korea"]["prob_positive"]), 0.95)


if __name__ == "__main__":
    unittest.main()
