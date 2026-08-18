"""Exact necessary-and-sufficient classification of P(lambda)<0 on [0,1]."""
from __future__ import annotations

import csv
from pathlib import Path

OUTPUT = Path('results/phase2_exact_interval_negativity_v1.csv')

ROWS = [
    ('convex_or_linear', 'p2>=0; P(0)<0; P(1)<0', 'P(lambda)<0 for every lambda in [0,1]', 'necessary_and_sufficient_branch'),
    ('concave_vertex_left', 'p2<0; vertex<=0; P(0)<0; P(1)<0', 'P(lambda)<0 for every lambda in [0,1]', 'necessary_and_sufficient_branch'),
    ('concave_vertex_right', 'p2<0; vertex>=1; P(0)<0; P(1)<0', 'P(lambda)<0 for every lambda in [0,1]', 'necessary_and_sufficient_branch'),
    ('concave_vertex_interior', 'p2<0; 0<p1<-2*p2; Delta_P<0', 'P(lambda)<0 for every lambda in [0,1]', 'necessary_and_sufficient_branch'),
    ('vertex_location', 'p2<0 and vertex=-p1/(2*p2)', '0<vertex<1 iff 0<p1<-2*p2', 'exact_identity'),
    ('vertex_value', 'p2!=0 and vertex=-p1/(2*p2)', 'P(vertex)=-Delta_P/(4*p2)', 'exact_identity'),
    ('structural_substitution', 'p1=2S; p2=FS; Delta_P=4ST', 'all branches translate exactly into (p0,S,T,F)', 'exact_translation'),
    ('scope', 'strict negativity is classified exactly at coefficient level', 'primitive conditions are sufficient translations unless separately proved equivalent', 'scope'),
]


def main() -> None:
    with OUTPUT.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['analysis','theorem_component','conditions','conclusion','classification','inference_level'])
        w.writeheader()
        for component, conditions, conclusion, classification in ROWS:
            w.writerow({'analysis':'phase2_exact_interval_negativity','theorem_component':component,'conditions':conditions,'conclusion':conclusion,'classification':classification,'inference_level':'exact_interval_negativity'})
    print(OUTPUT)
    print('PHASE2_EXACT_INTERVAL_NEGATIVITY_STATUS=PHASE2_EXACT_INTERVAL_NEGATIVITY_COMPLETE')

if __name__ == '__main__':
    main()
