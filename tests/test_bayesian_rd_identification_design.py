import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BayesianRDIdentificationDesignTests(unittest.TestCase):
    def test_rd_design_reports_selected_route_and_missing_requirements(self):
        subprocess.run([sys.executable, "results/run_bayesian_rd_identification_design.py"], cwd=ROOT, check=True)
        path = ROOT / "results/bayesian_rd_identification_design_v1.csv"
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        self.assertEqual(len(rows), 10)
        present = {r["component"]: r["present"] for r in rows}
        formal = {r["component"]: r["formalization"] for r in rows}
        self.assertEqual(present["design"], "True")
        self.assertEqual(formal["design"], "regression_discontinuity")
        for key in ("running_variable", "cutoff", "treatment_rule", "outcome", "local_likelihood", "continuity", "no_precise_manipulation", "local_support", "bandwidth_or_local_model"):
            self.assertEqual(present[key], "False")


if __name__ == "__main__":
    unittest.main()
