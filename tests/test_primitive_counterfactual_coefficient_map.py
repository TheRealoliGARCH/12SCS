import csv, subprocess, sys
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
class PrimitiveCounterfactualCoefficientMapTests(unittest.TestCase):
    def test_exact_affine_map(self):
        subprocess.run([sys.executable,"results/run_primitive_counterfactual_coefficient_map.py"],cwd=ROOT,check=True)
        path=ROOT/"results/convergence_primitive_counterfactual_coefficient_map_v1.csv"
        rows=list(csv.DictReader(path.open(encoding="utf-8")))
        self.assertTrue(rows)
        for r in rows:
            D=float(r["D"]); E=float(r["E"]); F=float(r["F"])
            Ds=float(r["D_slope"]); Es=float(r["E_slope"]); Fs=float(r["F_slope"])
            for delta in (0.0,0.1,0.37,1.0):
                self.assertAlmostEqual(float(r["D"])+delta*Ds,D+delta*Ds,places=12)
                self.assertAlmostEqual(float(r["E"])+delta*Es,E+delta*Es,places=12)
                self.assertAlmostEqual(float(r["F"])+delta*Fs,F+delta*Fs,places=12)
        self.assertTrue(any(abs(float(r["D_slope"]))>0 or abs(float(r["E_slope"]))>0 or abs(float(r["F_slope"]))>0 for r in rows))

if __name__=="__main__": unittest.main()
