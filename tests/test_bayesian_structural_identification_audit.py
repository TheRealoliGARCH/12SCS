import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BayesianStructuralIdentificationAuditTests(unittest.TestCase):
    def test_current_pipeline_is_not_data_identified(self):
        subprocess.run(
            [sys.executable, "results/run_bayesian_structural_identification_audit.py"],
            cwd=ROOT,
            check=True,
        )
        path = ROOT / "results/bayesian_structural_identification_audit_v1.csv"
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["prior_specification_present"], "True")
        self.assertEqual(row["observed_outcome_data_present"], "False")
        self.assertEqual(row["likelihood_present"], "False")
        self.assertEqual(row["intervention_identification_strategy_present"], "False")
        self.assertEqual(row["data_identified"], "False")
        self.assertEqual(row["status"], "NOT_IDENTIFIED_FROM_DATA")


if __name__ == "__main__":
    unittest.main()
