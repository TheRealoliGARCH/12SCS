import csv, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ConstructivePrimitiveWitnessTests(unittest.TestCase):
 def test_lifts_and_reproducibility(self):
  script='results/run_phase2_constructive_primitive_witnesses.py'
  subprocess.run([sys.executable,script],cwd=ROOT,check=True)
  p=ROOT/'results/phase2_constructive_primitive_witnesses_v1.csv'; first=p.read_bytes()
  subprocess.run([sys.executable,script],cwd=ROOT,check=True); self.assertEqual(first,p.read_bytes())
  rows=list(csv.DictReader(p.open(encoding='utf-8'))); self.assertEqual(len(rows),3)
  realized=[r for r in rows if r['status']=='constructively_realized']; self.assertEqual(len(realized),2)
  for r in realized:
   g,a,w,d,B0,F=map(float,[r[k] for k in ['g','a','w','d','B0','F']])
   B=w*g*a; C=B0-g; D=-g*(a+d); E=-g*a*d
   self.assertEqual((B,C,D,E),(float(r['B']),float(r['C']),float(r['D']),float(r['E'])))
   self.assertEqual((B+D-F*C,2*(F*B+E),F*(F*B+E)),(float(r['p0']),float(r['p1']),float(r['p2'])))
   self.assertGreaterEqual(g,0); self.assertGreaterEqual(w,0); self.assertGreaterEqual(a,-1); self.assertLessEqual(a,0); self.assertGreater(F,-1)
  self.assertEqual({r['analysis'] for r in rows},{'phase2_constructive_primitive_witnesses'})
if __name__=='__main__': unittest.main()
