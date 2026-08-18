import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BayesianRDEstimationReadinessAuditTests(unittest.TestCase):
    def test_current_stack_is_not_estimation_ready_without_data_and_bandwidth(self):
        commands = [
            "results/run_bayesian_rd_data_contract.py",
            "results/run_bayesian_rd_likelihood_specification.py",
            "results/run_bayesian_rd_prior_specification.py",
            "results/run_bayesian_rd_estimation_readiness_audit.py",
        ]
        for command in commands:
            subprocess.run([sys.executable, command], cwd=ROOT, check=True)
        path = ROOT / "results/bayesian_rd_estimation_readiness_audit_v1.csv"
        rows = dict(csv.reader(path.open(encoding="utf-8")))
        self.assertEqual(rows["validated_rd_data"], "False")
        self.assertEqual(rows["likelihood_specified"], "True")
        self.assertEqual(rows["proper_priors_specified"], "True")
        self.assertEqual(rows["bandwidth_supplied"], "False")
        self.assertEqual(rows["estimation_ready"], "False")
        self.assertEqual(rows["status"], "RD_ESTIMATION_NOT_READY")


if __name__ == "__main__":
    unittest.main()
