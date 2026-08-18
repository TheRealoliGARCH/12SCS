import csv, subprocess, sys
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class T(unittest.TestCase):
 def test_contract_and_reproducibility(self):
  s='results/run_phase3_unified_shape_theorem.py';subprocess.run([sys.executable,s],cwd=ROOT,check=True)
  p=ROOT/'results/phase3_unified_shape_theorem_v1.csv';first=p.read_bytes();subprocess.run([sys.executable,s],cwd=ROOT,check=True);self.assertEqual(first,p.read_bytes())
  rows=list(csv.DictReader(p.open(encoding='utf-8')));self.assertEqual(len(rows),12);self.assertEqual(len({r['theorem_component'] for r in rows}),12)
  counts={}
  for r in rows: counts[r['classification']]=counts.get(r['classification'],0)+1
  self.assertEqual(counts['exact_identity'],3);self.assertEqual(counts['necessary_and_sufficient_joint'],3);self.assertEqual(counts['scope_boundary'],1)
  self.assertEqual({r['analysis'] for r in rows},{'phase3_unified_shape_theorem'});self.assertEqual({r['inference_level'] for r in rows},{'unified_shape_theorem'})
if __name__=='__main__':unittest.main()
