import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Phase2SharpnessClassificationTests(unittest.TestCase):
    def test_contract_and_reproducibility(self):
        script = 'results/run_phase2_sharpness_classification.py'
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        path = ROOT / 'results/phase2_sharpness_classification_v1.csv'
        first = path.read_bytes()
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding='utf-8')))
        self.assertEqual(len(rows), 9)
        by_name = {r['theorem_component']: r for r in rows}
        self.assertEqual(len(by_name), 9)
        self.assertEqual(by_name['exact_interval_negativity']['classification'], 'necessary_and_sufficient')
        self.assertEqual(sum(r['classification'] == 'sufficient_not_necessary' for r in rows), 2)
        self.assertEqual(sum(r['classification'] == 'constructively_nonnecessary' for r in rows), 3)
        self.assertEqual(sum(r['classification'] == 'structurally_unrealizable' for r in rows), 1)
        self.assertEqual(sum(r['classification'] == 'coefficient_level_nonnecessary' for r in rows), 1)
        self.assertEqual(sum(r['classification'] == 'scope' for r in rows), 1)
        self.assertEqual({r['analysis'] for r in rows}, {'phase2_sharpness_classification'})
        self.assertEqual({r['inference_level'] for r in rows}, {'sharpness_classification'})

if __name__ == '__main__':
    unittest.main()
