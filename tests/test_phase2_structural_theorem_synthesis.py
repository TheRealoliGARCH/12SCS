import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Phase2StructuralTheoremSynthesisTests(unittest.TestCase):
    def test_contract_and_key_identities(self):
        script = 'results/run_phase2_structural_theorem_synthesis.py'
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        path = ROOT / 'results/phase2_structural_theorem_synthesis_v1.csv'
        first = path.read_bytes()
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding='utf-8')))
        self.assertEqual(len(rows), 10)
        by_name = {r['theorem_component']: r for r in rows}
        self.assertIn('curvature_bridge', by_name)
        self.assertIn('convex_endpoint_certificate', by_name)
        self.assertIn('concave_discriminant_certificate', by_name)
        self.assertEqual(by_name['curvature_bridge']['conclusion'], 'Delta_P=4*S*T=2*S*q0')
        self.assertEqual(by_name['degenerate_branch']['conclusion'], 'p1=p2=0 and Delta_P=0')
        self.assertEqual(by_name['curvature_neutral_branch']['conclusion'], 'Delta_P=0')
        self.assertEqual(sum(r['status'] == 'exact' for r in rows), 4)
        self.assertEqual(sum(r['status'] == 'sufficient' for r in rows), 3)


if __name__ == '__main__':
    unittest.main()
