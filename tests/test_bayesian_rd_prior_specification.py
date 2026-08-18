import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BayesianRDPriorSpecificationTests(unittest.TestCase):
    def test_all_rd_parameters_have_proper_priors(self):
        subprocess.run([sys.executable, "results/run_bayesian_rd_prior_specification.py"], cwd=ROOT, check=True)
        path = ROOT / "results/bayesian_rd_prior_specification_v1.csv"
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        self.assertEqual(len(rows), 5)
        priors = {r["parameter"]: r for r in rows}
        self.assertEqual(set(priors), {"alpha", "tau", "beta", "gamma", "sigma"})
        for parameter in priors:
            self.assertEqual(priors[parameter]["proper"], "True")
            self.assertGreater(float(priors[parameter]["scale"]), 0.0)
        for parameter in ("alpha", "tau", "beta", "gamma"):
            self.assertEqual(priors[parameter]["family"], "Normal")
        self.assertEqual(priors["sigma"]["family"], "HalfNormal")


if __name__ == "__main__":
    unittest.main()
