import csv
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Phase2MinimalAssumptionHierarchyTests(unittest.TestCase):
    def test_contract_and_reproducibility(self):
        script = 'results/run_phase2_minimal_assumption_hierarchy.py'
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        path = ROOT / 'results/phase2_minimal_assumption_hierarchy_v1.csv'
        first = path.read_bytes()
        subprocess.run([sys.executable, script], cwd=ROOT, check=True)
        self.assertEqual(first, path.read_bytes())
        rows = list(csv.DictReader(path.open(encoding='utf-8')))
        self.assertEqual(len(rows), 11)
        by_name = {r['theorem_component']: r for r in rows}
        required = {'basic_domain','p0_aggregate','S_nonnegative_aggregate','S_negative_aggregate','T_positive_aggregate','concave_minimal_branch','convex_minimal_branch','primitive_p0_refinement','primitive_S_negative_refinement','primitive_T_nonnegative_refinement','scope'}
        self.assertEqual(set(by_name), required)
        self.assertEqual(by_name['concave_minimal_branch']['classification'], 'minimal_branch')
        self.assertEqual(by_name['convex_minimal_branch']['classification'], 'minimal_branch')
        self.assertEqual(by_name['basic_domain']['classification'], 'endogenous')
        self.assertEqual({r['analysis'] for r in rows}, {'phase2_minimal_assumption_hierarchy'})
        self.assertEqual({r['inference_level'] for r in rows}, {'minimal_assumption_hierarchy'})


if __name__ == '__main__':
    unittest.main()
