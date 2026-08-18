import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BayesianRDDataContractTests(unittest.TestCase):
    def test_absent_input_is_reported_without_fabricating_data(self):
        data = ROOT / "results/bayesian_rd_input_v1.csv"
        if data.exists():
            data.unlink()
        subprocess.run([sys.executable, "results/run_bayesian_rd_data_contract.py"], cwd=ROOT, check=True)
        path = ROOT / "results/bayesian_rd_data_contract_v1.csv"
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertEqual(r["input_present"], "False")
        self.assertEqual(r["observation_count"], "0")
        self.assertEqual(r["cutoff_consistent"], "False")
        self.assertEqual(r["sharp_assignment_verified"], "False")
        self.assertEqual(r["status"], "RD_DATA_NOT_SUPPLIED")


if __name__ == "__main__":
    unittest.main()
