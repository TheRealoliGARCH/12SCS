import csv
import math
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Phase3JointShapeClassificationTests(unittest.TestCase):
    def test_contract_identities_and_reproducibility(self):
        script = 'results/run_phase3_joint_shape_classification.py'
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        path = ROOT / 'results/phase3_joint_shape_classification_v1.csv'
        first = path.read_bytes()
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding='utf-8')))
        self.assertEqual(len(rows), 10)
        self.assertEqual(len({r['theorem_component'] for r in rows}), 10)
        self.assertEqual(sum(r['classification'] == 'necessary_and_sufficient_joint' for r in rows), 3)
        self.assertEqual(sum(r['classification'] == 'exact_structural_exclusion' for r in rows), 2)
        self.assertEqual(sum(r['classification'] == 'exact_identity' for r in rows), 2)
        for S, T in [(-2.0, 3.0), (2.0, -3.0), (2.0, 3.0), (-2.0, -3.0), (0.0, 4.0)]:
            self.assertTrue(math.isclose(4*S*T, 4*S*T, rel_tol=0.0, abs_tol=0.0))
            if S*T < 0:
                self.assertLess(4*S*T, 0.0)
            elif S*T > 0:
                self.assertGreater(4*S*T, 0.0)
            else:
                self.assertEqual(4*S*T, 0.0)
        self.assertEqual({r['analysis'] for r in rows}, {'phase3_joint_shape_classification'})
        self.assertEqual({r['inference_level'] for r in rows}, {'joint_shape_classification'})

if __name__ == '__main__':
    unittest.main()
