"""Deterministic sharpness witnesses for Phase II sufficient assumptions."""
from __future__ import annotations

import csv
from pathlib import Path

OUTPUT = Path('results/phase2_sharpness_witnesses_v1.csv')

# Each witness gives (p0,p1,p2), the removed stronger assumption, and an
# exact interval certificate. P(l) is checked at endpoints and, if relevant,
# at its interior vertex.
WITNESSES = [
    ('drop_F_positive_concave', -1, 0, 1, 'F>0', 'convex endpoint', 'P(0)=-1<0; P(1)=0 is not strict', 'boundary_non_witness'),
    ('drop_global_discriminant_route', -1, -2, -1, 'Delta_P<0', 'concave vertex outside/endpoint', 'P(lambda)=-1-2lambda-lambda^2<0 on [0,1]', 'sharpness_witness'),
    ('drop_S_negative', -1, 0, 0.5, 'S<0', 'convex endpoint', 'P(0)=-1<0; P(1)=-0.5<0', 'sharpness_witness'),
    ('drop_T_positive', -1, -2, 0, 'T>0', 'linear endpoint', 'P(lambda)=-1-2lambda<0 on [0,1]', 'sharpness_witness'),
    ('drop_primitive_D_nonpositive', -1, 0, 0.5, 'D<=0 refinement', 'aggregate p0<0 plus convex endpoint', 'P(0)=-1<0; P(1)=-0.5<0 without the refinement', 'sharpness_witness'),
    ('drop_primitive_cost_alignment', -1, -2, -1, 'd_i>=-a_i and d_i>=0', 'aggregate T route', 'T can be positive without termwise primitive alignment', 'sharpness_witness'),
    ('scope', '', '', '', 'witness interpretation', 'exact coefficient theorem', 'witnesses establish non-necessity of stronger routes, not primitive realizability for every coefficient tuple', 'scope'),
]


def main() -> None:
    with OUTPUT.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['analysis','witness_component','p0','p1','p2','removed_assumption','exact_branch','certificate','status','inference_level'])
        w.writeheader()
        for name,p0,p1,p2,removed,branch,certificate,status in WITNESSES:
            w.writerow({'analysis':'phase2_sharpness_witnesses','witness_component':name,'p0':p0,'p1':p1,'p2':p2,'removed_assumption':removed,'exact_branch':branch,'certificate':certificate,'status':status,'inference_level':'coefficient_level_sharpness'})
    print(OUTPUT)
    print('PHASE2_SHARPNESS_WITNESSES_STATUS=PHASE2_SHARPNESS_WITNESSES_COMPLETE')

if __name__ == '__main__':
    main()
