"""Phase III exact primitive pullback of the curvature invariant T."""
from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / 'results'
MAP_SCRIPT = RESULTS / 'run_primitive_counterfactual_coefficient_map.py'
MAP = RESULTS / 'convergence_primitive_counterfactual_coefficient_map_v1.csv'
OUTPUT = RESULTS / 'phase3_primitive_curvature_pullback_v1.csv'


def main() -> None:
    subprocess.run([sys.executable, str(MAP_SCRIPT)], cwd=ROOT, check=True)
    with MAP.open(encoding='utf-8', newline='') as f:
        source = list(csv.DictReader(f))
    fields = ['analysis','regime','lambda_start','lambda_end','C','D','E','F','T','curvature_class','certificate','inference_level']
    with OUTPUT.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in source:
            C, D, E, F = (float(r[k]) for k in ('C','D','E','F'))
            T = E - F * D + F * F * C
            if T > 0.0:
                curvature = 'strictly_convex'
            elif T < 0.0:
                curvature = 'strictly_concave'
            else:
                curvature = 'affine'
            w.writerow({
                'analysis':'phase3_primitive_curvature_pullback',
                'regime':r['regime'],
                'lambda_start':r['lambda_start'],
                'lambda_end':r['lambda_end'],
                'C':repr(C),'D':repr(D),'E':repr(E),'F':repr(F),'T':repr(T),
                'curvature_class':curvature,
                'certificate':'T=E-FD+F^2C; sign(T)=sign(Pi_second) when F>-1',
                'inference_level':'exact_primitive_pullback',
            })
    print(OUTPUT)
    print('PHASE3_PRIMITIVE_CURVATURE_PULLBACK_STATUS=PHASE3_PRIMITIVE_CURVATURE_PULLBACK_COMPLETE')

if __name__ == '__main__':
    main()
