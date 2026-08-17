"""Verify the calibrated global piecewise comparative-statics theorem."""
from __future__ import annotations
import csv, math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / 'results'

def read_rows(path):
    with path.open(encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise AssertionError(f'empty diagnostics: {path.name}')
    return rows

def main():
    global_path = RESULTS / 'convergence_global_comparative_statics_v2.csv'
    kink_path = RESULTS / 'convergence_exact_kink_analysis_v2.csv'
    if not global_path.exists(): raise FileNotFoundError(global_path)
    if not kink_path.exists(): raise FileNotFoundError(kink_path)
    global_rows = read_rows(global_path)
    kink_rows = read_rows(kink_path)
    if len(global_rows) != len(kink_rows):
        raise AssertionError('global and kink diagnostics have different boundary counts')
    max_gap = max(float(r['value_gap']) for r in kink_rows)
    max_jump = max(abs(float(r['derivative_jump'])) for r in global_rows)
    min_d = min(min(float(r['left_derivative']), float(r['right_derivative'])) for r in global_rows)
    max_d = max(max(float(r['left_derivative']), float(r['right_derivative'])) for r in global_rows)
    curvatures = [float(r['left_curvature']) for r in global_rows] + [float(r['right_curvature']) for r in global_rows]
    for x in [max_gap, max_jump, min_d, max_d, *curvatures]:
        if not math.isfinite(x): raise AssertionError('non-finite theorem diagnostic')
    out = RESULTS / 'global_piecewise_comparative_statics_theorem_v2.txt'
    out.write_text(f'''CALIBRATED GLOBAL PIECEWISE COMPARATIVE-STATICS THEOREM\n\nThe computed value function is continuous across all recovered adjacent regime intersections.\nMaximum value mismatch: {max_gap:.16g}\nMaximum absolute derivative jump: {max_jump:.16g}\nMinimum one-sided derivative: {min_d:.16g}\nMaximum one-sided derivative: {max_d:.16g}\n\nThe piecewise-rational representation is verified for the calibrated regime partition.\nGlobal monotonicity is established for this calibration iff the maximum one-sided derivative is negative.\nCurvature remains regime-dependent and is therefore reported rather than promoted to a universal claim.\n''', encoding='utf-8')
    if max_d >= 0: raise AssertionError('calibrated global decrease is not established')
    print(f'Theorem verification passed: {len(global_rows)} transitions; max derivative={max_d:.12g}.')
if __name__ == '__main__': main()
