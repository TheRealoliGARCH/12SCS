"""Classify exact active-set transitions by derivative matching and curvature."""
from __future__ import annotations
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
TOL = 1e-7


def value(c, x):
    A, B, C, D, E, F = c
    q = 1.0 + F*x
    return A + B*x + (C + D*x + E*x*x)/q


def derivatives(c, x):
    A, B, C, D, E, F = c
    q = 1.0 + F*x
    n = C + D*x + E*x*x
    n1 = D + 2.0*E*x
    d1 = B + (n1*q - F*n)/(q*q)
    d2 = 2.0*E/q - 2.0*F*n1/(q*q) + 2.0*F*F*n/(q*q*q)
    return d1, d2


def main():
    source = RESULTS / "convergence_regime_derivatives_continuity_v2.csv"
    intersections = RESULTS / "convergence_exact_breakpoint_intersections_v2.csv"
    if not source.exists() or not intersections.exists():
        raise FileNotFoundError("required derivative/intersection artifacts are missing")
    with source.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    with intersections.open(encoding="utf-8", newline="") as f:
        cuts = list(csv.DictReader(f))
    coefs = [tuple(float(r[k]) for k in ("A","B","C","D","E","F")) for r in rows]
    if len(cuts) != max(0, len(rows)-1):
        raise AssertionError("intersection count does not match regime boundaries")
    out = RESULTS / "convergence_exact_kink_analysis_v2.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["boundary","lambda_exact","value_gap","left_derivative","right_derivative","derivative_jump","left_curvature","right_curvature","transition"])
        for k, cut in enumerate(cuts):
            x = float(cut["exact_intersection"])
            vl = value(coefs[k], x)
            vr = value(coefs[k+1], x)
            dl, d2l = derivatives(coefs[k], x)
            dr, d2r = derivatives(coefs[k+1], x)
            gap = abs(vl-vr)
            jump = dr-dl
            if not all(math.isfinite(z) for z in (x, vl, vr, dl, dr, d2l, d2r, gap, jump)):
                raise AssertionError(f"non-finite kink diagnostic at boundary {k+1}")
            if gap > TOL:
                raise AssertionError(f"value mismatch at exact intersection {x}: {gap}")
            transition = "C1" if abs(jump) <= TOL else "KINK"
            w.writerow([k+1, x, gap, dl, dr, jump, d2l, d2r, transition])
    print(f"Classified {len(cuts)} exact regime transitions.")


if __name__ == "__main__":
    main()
