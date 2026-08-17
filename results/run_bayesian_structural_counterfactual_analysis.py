"""Prior-induced uncertainty over the structural d -> (1-delta)d counterfactual.

No likelihood or observational data are used here. Consequently the output is
not a posterior causal effect: it is the push-forward of the specified Beta
prior for delta through the deterministic structural counterfactual map.
"""
from __future__ import annotations
import csv
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
    required={"A","B","C","D","E","F","lambda_start","lambda_end","d","D_cf_unit","E_cf_unit"}
    if not rows or not required.issubset(rows[0]): raise ValueError("counterfactual input lacks canonical objective columns")
    return rows

def affine_contrast(rows):
    terms=[]
    for r in rows:
        if float(r["d"]) < 0.0: continue
        lam=(float(r["lambda_start"])+float(r["lambda_end"])) / 2.0
        vals=[float(r[x]) for x in "ABCDEF"]
        base=objective(*vals,lam)
        D1=float(r["D_cf_unit"]); E1=float(r["E_cf_unit"])
        cf1=objective(vals[0],vals[1],vals[2],D1,E1,vals[5],lam)
        w=float(r.get("weight",1.0))
        terms.append((w,0.0,cf1-base))
    if not terms: raise ValueError("empty admissible population")
    total=sum(w for w,_,_ in terms)
    alpha=sum(w*a for w,a,_ in terms)/total
    beta=sum(w*b for w,_,b in terms)/total
    return alpha,beta

def main():
    inp=Path("results/bayesian_structural_counterfactual_cells_v1.csv")
    out=Path("results/bayesian_structural_counterfactual_analysis_v1.csv")
    alpha,beta=affine_contrast(load(inp))
    with out.open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f)
        w.writerow(["prior_a","prior_b","mean_delta","var_delta","contrast_intercept","contrast_slope","mean_contrast","var_contrast","contrast_at_delta_0","contrast_at_delta_1"])
        for a,b in PRIORS:
            m,v=beta_moments(a,b)
            w.writerow([a,b,m,v,alpha,beta,alpha+beta*m,beta*beta*v,alpha,alpha+beta])
    print(out)
    print(f"CONTRAST(delta)={alpha:.17g}+({beta:.17g})*delta")

if __name__ == "__main__": main()
