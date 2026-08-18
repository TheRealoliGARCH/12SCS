import csv
import math
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Phase3ExactCurvatureTheoremTests(unittest.TestCase):
    def test_contract_identities_and_reproducibility(self):
        script = 'results/run_phase3_exact_curvature_theorem.py'
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        path = ROOT / 'results/phase3_exact_curvature_theorem_v1.csv'
        first = path.read_bytes()
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding='utf-8')))
        self.assertEqual(len(rows), 10)
        self.assertEqual(len({r['theorem_component'] for r in rows}), 10)
        self.assertEqual(sum(r['classification'] == 'exact_identity' for r in rows), 3)
        self.assertEqual(sum(r['classification'] == 'necessary_and_sufficient' for r in rows), 3)
        self.assertEqual(sum(r['classification'] == 'structural_consequence' for r in rows), 1)
        # Independent deterministic algebra checks for representative values.
        for F, p0, S in [(0.0, -1.0, 2.0), (1.0, -3.0, -1.0), (-0.5, -2.0, 4.0)]:
            p1, p2 = 2*S, F*S
            T = S - F*p0
            for x in (0.0, 0.25, 0.5, 0.75, 1.0):
                q = (p1 - 2*F*p0) + (2*p2 - F*p1)*x
                self.assertTrue(math.isclose(q, 2*T, rel_tol=0.0, abs_tol=1e-12))
        self.assertEqual({r['analysis'] for r in rows}, {'phase3_exact_curvature_theorem'})
        self.assertEqual({r['inference_level'] for r in rows}, {'phase3_exact_curvature_theorem'})

if __name__ == '__main__':
    unittest.main()
