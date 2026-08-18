"""Phase III sharpness witnesses from the realizable primitive curvature pullback."""
from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / 'results'
PULLBACK = RESULTS / 'run_phase3_primitive_curvature_pullback.py'
SOURCE = RESULTS / 'phase3_primitive_curvature_pullback_v1.csv'
OUTPUT = RESULTS / 'phase3_primitive_curvature_sharpness_v1.csv'


def main() -> None:
    subprocess.run([sys.executable, str(PULLBACK)], cwd=ROOT, check=True)
    with SOURCE.open(encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))
    by_class = {}
    for r in rows:
        by_class.setdefault(r['curvature_class'], r)
    required = ['strictly_convex', 'affine', 'strictly_concave']
    with OUTPUT.open('w', encoding='utf-8', newline='') as f:
        fields = ['analysis','witness_type','regime','C','D','E','F','T','curvature_class','attainability','certificate','inference_level']
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for cls in required:
            if cls in by_class:
                r = by_class[cls]
                C,D,E,F,T = (float(r[k]) for k in ('C','D','E','F','T'))
                w.writerow({'analysis':'phase3_primitive_curvature_sharpness','witness_type':cls,'regime':r['regime'],'C':repr(C),'D':repr(D),'E':repr(E),'F':repr(F),'T':repr(T),'curvature_class':cls,'attainability':'realized_by_primitive_map','certificate':'realized primitive regime; T=E-FD+F^2C','inference_level':'constructive_primitive_witness'})
            else:
                w.writerow({'analysis':'phase3_primitive_curvature_sharpness','witness_type':cls,'regime':'','C':'','D':'','E':'','F':'','T':'','curvature_class':cls,'attainability':'not_witnessed_in_current_map','certificate':'no realized witness emitted by current primitive pullback','inference_level':'constructive_primitive_witness'})
    print(OUTPUT)
    print('PHASE3_PRIMITIVE_CURVATURE_SHARPNESS_STATUS=PHASE3_PRIMITIVE_CURVATURE_SHARPNESS_COMPLETE')

if __name__ == '__main__':
    main()
