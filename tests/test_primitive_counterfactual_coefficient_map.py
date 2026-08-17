import csv, subprocess, sys
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from model.convergence_analysis import CAPABILITIES, STATES
from model.heterogeneous_scenario import build_scenario

def read_matrix(path):
    with path.open(encoding="utf-8",newline="") as f: rows=list(csv.reader(f))
    return {r[0]:{c:float(r[j+1]) for j,c in enumerate(CAPABILITIES)} for r in rows[1:]}

def read_vector(path):
    with path.open(encoding="utf-8",newline="") as f: rows=list(csv.reader(f))
    return {r[0]:float(r[1]) for r in rows[1:]}

class PrimitiveCounterfactualCoefficientMapTests(unittest.TestCase):
    def test_exact_affine_map(self):
        gap_file=ROOT/"results/capability_gap_positive_v2.csv"
        weight_file=ROOT/"results/capability_dispersion_weights_v2.csv"
        if not gap_file.exists() or not weight_file.exists():
            subprocess.run([sys.executable,"results/run_gap_priority.py"],cwd=ROOT,check=True)
        subprocess.run([sys.executable,"results/run_primitive_counterfactual_coefficient_map.py"],cwd=ROOT,check=True)
        rows=list(csv.DictReader((ROOT/"results/convergence_primitive_counterfactual_coefficient_map_v1.csv").open(encoding="utf-8")))
        gaps=read_matrix(gap_file); weights=read_vector(weight_file)
        f_raw,c_raw=build_scenario(STATES,CAPABILITIES)
        feas={s:{c:float(f_raw[i][j]) for j,c in enumerate(CAPABILITIES)} for i,s in enumerate(STATES)}
        costs={s:{c:float(c_raw[i][j]) for j,c in enumerate(CAPABILITIES)} for i,s in enumerate(STATES)}
        for r in rows:
            D0=E0=Ds=Es=0.0
            for label in filter(None,r["binding_cells"].split(";")):
                s,c=label.split(":",1); g=gaps[s][c]; a=feas[s][c]-1.0; d=costs[s][c]-1.0
                D0-=g*(a+d); E0-=g*a*d; Ds+=g*d; Es+=g*a*d
            self.assertAlmostEqual(float(r["D"]),D0,places=12); self.assertAlmostEqual(float(r["E"]),E0,places=12)
            self.assertAlmostEqual(float(r["D_slope"]),Ds,places=12); self.assertAlmostEqual(float(r["E_slope"]),Es,places=12)
            marginal=r["marginal_cell"]
            F0=0.0 if not marginal else costs[marginal.split(":",1)[0]][marginal.split(":",1)[1]]-1.0
            self.assertAlmostEqual(float(r["F"]),F0,places=12); self.assertAlmostEqual(float(r["F_slope"]),-F0,places=12)

if __name__=="__main__": unittest.main()
