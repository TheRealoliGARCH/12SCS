"""Assemble global monotonicity and curvature diagnostics from exact regimes."""
from __future__ import annotations
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

def main():
    source = RESULTS / "convergence_exact_kink_analysis_v2.csv"
    if not source.exists():
        raise FileNotFoundError(source)
    with source.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise AssertionError("no exact transition diagnostics")
    out = RESULTS / "convergence_global_comparative_statics_v2.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["boundary","lambda_exact","left_derivative","right_derivative","derivative_jump","left_curvature","right_curvature","transition","global_slope_sign","curvature_transition"])
        for r in rows:
            dl = float(r["left_derivative"])
            dr = float(r["right_derivative"])
            d2l = float(r["left_curvature"])
            d2r = float(r["right_curvature"])
            vals = [float(r[k]) for k in ("lambda_exact","left_derivative","right_derivative","derivative_jump","left_curvature","right_curvature")]
            if not all(math.isfinite(x) for x in vals):
                raise AssertionError(f"non-finite global diagnostic at boundary {r['boundary']}")
            slope_sign = "DECREASING" if dl < 0 and dr < 0 else "INCREASING" if dl > 0 and dr > 0 else "SLOPE-CROSSING"
            curvature_transition = "CONVEX" if d2l > 1e-10 and d2r > 1e-10 else "CONCAVE" if d2l < -1e-10 and d2r < -1e-10 else "CURVATURE-CHANGE"
            w.writerow([r["boundary"], r["lambda_exact"], dl, dr, r["derivative_jump"], d2l, d2r, r["transition"], slope_sign, curvature_transition])
    if any(float(r["left_derivative"]) > 1e-8 or float(r["right_derivative"]) > 1e-8 for r in rows):
        raise AssertionError("observed positive one-sided derivative; global decreasing claim fails")
    print(f"Global comparative-statics diagnostics assembled for {len(rows)} transitions.")

if __name__ == "__main__": main()
