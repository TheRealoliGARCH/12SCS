import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class BayesianStructuralCounterfactualAuditTests(unittest.TestCase):
    def test_prior_pushforward_is_affine_and_sensitivity_is_exact(self):
        subprocess.run([sys.executable, "results/run_bayesian_structural_counterfactual_input.py"], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "results/run_bayesian_structural_counterfactual_audit.py"], cwd=ROOT, check=True)
        path = ROOT / "results/bayesian_structural_counterfactual_audit_v1.csv"
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        self.assertEqual(len(rows), 3)
        self.assertEqual({(float(r["prior_a"]), float(r["prior_b"])) for r in rows}, {(5.0,45.0),(10.0,90.0),(20.0,180.0)})
        means = [float(r["mean_delta"]) for r in rows]
        variances = [float(r["var_delta"]) for r in rows]
        contrasts = [float(r["mean_contrast"]) for r in rows]
        self.assertTrue(all(abs(x-0.1) < 1e-15 for x in means))
        self.assertGreater(variances[0], variances[1])
        self.assertGreater(variances[1], variances[2])
        self.assertLess(max(contrasts)-min(contrasts), 1e-15)

if __name__ == "__main__":
    unittest.main()
