"""Explicit primitive lifts for surviving Phase II sharpness witnesses."""
from __future__ import annotations
import csv
from pathlib import Path

OUTPUT = Path('results/phase2_constructive_primitive_witnesses_v1.csv')

# One active primitive i is sufficient for both constructions.
# Map: B=w*g*a; C=B0-g; D=-g*(a+d); E=-g*a*d; F=d_m.
PRIMITIVES = [
    ('global_discriminant_and_cost_alignment', 1, -1, 1, 0, 2, 1, -1, -2, -1),
    ('T_positive_linear_route', 1, -1, 3, -1, 0, 0, -1, -2, 0),
]

def recover(g,a,w,d,B0,F):
    B=w*g*a; C=B0-g; D=-g*(a+d); E=-g*a*d
    p0=B+D-F*C; p1=2*(F*B+E); p2=F*(F*B+E)
    return B,C,D,E,p0,p1,p2

def main():
    with OUTPUT.open('w', newline='', encoding='utf-8') as f:
        fields=['analysis','witness_component','g','a','w','d','B0','F','B','C','D','E','p0','p1','p2','status','inference_level']
        wr=csv.DictWriter(f, fieldnames=fields); wr.writeheader()
        for name,g,a,w,d,B0,F,t0,t1,t2 in PRIMITIVES:
            B,C,D,E,p0,p1,p2=recover(g,a,w,d,B0,F)
            assert (p0,p1,p2)==(t0,t1,t2)
            assert g>=0 and w>=0 and -1<=a<=0 and F>-1
            wr.writerow(dict(analysis='phase2_constructive_primitive_witnesses', witness_component=name,g=g,a=a,w=w,d=d,B0=B0,F=F,B=B,C=C,D=D,E=E,p0=p0,p1=p1,p2=p2,status='constructively_realized',inference_level='explicit_primitive_lift'))
        wr.writerow(dict(analysis='phase2_constructive_primitive_witnesses',witness_component='scope',status='scope',inference_level='explicit_primitive_lift'))
    print(OUTPUT)
    print('PHASE2_CONSTRUCTIVE_PRIMITIVE_WITNESSES_STATUS=PHASE2_CONSTRUCTIVE_PRIMITIVE_WITNESSES_COMPLETE')
if __name__=='__main__': main()
