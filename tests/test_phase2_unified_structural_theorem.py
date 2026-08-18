import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Phase2UnifiedStructuralTheoremTests(unittest.TestCase):
    def test_contract_and_reproducibility(self):
        script = 'results/run_phase2_unified_structural_theorem.py'
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        path = ROOT / 'results/phase2_unified_structural_theorem_v1.csv'
        first = path.read_bytes()
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding='utf-8')))
        self.assertEqual(len(rows), 10)
        names = [r['theorem_component'] for r in rows]
        self.assertEqual(len(set(names)), 10)
        by_name = {r['theorem_component']: r for r in rows}
        self.assertEqual(by_name['exact_interval_theorem']['classification'], 'necessary_and_sufficient')
        self.assertEqual(sum(r['classification'] == 'exact_identity' for r in rows), 3)
        self.assertEqual(sum(r['classification'] == 'sufficient_not_necessary' for r in rows), 2)
        self.assertEqual(sum(r['classification'] == 'scope_boundary' for r in rows), 1)
        self.assertEqual({r['analysis'] for r in rows}, {'phase2_unified_structural_theorem'})
        self.assertEqual({r['inference_level'] for r in rows}, {'phase2_unified_structural_theorem'})

if __name__ == '__main__':
    unittest.main()
