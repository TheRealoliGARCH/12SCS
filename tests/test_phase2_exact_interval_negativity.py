import csv
import random
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def exact_certificate(p0, p1, p2):
    P0 = p0
    P1 = p0 + p1 + p2
    if p2 >= 0:
        return P0 < 0 and P1 < 0
    v = -p1 / (2 * p2)
    if 0 < v < 1:
        delta = p1 * p1 - 4 * p2 * p0
        return delta < 0
    return P0 < 0 and P1 < 0


def direct_max_negative(p0, p1, p2):
    pts = [0.0, 1.0]
    if p2 != 0:
        v = -p1 / (2 * p2)
        if 0 < v < 1:
            pts.append(v)
    return max(p0 + p1*x + p2*x*x for x in pts) < 0


class Phase2ExactIntervalNegativityTests(unittest.TestCase):
    def test_exact_certificate_matches_interval_maximum(self):
        rng = random.Random(1202)
        for _ in range(5000):
            p0 = rng.uniform(-5, 5)
            p1 = rng.uniform(-8, 8)
            p2 = rng.uniform(-5, 5)
            self.assertEqual(exact_certificate(p0,p1,p2), direct_max_negative(p0,p1,p2))

    def test_artifact_contract_and_reproducibility(self):
        script = 'results/run_phase2_exact_interval_negativity.py'
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        path = ROOT / 'results/phase2_exact_interval_negativity_v1.csv'
        first = path.read_bytes()
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding='utf-8')))
        self.assertEqual(len(rows), 8)
        names = {r['theorem_component'] for r in rows}
        self.assertEqual(names, {'convex_or_linear','concave_vertex_left','concave_vertex_right','concave_vertex_interior','vertex_location','vertex_value','structural_substitution','scope'})
        self.assertEqual(sum(r['classification']=='necessary_and_sufficient_branch' for r in rows), 4)
        self.assertEqual({r['inference_level'] for r in rows}, {'exact_interval_negativity'})


if __name__ == '__main__':
    unittest.main()
