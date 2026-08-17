"""Bayesian uncertainty over the structural d -> 0.9d counterfactual."""
from __future__ import annotations
import csv, math
from pathlib import Path

PRIORS = ((5.0,45.0),(10.0,90.0),(20.0,180.0))

def beta_moments(a: float,b: float):
    mean=a/(a+b)
    var=a*b/((a+b)**2*(a+b+1.0))
    return mean,var

def objective(A,B,C,D,E,F,lam):
    den=1.0+F*lam
    if den <= 0.0: raise ValueError("invalid objective denominator")
    return A+B*lam+(C+D*lam+E*lam*lam)/den

def load(path: Path):
    rows=list(csv.DictReader(path.open(encoding="utf-8")))
    required={"A","B","C","D","E","F","lambda_start","lambda_end","d"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("counterfactual input lacks canonical objective columns")
    return rows

def evaluate(rows, mean_delta):
    deltas=[]
    for r in rows:
        d=float(r["d"])
        if d < 0.0: continue
        lam=(float(r["lambda_start"])+float(r["lambda_end"])) / 2.0
        vals=[float(r[x]) for x in "ABCDEF"]
        base=objective(*vals,lam)
        # d is a primitive input; the canonical map must supply the affected
        # objective coefficients in a counterfactual artifact. We therefore
        # require explicit counterfactual columns rather than guessing how D/E
        # decompose by cell.
        if "D_cf_unit" not in r or "E_cf_unit" not in r:
            raise ValueError("missing canonical counterfactual coefficient map")
        D_cf=float(r["D_cf_unit"]); E_cf=float(r["E_cf_unit"])
        cfvals=vals[:3]+[D_cf,E_cf,vals[5]]
        cf=objective(*cfvals,lam)
        deltas.append((cf-base, float(r.get("weight",1.0))))
    if not deltas: raise ValueError("empty admissible population")
    total=sum(w for _,w in deltas)
    return sum(x*w for x,w in deltas)/total

def main():
    inp=Path("results/bayesian_structural_counterfactual_cells_v1.csv")
    out=Path("results/bayesian_structural_counterfactual_analysis_v1.csv")
    rows=load(inp)
    structural=evaluate(rows,0.10)
    with out.open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["prior_a","prior_b","mean_delta","structural_contrast"])
        for a,b in PRIORS:
            m,v=beta_moments(a,b); w.writerow([a,b,m,structural])
    print(out)
    print(f"STRUCTURAL_CONTRAST={structural:.17g}")

if __name__ == "__main__": main()
