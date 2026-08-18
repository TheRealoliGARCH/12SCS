import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Phase2PrimitiveSignRestrictionsTests(unittest.TestCase):
    def test_contract_identities_and_boundary(self):
        script = 'results/run_phase2_primitive_sign_restrictions.py'
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        path = ROOT / 'results/phase2_primitive_sign_restrictions_v1.csv'
        first = path.read_bytes()
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding='utf-8')))
        self.assertEqual(len(rows), 17)
        by_quantity = {r['quantity']: r for r in rows}
        self.assertEqual(by_quantity['p0']['primitive_expression_or_condition'], 'sum_i w_i*g_i*a_i-sum_i g_i*(a_i+d_i)-d_m*(B0-sum_i g_i)')
        self.assertEqual(by_quantity['S']['primitive_expression_or_condition'], 'd_m*sum_i w_i*g_i*a_i-sum_i g_i*a_i*d_i')
        self.assertEqual(by_quantity['T']['primitive_expression_or_condition'], '-sum_i g_i*a_i*d_i+d_m*sum_i g_i*(a_i+d_i)+d_m^2*(B0-sum_i g_i)')
        self.assertEqual(by_quantity['q0']['primitive_expression_or_condition'], '2*T')
        self.assertEqual(by_quantity['Delta_P']['primitive_expression_or_condition'], '4*S*T=2*S*q0')
        self.assertEqual(by_quantity['F>-1']['classification'], 'endogenous')
        for key in ['sign(p0)', 'sign(S)', 'sign(T)']:
            self.assertEqual(by_quantity[key]['classification'], 'not_derivable')
        self.assertEqual(sum(r['classification'] == 'identity' for r in rows), 10)
        self.assertEqual(sum(r['classification'] == 'additional_assumption' for r in rows), 3)
        self.assertEqual({r['inference_level'] for r in rows}, {'primitive_to_structural_sign_classification'})


if __name__ == '__main__':
    unittest.main()
