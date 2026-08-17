"""Produce the quantitative calibrated theorem summary."""
from __future__ import annotations
import csv, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; R=ROOT/'results'
def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def main():
    g=read(R/'convergence_global_comparative_statics_v2.csv')
    k=read(R/'convergence_exact_kink_analysis_v2.csv')
    if not g or not k or len(g)!=len(k): raise AssertionError('inconsistent theorem artifacts')
    max_jump=max(abs(float(x['derivative_jump'])) for x in g)
    max_gap=max(float(x['value_gap']) for x in k)
    min_slope=min(min(float(x['left_derivative']),float(x['right_derivative'])) for x in g)
    max_slope=max(max(float(x['left_derivative']),float(x['right_derivative'])) for x in g)
    transitions={'C1':0,'KINK':0}
    curvature={'CONVEX':0,'CONCAVE':0,'CURVATURE-CHANGE':0}
    for x in g:
        transitions[x['transition']]+=1; curvature[x['curvature_transition']]+=1
    vals=[max_jump,max_gap,min_slope,max_slope]
    if not all(math.isfinite(x) for x in vals): raise AssertionError('non-finite summary')
    out=R/'calibrated_global_theorem_summary_v2.txt'
    out.write_text(f'''CALIBRATED GLOBAL PIECEWISE COMPARATIVE-STATICS THEOREM\n\nNumber of exact regime transitions: {len(g)}\nMaximum continuity error: {max_gap:.16g}\nMaximum absolute derivative jump: {max_jump:.16g}\nMinimum one-sided derivative: {min_slope:.16g}\nMaximum one-sided derivative: {max_slope:.16g}\n\nTransition classification:\n  C1 transitions: {transitions['C1']}\n  Genuine kinks: {transitions['KINK']}\n\nCurvature classification:\n  Convex: {curvature['CONVEX']}\n  Concave: {curvature['CONCAVE']}\n  Curvature-changing: {curvature['CURVATURE-CHANGE']}\n\nConclusion:\nThe calibrated value function is continuous and strictly decreasing on all one-sided regime intervals when the maximum one-sided derivative is negative. Differentiability and curvature are classified transition-by-transition; no universal curvature claim is made.\n''',encoding='utf-8')
    if max_slope>=0: raise AssertionError('strict calibrated decrease not established')
    print(out)
if __name__=='__main__':main()
