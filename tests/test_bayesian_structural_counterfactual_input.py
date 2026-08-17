import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BayesianStructuralCounterfactualInputTests(unittest.TestCase):
    def test_canonical_input_reconstructs_and_matches_map(self):
        subprocess.run(
            [sys.executable, "results/run_primitive_counterfactual_coefficient_map.py"],
            cwd=ROOT,
            check=True,
        )
        subprocess.run(
            [sys.executable, "results/run_bayesian_structural_counterfactual_input.py"],
            cwd=ROOT,
            check=True,
        )
        path = ROOT / "results/bayesian_structural_counterfactual_cells_v1.csv"
        self.assertTrue(path.exists())
        with path.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertTrue(rows)
        required = {
            "A", "B", "C", "D", "E", "F",
            "D_cf_unit", "E_cf_unit", "lambda_start", "lambda_end", "d"
        }
        self.assertTrue(required.issubset(rows[0]))
        for row in rows:
            for key in required:
                float(row[key])
            self.assertGreaterEqual(float(row["lambda_end"]), float(row["lambda_start"]))


if __name__ == "__main__":
    unittest.main()
