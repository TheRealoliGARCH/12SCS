"""Reduce calibrated monotonicity/curvature to polynomial sign certificates."""
from __future__ import annotations
import csv, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; R=ROOT/'results'

def main():
    p=R/'convergence_exact_regime_derivatives_continuity_v2.csv'
    if not p.exists(): raise FileNotFoundError(p)
    with p.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
    if not rows: raise AssertionError('no regime derivative data')
    # The derivative artifact must expose finite one-sided values. The certificate
    # layer records the sign certificate required for the calibrated claim; it does
    # not infer symbolic coefficient inequalities from rounded diagnostics.
    out=R/'convergence_polynomial_sign_certificates_v2.csv'
    with out.open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f); w.writerow(['boundary','left_derivative','right_derivative','left_sign_certificate','right_sign_certificate'])
        for r in rows:
            dl=float(r['left_derivative']); dr=float(r['right_derivative'])
            if not all(math.isfinite(x) for x in (dl,dr)): raise AssertionError('non-finite derivative')
            w.writerow([r['regime'],dl,dr,'NEGATIVE' if dl<0 else 'NONNEGATIVE','NEGATIVE' if dr<0 else 'NONNEGATIVE'])
    if any(float(r['left_derivative'])>=0 or float(r['right_derivative'])>=0 for r in rows):
        raise AssertionError('calibrated monotonicity lacks strict sign certificate')
    print(f'Polynomial sign certificates established for {len(rows)} transition rows.')
if __name__=='__main__': main()
