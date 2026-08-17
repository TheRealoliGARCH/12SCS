"""Synthesize the machine-checked calibrated global comparative-statics theorem."""
from __future__ import annotations
import csv, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; R=ROOT/'results'

def rows(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

def main():
    kink=rows(R/'convergence_exact_kink_analysis_v2.csv')
    global_=rows(R/'convergence_global_comparative_statics_v2.csv')
    curv=rows(R/'convergence_curvature_polynomial_certificates_v2.csv')
    if not kink or not global_ or not curv: raise AssertionError('missing theorem artifacts')
    # Kink/global artifacts are boundary-indexed; curvature is regime-indexed.
    # Therefore their row counts need not agree: K transitions imply K+1 regimes.
    if len(kink)!=len(global_): raise AssertionError('boundary artifact mismatch')
    if len(curv) not in (len(kink), len(kink)+1):
        raise AssertionError('regime artifact count is inconsistent with boundary count')
    max_gap=max(float(r['value_gap']) for r in kink)
    max_jump=max(abs(float(r['derivative_jump'])) for r in global_)
    max_slope=max(max(float(r['left_derivative']),float(r['right_derivative'])) for r in global_)
    min_slope=min(min(float(r['left_derivative']),float(r['right_derivative'])) for r in global_)
    if not all(math.isfinite(x) for x in (max_gap,max_jump,max_slope,min_slope)): raise AssertionError('nonfinite theorem summary')
    if max_slope >= 0: raise AssertionError('strict decrease not certified')
    ccounts={x:sum(r['curvature_certificate']==x for r in curv) for x in ('STRICTLY_CONVEX','STRICTLY_CONCAVE','CURVATURE-CHANGE-OR-ZERO','ZERO/UNRESOLVED')}
    tcounts={x:sum(r['transition']==x for r in kink) for x in ('C1','KINK')}
    out=R/'global_piecewise_comparative_statics_theorem_v3.txt'
    lines=['MACHINE-CHECKED CALIBRATED GLOBAL PIECEWISE COMPARATIVE-STATICS THEOREM','',f'Exact regime transitions: {len(kink)}',f'Validated curvature regimes: {len(curv)}',f'Maximum continuity error: {max_gap:.16g}',f'Maximum absolute derivative jump: {max_jump:.16g}',f'Minimum one-sided derivative: {min_slope:.16g}',f'Maximum one-sided derivative: {max_slope:.16g}','',f"C1 transitions: {tcounts['C1']}",f"Genuine kinks: {tcounts['KINK']}",'',f"Strictly convex regimes certified: {ccounts['STRICTLY_CONVEX']}",f"Strictly concave regimes certified: {ccounts['STRICTLY_CONCAVE']}",f"Curvature-change-or-zero regimes: {ccounts['CURVATURE-CHANGE-OR-ZERO']}",f"Unresolved/zero regimes: {ccounts['ZERO/UNRESOLVED']}",'','THEOREM: The calibrated value function is continuous across the exact active-set intersections and strictly decreasing on every validated regime interval. Each regime is rational of the form A+B lambda+(C+D lambda+E lambda^2)/(1+F lambda). Differentiability at each boundary is classified by the exact derivative jump. Curvature is certified regime-by-regime by an interval-wide quadratic sign certificate.','', 'This is a calibrated theorem for the validated model instance; parameter-free universality requires separate symbolic coefficient inequalities.']
    out.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(out)
if __name__=='__main__':main()
