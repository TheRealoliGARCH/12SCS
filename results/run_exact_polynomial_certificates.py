"""Certify the sign of the exact quadratic numerator of Pi' on each regime."""
from __future__ import annotations
import csv, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; R=ROOT/'results'

def qval(p,x): return p[0]+p[1]*x+p[2]*x*x

def main():
    src=R/'convergence_regime_derivatives_continuity_v2.csv'
    if not src.exists(): raise FileNotFoundError(src)
    with src.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
    if not rows: raise AssertionError('no regime coefficient rows')
    out=R/'convergence_exact_polynomial_sign_certificates_v2.csv'
    with out.open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f); w.writerow(['regime','lambda_start','lambda_end','p0','p1','p2','q_start','q_end','q_min','certificate_method','certificate'])
        for r in rows:
            a,b,c,d,e,F=(float(r[k]) for k in ('A','B','C','D','E','F'))
            lo,hi=float(r['lambda_start']),float(r['lambda_end'])
            # Pi' numerator after multiplying by (1+F lambda)^2.
            p=(b+d-F*c, 2*b*F+2*e, F*(b*F+e))
            den0,den1=1+F*lo,1+F*hi
            if min(den0,den1)<=0: raise AssertionError(f'nonpositive derivative denominator in regime {r["regime"]}')
            candidates=[lo,hi]
            if abs(p[2])>1e-18:
                v=-p[1]/(2*p[2])
                if lo<=v<=hi: candidates.append(v)
            vals=[qval(p,x) for x in candidates]
            qmin=min(vals)
            # A quadratic is negative on the closed interval iff its minimum is negative.
            if qmin>=-1e-12: raise AssertionError(f'quadratic sign certificate failed in regime {r["regime"]}: min={qmin}')
            method='endpoint+vertex' if len(candidates)==3 else 'endpoints'
            w.writerow([r['regime'],lo,hi,*p,den0,den1,qmin,method,'NEGATIVE'])
    print(f'Exact quadratic sign certificates established for {len(rows)} regimes.')
if __name__=='__main__': main()
