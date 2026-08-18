import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Phase2EndogenousSignTheoremSynthesisTests(unittest.TestCase):
    def test_contract_and_reproducibility(self):
        script = 'results/run_phase2_endogenous_sign_theorem_synthesis.py'
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        path = ROOT / 'results/phase2_endogenous_sign_theorem_synthesis_v1.csv'
        first = path.read_bytes()
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding='utf-8')))
        self.assertEqual(len(rows), 9)
        by_name = {r['theorem_component']: r for r in rows}
        self.assertEqual(by_name['basic_B_sign']['status'], 'endogenous')
        self.assertEqual(by_name['p0_negative']['conclusion'], 'p0=B+D-F*C<0')
        self.assertEqual(by_name['S_nonnegative']['conclusion'], 'S=F*B+E>=0')
        self.assertIn('T=E-F*D+F^2*C>=0', by_name['T_nonnegative']['conclusion'])
        self.assertEqual(by_name['concave_global_negative']['conclusion'], 'p2=F*S<0 and Delta_P=4*S*T<0')
        self.assertEqual(by_name['convex_endpoint_negative']['conclusion'], 'p2>=0 and P(0)<0 and P(1)<0')
        self.assertEqual(sum(r['status'] == 'sufficient' for r in rows), 6)
        self.assertEqual({r['inference_level'] for r in rows}, {'primitive_sufficient_sign_theorem'})

if __name__ == '__main__':
    unittest.main()
