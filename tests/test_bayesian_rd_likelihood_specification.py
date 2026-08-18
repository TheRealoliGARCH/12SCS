import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class BayesianRDLikelihoodSpecificationTests(unittest.TestCase):
    def test_likelihood_is_specified_but_not_estimation_ready(self):
        subprocess.run([sys.executable,"results/run_bayesian_rd_likelihood_specification.py"],cwd=ROOT,check=True)
        p=ROOT/"results/bayesian_rd_likelihood_specification_v1.csv"
        rows=list(csv.DictReader(p.open(encoding="utf-8")))
        self.assertEqual(len(rows),13)
        specified={r["component"]:r["specified"] for r in rows}
        for key in ("model_family","outcome","running_variable","cutoff","treatment","local_window","conditional_mean","noise","causal_estimand","posterior"):
            self.assertEqual(specified[key],"True")
        for key in ("observed_data_required","prior_hyperparameters_supplied","bandwidth_supplied"):
            self.assertEqual(specified[key],"False")

if __name__=="__main__": unittest.main()
