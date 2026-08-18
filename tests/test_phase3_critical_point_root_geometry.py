import csv
import math
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Phase3CriticalPointRootGeometryTests(unittest.TestCase):
    def test_contract_identities_and_reproducibility(self):
        script = 'results/run_phase3_critical_point_root_geometry.py'
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        path = ROOT / 'results/phase3_critical_point_root_geometry_v1.csv'
        first = path.read_bytes()
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding='utf-8')))
        self.assertEqual(len(rows), 10)
        self.assertEqual(len({r['theorem_component'] for r in rows}), 10)
        self.assertEqual(sum(r['classification'] == 'exact_identity' for r in rows), 3)
        self.assertEqual(sum(r['classification'] == 'necessary_and_sufficient_discriminant_regime' for r in rows), 2)
        self.assertEqual(sum(r['classification'] == 'exact_boundary' for r in rows), 1)
        self.assertEqual(sum(r['classification'] == 'necessary_and_sufficient_interval_condition' for r in rows), 1)
        self.assertEqual(sum(r['classification'] == 'exact_structural_boundary' for r in rows), 1)
        self.assertEqual(sum(r['classification'] == 'scope_boundary' for r in rows), 1)
        for F, p0, S in [(1.0, -2.0, 3.0), (-0.5, -1.0, 2.0), (0.0, -3.0, 4.0)]:
            T = S - F*p0
            disc = 4*S*T
            self.assertTrue(math.isclose(disc, 4*S*T, abs_tol=1e-12))
            if F*S != 0 and S*T >= 0:
                r1 = (-S + math.sqrt(S*T))/(F*S)
                r2 = (-S - math.sqrt(S*T))/(F*S)
                for r in (r1, r2):
                    p = p0 + 2*S*r + F*S*r*r
                    self.assertTrue(math.isclose(p, 0.0, abs_tol=1e-10))
        for F, p0 in [(0.0, -2.0), (1.0, -2.0), (-0.5, 3.0)]:
            S = F*p0
            T = S - F*p0
            self.assertTrue(math.isclose(T, 0.0, abs_tol=1e-12))
            for x in (0.0, 0.25, 0.5, 0.75, 1.0):
                p = p0 + 2*S*x + F*S*x*x
                self.assertTrue(math.isclose(p, p0*(1+F*x)**2, abs_tol=1e-12))
        self.assertEqual({r['analysis'] for r in rows}, {'phase3_critical_point_root_geometry'})
        self.assertEqual({r['inference_level'] for r in rows}, {'critical_point_root_geometry'})

if __name__ == '__main__':
    unittest.main()
