"""Unified Phase II structural monotonicity theorem synthesis."""
from __future__ import annotations

import csv
from pathlib import Path

OUTPUT = Path('results/phase2_unified_structural_theorem_v1.csv')

ROWS = [
    ('domain', 'F>-1', '1+F*lambda>0 on [0,1]', 'established_domain_condition'),
    ('derivative_reduction', "Pi_prime=P/(1+F*lambda)^2", 'sign(Pi_prime)=sign(P)', 'exact_identity'),
    ('structural_identity', 'p1=2S; p2=FS', 'first-order coefficient structure', 'exact_identity'),
    ('discriminant_curvature_identity', 'Delta_P=4ST=2S*q0', 'links monotonicity and curvature numerators', 'exact_identity'),
    ('exact_interval_theorem', 'P<0 on [0,1] iff exact quadratic branch holds', 'necessary and sufficient coefficient classification', 'necessary_and_sufficient'),
    ('concave_global_route', 'F>0; S<0; T>0', 'p2<0 and Delta_P<0 imply P<0 globally', 'sufficient_not_necessary'),
    ('convex_endpoint_route', 'F>=0; S>=0; p0<0; p0+2S+FS<0', 'convex maximum occurs at endpoint', 'sufficient_not_necessary'),
    ('sharpness', 'stronger routes have certified non-necessity witnesses', 'coefficient and constructive levels distinguished', 'sharpness_certified'),
    ('realizability', 'p2=F*p1/2', 'necessary structural image constraint; selected witnesses explicitly lifted', 'structural_and_constructive'),
    ('scope', 'no full primitive inverse-image theorem claimed', 'Phase II is exact at coefficient level with certified primitive routes', 'scope_boundary'),
]


def main() -> None:
    with OUTPUT.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['analysis','theorem_component','statement','certificate','classification','inference_level'])
        w.writeheader()
        for component, statement, certificate, classification in ROWS:
            w.writerow({'analysis':'phase2_unified_structural_theorem','theorem_component':component,'statement':statement,'certificate':certificate,'classification':classification,'inference_level':'phase2_unified_structural_theorem'})
    print(OUTPUT)
    print('PHASE2_UNIFIED_STRUCTURAL_THEOREM_STATUS=PHASE2_UNIFIED_STRUCTURAL_THEOREM_COMPLETE')

if __name__ == '__main__':
    main()
