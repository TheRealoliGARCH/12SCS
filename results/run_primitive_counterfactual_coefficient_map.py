"""Derive the exact primitive coefficient map under d -> (1-delta)d."""
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from model.convergence_analysis import CAPABILITIES, STATES
from model.heterogeneous_scenario import build_scenario
RESULTS=ROOT/"results"

def matrix(path):
    with path.open(encoding="utf-8",newline="") as f: rows=list(csv.reader(f))
    if rows[0][1:] != list(CAPABILITIES): raise ValueError(f"capability header mismatch: {path}")
    return {r[0]:{c:float(r[j+1]) for j,c in enumerate(CAPABILITIES)} for r in rows[1:]}

def vector(path):
    with path.open(encoding="utf-8",newline="") as f: rows=list(csv.reader(f))
    return {r[0]:float(r[1]) for r in rows[1:]}

def lookup(m): return {s:{c:float(m[i][j]) for j,c in enumerate(CAPABILITIES)} for i,s in enumerate(STATES)}
def cell(label): return label.split(":",1)

def derive(binding,marginal,gaps,weights,feas,costs):
    A=B=0.0; C=1.0; D=E=0.0; D_slope=E_slope=0.0
    for label in binding:
        s,c=cell(label); g=gaps[s][c]; w=weights[c]
        a=feas[s][c]-1.0; d=costs[s][c]-1.0
        A += w*g; B += w*g*a; C -= g
        D -= g*(a+d); E -= g*a*d
        D_slope += g*d; E_slope += g*a*d
    F=costs[cell(marginal)[0]][cell(marginal)[1]]-1.0 if marginal else 0.0
    F_slope=-F
    return dict(A=A,B=B,C=C,D=D,E=E,F=F,D_slope=D_slope,E_slope=E_slope,F_slope=F_slope)

def main():
    gaps=matrix(RESULTS/"capability_gap_positive_v2.csv"); weights=vector(RESULTS/"capability_dispersion_weights_v2.csv")
    f_raw,c_raw=build_scenario(STATES,CAPABILITIES); feas=lookup(f_raw); costs=lookup(c_raw)
    with (RESULTS/"convergence_active_set_regime_formulas_v2.csv").open(encoding="utf-8",newline="") as f: regimes=list(csv.DictReader(f))
    fields=["regime","lambda_start","lambda_end","binding_cells","marginal_cell","A","B","C","D","E","F","D_slope","E_slope","F_slope"]
    out=RESULTS/"convergence_primitive_counterfactual_coefficient_map_v1.csv"
    with out.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for r in regimes:
            binding=[x for x in r["binding_feasibility_cells"].split(";") if x]; marginal=r["marginal_cell"] or ""
            d=derive(binding,marginal,gaps,weights,feas,costs)
            row={k:r[k] for k in ("regime","lambda_start","lambda_end")}; row.update(binding_cells=";".join(binding),marginal_cell=marginal); row.update(d); w.writerow(row)
    print(out)
if __name__=="__main__": main()
