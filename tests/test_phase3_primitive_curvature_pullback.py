import csv
import math
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Phase3PrimitiveCurvaturePullbackTests(unittest.TestCase):
    def test_exact_pullback_and_reproducibility(self):
        script = 'results/run_phase3_primitive_curvature_pullback.py'
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        path = ROOT / 'results/phase3_primitive_curvature_pullback_v1.csv'
        first = path.read_bytes()
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding='utf-8')))
        self.assertGreater(len(rows), 0)
        for r in rows:
            C, D, E, F, T = (float(r[k]) for k in ('C','D','E','F','T'))
            self.assertTrue(math.isclose(T, E-F*D+F*F*C, rel_tol=0.0, abs_tol=1e-12))
            self.assertIn(r['curvature_class'], {'strictly_convex','affine','strictly_concave'})
            self.assertEqual(r['analysis'], 'phase3_primitive_curvature_pullback')
            self.assertEqual(r['inference_level'], 'exact_primitive_pullback')

if __name__ == '__main__':
    unittest.main()
