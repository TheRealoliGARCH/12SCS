import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Phase2PrimitiveRealizabilityTests(unittest.TestCase):
    def test_structural_filter_and_reproducibility(self):
        script = 'results/run_phase2_primitive_realizability.py'
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        path = ROOT / 'results/phase2_primitive_realizability_v1.csv'
        first = path.read_bytes()
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding='utf-8')))
        self.assertEqual(len(rows), 7)
        checked = [r for r in rows if r['status'] in {'passes_structural_filter','fails_structural_filter'}]
        self.assertEqual(len(checked), 5)
        for r in checked:
            p1, p2 = float(r['p1']), float(r['p2'])
            if abs(p1) < 1e-15:
                self.assertEqual(r['status'], 'fails_structural_filter')
                self.assertNotEqual(p2, 0.0)
            else:
                F = 2.0*p2/p1
                self.assertGreater(F, -1.0)
                self.assertEqual(r['status'], 'passes_structural_filter')
        self.assertEqual({r['analysis'] for r in rows}, {'phase2_primitive_realizability'})
        self.assertEqual({r['inference_level'] for r in rows}, {'structural_realizability_filter'})

if __name__ == '__main__':
    unittest.main()
