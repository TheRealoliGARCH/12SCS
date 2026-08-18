import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Phase3PrimitiveCurvatureSharpnessTests(unittest.TestCase):
    def test_witnesses_and_reproducibility(self):
        script = 'results/run_phase3_primitive_curvature_sharpness.py'
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        path = ROOT / 'results/phase3_primitive_curvature_sharpness_v1.csv'
        first = path.read_bytes()
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding='utf-8')))
        self.assertEqual([r['witness_type'] for r in rows], ['strictly_convex','affine','strictly_concave'])
        for r in rows:
            if r['attainability'] == 'realized_by_primitive_map':
                C,D,E,F,T = (float(r[k]) for k in ('C','D','E','F','T'))
                self.assertAlmostEqual(T, E-F*D+F*F*C, places=12)
                if r['witness_type'] == 'strictly_convex': self.assertGreater(T, 0.0)
                elif r['witness_type'] == 'affine': self.assertEqual(T, 0.0)
                else: self.assertLess(T, 0.0)
            else:
                self.assertEqual(r['attainability'], 'not_witnessed_in_current_map')
        self.assertEqual({r['analysis'] for r in rows}, {'phase3_primitive_curvature_sharpness'})
        self.assertEqual({r['inference_level'] for r in rows}, {'constructive_primitive_witness'})

if __name__ == '__main__':
    unittest.main()
