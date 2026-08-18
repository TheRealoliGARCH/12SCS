import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RDSummaryBootstrapTests(unittest.TestCase):
    def test_bootstrap_output_is_complete_and_reproducible(self):
        command = [sys.executable, "results/run_rd_summary_bootstrap.py"]
        subprocess.run(command, cwd=ROOT, check=True)
        path = ROOT / "results/rd_summary_bootstrap_v1.csv"
        first = path.read_text(encoding="utf-8")
        subprocess.run(command, cwd=ROOT, check=True)
        second = path.read_text(encoding="utf-8")
        self.assertEqual(first, second)
        rows = list(csv.DictReader(path.open(encoding="utf-8")))
        self.assertEqual(len(rows), 3)
        self.assertEqual({r["country"] for r in rows}, {"Pakistan", "Israel", "North Korea"})
        for r in rows:
            self.assertEqual(int(r["bootstrap_reps"]), 10000)
            self.assertGreater(float(r["standard_error"]), 0.0)
            self.assertLessEqual(float(r["q025"]), float(r["median"]))
            self.assertLessEqual(float(r["median"]), float(r["q975"]))
            self.assertGreaterEqual(float(r["prob_negative"]), 0.0)
            self.assertLessEqual(float(r["prob_negative"]), 1.0)
            self.assertGreaterEqual(float(r["prob_positive"]), 0.0)
            self.assertLessEqual(float(r["prob_positive"]), 1.0)
            self.assertAlmostEqual(
                float(r["prob_negative"]) + float(r["prob_positive"]), 1.0, places=12
            )
            self.assertEqual(r["source_type"], "reported_estimate_and_standard_error")


if __name__ == "__main__":
    unittest.main()
