"""Certify interval-wide signs of the exact quadratic curvature numerator."""
from __future__ import annotations
import csv, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; R=ROOT/'results'

def sign_certificate(a,b,c,left,right):
    pts=[left,right]
    if abs(a)>1e-15:
        v=-b/(2*a)
        if left < v < right: pts.append(v)
    vals=[a*x*x+b*x+c for x in pts]
    return min(vals),max(vals),pts

def main():
    p=R/'convergence_regime_derivatives_continuity_v2.csv'
    if not p.exists(): raise FileNotFoundError(p)
    with p.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
    if not rows: raise AssertionError('no derivative regimes')
    out=R/'convergence_curvature_polynomial_certificates_v2.csv'
    with out.open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f); w.writerow(['regime','lambda_start','lambda_end','q0','q1','q2','q_min','q_max','curvature_certificate'])
        for r in rows:
            left=float(r['lambda_start']); right=float(r['lambda_end'])
            A,B,C,D,E,F=[float(r[k]) for k in ('A','B','C','D','E','F')]
            # Q(lambda) is the numerator after multiplying Pi'' by (1+F lambda)^3.
            q0=2*(E-D*F+C*F*F)
            q1=2*F*(D*F-2*E)
            q2=2*F*F*E
            qmin,qmax,_=sign_certificate(q2,q1,q0,left,right)
            if not all(math.isfinite(x) for x in (q0,q1,q2,qmin,qmax)): raise AssertionError('non-finite curvature certificate')
            if qmin>1e-10: cert='STRICTLY_CONVEX'
            elif qmax<-1e-10: cert='STRICTLY_CONCAVE'
            elif qmin<=0<=qmax: cert='CURVATURE-CHANGE-OR-ZERO'
            else: cert='ZERO/UNRESOLVED'
            w.writerow([r['regime'],left,right,q0,q1,q2,qmin,qmax,cert])
    print(f'Curvature polynomial certificates generated for {len(rows)} regimes.')
if __name__=='__main__': main()
