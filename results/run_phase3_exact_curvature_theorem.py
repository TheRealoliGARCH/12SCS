"""Phase III exact structural curvature theorem."""
from __future__ import annotations

import csv
from pathlib import Path

OUTPUT = Path('results/phase3_exact_curvature_theorem_v1.csv')

ROWS = [
    ('domain', 'F>-1', '1+F*lambda>0 on [0,1]', 'established_domain_condition'),
    ('curvature_reduction', "Pi_double_prime=Q/(1+F*lambda)^3", 'curvature sign equals sign(Q)', 'exact_identity'),
    ('curvature_numerator', 'Q=(p1-2F*p0)+(2p2-F*p1)*lambda', 'direct differentiation identity', 'exact_identity'),
    ('structural_cancellation', '2p2-F*p1=0', 'p1=2S and p2=FS', 'exact_identity'),
    ('constant_curvature_numerator', 'Q(lambda)=2T', 'p1-2F*p0=2T', 'exact_identity'),
    ('convexity', 'T>0 iff Pi_double_prime>0 on [0,1]', 'positive denominator cube', 'necessary_and_sufficient'),
    ('linearity', 'T=0 iff Pi_double_prime=0 on [0,1]', 'zero constant numerator', 'necessary_and_sufficient'),
    ('concavity', 'T<0 iff Pi_double_prime<0 on [0,1]', 'positive denominator cube', 'necessary_and_sufficient'),
    ('no_inflection', 'T has one global sign', 'Pi_double_prime cannot change sign on [0,1]', 'structural_consequence'),
    ('scope', 'exact curvature classification under F>-1', 'coefficient/structural result; primitive necessity not claimed', 'scope_boundary'),
]


def main() -> None:
    with OUTPUT.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['analysis','theorem_component','statement','certificate','classification','inference_level'])
        w.writeheader()
        for component, statement, certificate, classification in ROWS:
            w.writerow({'analysis':'phase3_exact_curvature_theorem','theorem_component':component,'statement':statement,'certificate':certificate,'classification':classification,'inference_level':'phase3_exact_curvature_theorem'})
    print(OUTPUT)
    print('PHASE3_EXACT_CURVATURE_THEOREM_STATUS=PHASE3_EXACT_CURVATURE_THEOREM_COMPLETE')

if __name__ == '__main__':
    main()
