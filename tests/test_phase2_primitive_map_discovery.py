import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Phase2PrimitiveMapDiscoveryTests(unittest.TestCase):
    def test_recovered_map_contract_and_reproducibility(self):
        script = 'results/run_phase2_primitive_map_discovery.py'
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        path = ROOT / 'results/phase2_primitive_map_discovery_v1.csv'
        first = path.read_bytes()
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding='utf-8')))
        self.assertEqual(len(rows), 10)
        by_object = {r['required_object']: r for r in rows}
        self.assertEqual(by_object['canonical_source_artifact']['discovery_status'], 'recovered')
        self.assertEqual(by_object['primitive_variable_list']['discovery_status'], 'recovered')
        for key in ['coefficient_A','coefficient_B','coefficient_C','coefficient_D','coefficient_E','coefficient_F']:
            self.assertEqual(by_object[key]['discovery_status'], 'recovered')
        self.assertEqual(by_object['primitive_domain']['discovery_status'], 'recovered')
        self.assertEqual(by_object['endogenous_signs']['discovery_status'], 'partially_derivable')
        self.assertIn('F>-1', by_object['primitive_domain']['boundary_statement'])
        self.assertIn('q2=', by_object['endogenous_signs']['boundary_statement'])
        self.assertEqual({r['inference_level'] for r in rows}, {'primitive_map_recovered_from_repository_history'})


if __name__ == '__main__':
    unittest.main()
