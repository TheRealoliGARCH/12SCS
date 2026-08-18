import csv, subprocess, sys
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class Phase3ClosureConsistencyAuditTests(unittest.TestCase):
 def test_contract_and_reproducibility(self):
  script='results/run_phase3_closure_consistency_audit.py'
  subprocess.run([sys.executable,script],cwd=ROOT,check=True)
  p=ROOT/'results/phase3_closure_consistency_audit_v1.csv';first=p.read_bytes()
  subprocess.run([sys.executable,script],cwd=ROOT,check=True);self.assertEqual(first,p.read_bytes())
  rows=list(csv.DictReader(p.open(encoding='utf-8')))
  self.assertEqual(len(rows),20)
  self.assertEqual({r['analysis'] for r in rows},{'phase3_closure_consistency_audit'})
  self.assertEqual({r['inference_level'] for r in rows},{'phase3_closure_audit'})
  for target in ['exact_curvature','critical_point_root_geometry','primitive_curvature_pullback','primitive_curvature_sharpness','unified_shape_theorem']:
   self.assertEqual(sum(r['audit_target']==target for r in rows),3)
  cross={r['check'] for r in rows if r['audit_target']=='cross_artifact'}
  self.assertEqual(cross,{'curvature_identity','pullback_identity','discriminant_identity','zero_curvature_boundary','scope_boundary'})
if __name__=='__main__':unittest.main()
