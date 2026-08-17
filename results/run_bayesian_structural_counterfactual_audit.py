"""Audit the exact prior-induced structural counterfactual distribution."""
from __future__ import annotations
import csv, math
from pathlib import Path

PRIORS=((5.0,45.0),(10.0,90.0),(20.0,180.0))
INPUT=Path("results/bayesian_structural_counterfactual_cells_v1.csv")
OUTPUT=Path("results/bayesian_structural_counterfactual_audit_v1.csv")

def beta_moments(a,b):
    m=a/(a+b)
    v=a*b/((a+b)**2*(a+b+1.0))
    return m,v

def objective(A,B,C,D,E,F,lam):
    den=1.0+F*lam
    if den<=0: raise ValueError("invalid objective denominator")
    return A+B*lam+(C+D*lam+E*lam*lam)/den

def main():
    rows=list(csv.DictReader(INPUT.open(encoding="utf-8")))
    required={"A","B","C","D","E","F","D_cf_unit","E_cf_unit","lambda_start","lambda_end","d"}
    assert rows and required.issubset(rows[0])
    terms=[]
    for r in rows:
        if float(r["d"])<0: continue
        lam=(float(r["lambda_start"])+float(r["lambda_end"])) / 2
        vals=[float(r[x]) for x in "ABCDEF"]
        base=objective(*vals,lam)
        cf0=objective(vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],lam)
        cf1=objective(vals[0],vals[1],vals[2],float(r["D_cf_unit"]),float(r["E_cf_unit"]),vals[5],lam)
        w=float(r.get("weight",1.0)); terms.append((w,cf0-base,cf1-cf0))
    assert terms
    total=sum(w for w,_,_ in terms)
    alpha=sum(w*a for w,a,_ in terms)/total
    beta=sum(w*b for w,_,b in terms)/total
    rows_out=[]
    for a,b in PRIORS:
        m,v=beta_moments(a,b)
        assert abs(m-0.1)<1e-15
        mean=alpha+beta*m
        var=beta*beta*v
        rows_out.append((a,b,m,v,alpha,beta,mean,var))
    assert abs(rows_out[0][6]-rows_out[1][6])<1e-15
    assert rows_out[0][7]>rows_out[1][7]>rows_out[2][7]
    assert all(math.isfinite(x) for row in rows_out for x in row)
    with OUTPUT.open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["prior_a","prior_b","mean_delta","var_delta","alpha","beta","mean_contrast","var_contrast"])
        w.writerows(rows_out)
    print(f"alpha={alpha:.17g} beta={beta:.17g}")
    print(OUTPUT)

if __name__=="__main__": main()
