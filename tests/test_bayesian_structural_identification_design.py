import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BayesianStructuralIdentificationDesignTests(unittest.TestCase):
    def test_design_reports_exact_missing_identification_components(self):
        subprocess.run([sys.executable, "results/run_bayesian_structural_identification_design.py"], cwd=ROOT, check=True)
        path = ROOT / "results/bayesian_structural_identification_design_v1.csv"
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        present = {r["component"]: r["present"] for r in rows}
        self.assertEqual(present["structural_map"], "True")
        self.assertEqual(present["prior"], "True")
        for name in ["observed_outcome_data", "likelihood", "consistency", "exchangeability_or_design", "positivity_or_support"]:
            self.assertEqual(present[name], "False")


if __name__ == "__main__":
    unittest.main()
