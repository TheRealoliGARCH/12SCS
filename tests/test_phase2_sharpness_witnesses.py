import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def max_on_unit_interval(p0, p1, p2):
    values = [p0, p0 + p1 + p2]
    if p2 < 0:
        v = -p1 / (2 * p2)
        if 0 < v < 1:
            values.append(p0 + p1 * v + p2 * v * v)
    return max(values)


class Phase2SharpnessWitnessTests(unittest.TestCase):
    def test_witnesses_and_reproducibility(self):
        script = 'results/run_phase2_sharpness_witnesses.py'
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        path = ROOT / 'results/phase2_sharpness_witnesses_v1.csv'
        first = path.read_bytes()
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding='utf-8')))
        self.assertEqual(len(rows), 7)
        witnesses = [r for r in rows if r['status'] == 'sharpness_witness']
        self.assertEqual(len(witnesses), 5)
        for r in witnesses:
            self.assertLess(max_on_unit_interval(float(r['p0']), float(r['p1']), float(r['p2'])), 0.0)
        self.assertEqual(rows[-1]['status'], 'scope')
        self.assertEqual({r['analysis'] for r in rows}, {'phase2_sharpness_witnesses'})


if __name__ == '__main__':
    unittest.main()
