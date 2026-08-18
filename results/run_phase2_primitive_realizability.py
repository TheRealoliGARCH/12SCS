"""Primitive realizability filter for Phase II coefficient sharpness witnesses."""
from __future__ import annotations

import csv
from pathlib import Path

OUTPUT = Path('results/phase2_primitive_realizability_v1.csv')

# For p1 != 0, realizability requires F = 2*p2/p1 and hence F > -1.
# For p1 = 0, the identity p2 = F*p1/2 forces p2 = 0.
ROWS = [
    ('identity_filter', '', '', '', '', 'p2=F*p1/2', 'exact_structural_identity'),
    ('drop_global_discriminant_route', -1, -2, -1, 1, 'F=2*p2/p1=1>-1', 'passes_structural_filter'),
    ('drop_S_negative', -1, 0, 0.5, '', 'p1=0 implies p2 must equal 0', 'fails_structural_filter'),
    ('drop_T_positive', -1, -2, 0, 0, 'F=2*p2/p1=0>-1', 'passes_structural_filter'),
    ('drop_primitive_D_nonpositive', -1, 0, 0.5, '', 'p1=0 implies p2 must equal 0', 'fails_structural_filter'),
    ('drop_primitive_cost_alignment', -1, -2, -1, 1, 'F=2*p2/p1=1>-1', 'passes_structural_filter'),
    ('scope', '', '', '', '', 'structural filter is necessary, not a full primitive construction', 'scope'),
]


def main() -> None:
    with OUTPUT.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['analysis','witness_component','p0','p1','p2','implied_F','certificate','status','inference_level'])
        w.writeheader()
        for name,p0,p1,p2,F,certificate,status in ROWS:
            w.writerow({'analysis':'phase2_primitive_realizability','witness_component':name,'p0':p0,'p1':p1,'p2':p2,'implied_F':F,'certificate':certificate,'status':status,'inference_level':'structural_realizability_filter'})
    print(OUTPUT)
    print('PHASE2_PRIMITIVE_REALIZABILITY_STATUS=PHASE2_PRIMITIVE_REALIZABILITY_COMPLETE')

if __name__ == '__main__':
    main()
