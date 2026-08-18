"""Primitive sufficient sign theorems for Phase II."""
from __future__ import annotations

import csv
from pathlib import Path

OUTPUT = Path('results/phase2_endogenous_sign_theorem_synthesis_v1.csv')

ROWS = [
    ('basic_B_sign', 'g_i>=0, w_i>=0, a_i in [-1,0]', 'B=sum_i w_i*g_i*a_i<=0', 'endogenous'),
    ('p0_negative', 'B<0 or D<0 or (F>0 and C>0); additionally D<=0, F>=0, C>=0', 'p0=B+D-F*C<0', 'sufficient'),
    ('S_nonnegative', 'F>=0 and E>=-F*B', 'S=F*B+E>=0', 'sufficient'),
    ('T_nonnegative', 'F>=0, C>=0, d_i>=-a_i and d_i>=0 for all i', 'E>=0, D<=0, hence T=E-F*D+F^2*C>=0', 'sufficient'),
    ('S_negative', 'F>0 and E<-F*B', 'S=F*B+E<0', 'sufficient'),
    ('T_positive', 'E-F*D+F^2*C>0', 'T>0', 'primitive_substituted_sufficient'),
    ('concave_global_negative', 'F>0, E<-F*B, and E-F*D+F^2*C>0', 'p2=F*S<0 and Delta_P=4*S*T<0', 'sufficient'),
    ('convex_endpoint_negative', 'F>=0, E>=-F*B, p0<0, and p0+2*S+F*S<0', 'p2>=0 and P(0)<0 and P(1)<0', 'sufficient'),
    ('theorem_scope', 'primitive conditions stated explicitly', 'all sign claims beyond basic-domain consequences are sufficient conditions, not automatic domain implications', 'scope'),
]


def main() -> None:
    with OUTPUT.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['analysis','theorem_component','primitive_conditions','conclusion','status','inference_level'])
        w.writeheader()
        for component, conditions, conclusion, status in ROWS:
            w.writerow({'analysis':'phase2_endogenous_sign_theorem_synthesis','theorem_component':component,'primitive_conditions':conditions,'conclusion':conclusion,'status':status,'inference_level':'primitive_sufficient_sign_theorem'})
    print(OUTPUT)
    print('PHASE2_ENDOGENOUS_SIGN_THEOREM_SYNTHESIS_STATUS=PHASE2_ENDOGENOUS_SIGN_THEOREM_SYNTHESIS_COMPLETE')

if __name__ == '__main__':
    main()
