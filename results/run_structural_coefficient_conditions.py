"""Derive calibration-independent sufficient coefficient conditions.

The conditions are expressed only in the rational-regime coefficients. They are
therefore structural sufficient conditions, not statements about any particular
calibration. Strong global conditions are imposed on lambda in [0,1].
"""
from __future__ import annotations
from pathlib import Path
R=Path(__file__).resolve().parents[1]/'results'

def main():
    out=R/'structural_coefficient_conditions_v1.txt'
    text='''12SCS PHASE II -- STRUCTURAL COEFFICIENT CONDITIONS

For a regime
  Pi(lambda)=A+B lambda+(C+D lambda+E lambda^2)/(1+F lambda),
assume 1+F lambda>0 on [0,1]. This is equivalent to F>-1.

FIRST DERIVATIVE

Pi'(lambda)=P(lambda)/(1+F lambda)^2,
P(lambda)=p0+p1 lambda+p2 lambda^2,

p0 = B+D-F C,
p1 = 2(B F+E),
p2 = F(B F+E).

There is an important structural identity. Put S=BF+E and
T=E-FD+F^2 C. Then
  p1=2S,
  p2=F S,
  p0=B+D-FC,
  Delta_P=p1^2-4 p2 p0=4 S T.
Moreover q0=2T for the curvature numerator below. Hence
  Delta_P=2(BF+E) q0.
This links first-order discriminant structure directly to the second-order
constant coefficient.

The following are calibration-independent sufficient conditions for strict
monotonic decrease on the full parameter domain [0,1].

Case M1 (convex numerator):
  p2 >= 0,
  p0 < 0,
  p0+p1+p2 < 0.
Then P(lambda)<0 for every lambda in [0,1], because a convex quadratic
attains its maximum on a compact interval at an endpoint.

Case M2 (globally negative concave numerator):
  p2 < 0,
  Delta_P < 0.
Then P(lambda)<0 for every real lambda, hence on [0,1].

Case M3 (linear numerator):
  p2=0,
  p0<0,
  p0+p1<0.
This is the linear limiting case and is exact on [0,1].

A sharper interval certificate can replace M1--M3 by evaluating P at 0, 1,
and its vertex when the vertex lies in (0,1). Thus Phase II separates a
simple structural sufficient theorem from the exact interval certificate
already established in Phase I.

SECOND DERIVATIVE

Pi''(lambda)=Q(lambda)/(1+F lambda)^3,
Q(lambda)=q0+q1 lambda+q2 lambda^2,

q0 = 2(E-D F+C F^2),
q1 = 2F(D F-2E),
q2 = 2F^2 E.

For strict convexity on [0,1], sufficient structural conditions are:

Case C+1:
  q2 >= 0,
  q0 > 0,
  q0+q1+q2 > 0.

Case C+2 (global positivity):
  q2 > 0,
  Delta_Q = q1^2-4 q2 q0 < 0.

For strict concavity on [0,1], sufficient structural conditions are:

Case C-1:
  q2 <= 0,
  q0 < 0,
  q0+q1+q2 < 0.

Case C-2 (global negativity):
  q2 < 0,
  Delta_Q = q1^2-4 q2 q0 < 0.

When q2=0, endpoint inequalities are exact for the linear numerator.

STRUCTURAL THEOREM

If F>-1 and any one of M1--M3 holds, then Pi'(lambda)<0 for all
lambda in [0,1]. If, additionally, one of C+1/C+2 holds, Pi is strictly
convex; if one of C-1/C-2 holds, Pi is strictly concave.

These are coefficient-level sufficient conditions. They do not assert that
the calibrated 12SCS model satisfies them in every regime. The next Phase II
step is to substitute the model's symbolic coefficient map and determine
which of these inequalities are implied by the primitives.
'''
    out.write_text(text,encoding='utf-8'); print(out)
if __name__=='__main__': main()
