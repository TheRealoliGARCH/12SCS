import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BayesianRDSummaryHierarchicalPPCTests(unittest.TestCase):
    def test_ppc_contract_and_reproducibility(self):
        subprocess.run([sys.executable, "results/run_rd_summary_bootstrap.py"], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "results/run_bayesian_rd_summary_hierarchical_ppc.py"], cwd=ROOT, check=True)
        path = ROOT / "results/bayesian_rd_summary_hierarchical_ppc_v1.csv"
        first = path.read_bytes()
        subprocess.run([sys.executable, "results/run_bayesian_rd_summary_hierarchical_ppc.py"], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        self.assertEqual(len(rows), 5)
        self.assertEqual({r["country"] for r in rows if r["scope"] == "country"}, {"Pakistan", "Israel", "North Korea"})
        self.assertEqual(sum(r["scope"] == "global" for r in rows), 1)
        self.assertEqual(sum(r["scope"] == "global_range" for r in rows), 1)
        for r in rows:
            p = float(r["two_sided_predictive_tail_probability"])
            self.assertGreaterEqual(p, 0.0)
            self.assertLessEqual(p, 1.0)
            self.assertEqual(r["source_type"], "reported_estimate_and_standard_error")
            self.assertEqual(r["inference_level"], "summary_data_hierarchical_ppc")


if __name__ == "__main__":
    unittest.main()
