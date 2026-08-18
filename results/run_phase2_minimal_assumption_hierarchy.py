"""Minimal-assumption hierarchy for Phase II monotonicity regimes."""
from __future__ import annotations

import csv
from pathlib import Path

OUTPUT = Path('results/phase2_minimal_assumption_hierarchy_v1.csv')

ROWS = [
    ('basic_domain', 'g_i>=0; w_i>=0; a_i in [-1,0]; d_m>-1', 'B<=0 and F>-1', 'endogenous'),
    ('p0_aggregate', 'p0=B+D-F*C<0', 'P(0)<0', 'minimal_aggregate_sufficient'),
    ('S_nonnegative_aggregate', 'S=F*B+E>=0', 'p2=F*S>=0 when F>=0', 'minimal_aggregate_sufficient'),
    ('S_negative_aggregate', 'F>0 and S=F*B+E<0', 'p2<0', 'minimal_aggregate_sufficient'),
    ('T_positive_aggregate', 'T=E-F*D+F^2*C>0', 'q0=2*T>0', 'minimal_aggregate_sufficient'),
    ('concave_minimal_branch', 'F>0; S<0; T>0', 'p2<0 and Delta_P=4*S*T<0, hence P(lambda)<0 for all real lambda', 'minimal_branch'),
    ('convex_minimal_branch', 'F>=0; S>=0; p0<0; p0+2*S+F*S<0', 'p2>=0 and P(0)<0 and P(1)<0, hence P(lambda)<0 on [0,1]', 'minimal_branch'),
    ('primitive_p0_refinement', 'D<=0; F>=0; C>=0; and (B<0 or D<0 or (F>0 and C>0))', 'p0<0', 'stronger_transparent_sufficient'),
    ('primitive_S_negative_refinement', 'F>0 and E<-F*B', 'S<0', 'stronger_transparent_sufficient'),
    ('primitive_T_nonnegative_refinement', 'F>=0; C>=0; d_i>=-a_i and d_i>=0 for all i', 'T>=0', 'stronger_transparent_sufficient'),
    ('scope', 'aggregate inequalities are weakest at the coefficient-combination level; primitive refinements are stronger but interpretable', 'no primitive refinement is claimed necessary', 'scope'),
]


def main() -> None:
    with OUTPUT.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['analysis','theorem_component','assumptions','conclusion','classification','inference_level'])
        w.writeheader()
        for component, assumptions, conclusion, classification in ROWS:
            w.writerow({'analysis':'phase2_minimal_assumption_hierarchy','theorem_component':component,'assumptions':assumptions,'conclusion':conclusion,'classification':classification,'inference_level':'minimal_assumption_hierarchy'})
    print(OUTPUT)
    print('PHASE2_MINIMAL_ASSUMPTION_HIERARCHY_STATUS=PHASE2_MINIMAL_ASSUMPTION_HIERARCHY_COMPLETE')

if __name__ == '__main__':
    main()
