"""Recover exact adjacent-regime intersection points from rational value functions."""
from __future__ import annotations
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
TOL = 1e-8


def value(coef, x):
    A, B, C, D, E, F = coef
    q = 1.0 + F*x
    return A + B*x + (C + D*x + E*x*x)/q


def difference_polynomial(a, b):
    """Return coefficients of numerator of value(a)-value(b), ascending powers."""
    A,B,C,D,E,F = a
    G,H,I,J,K,L = b
    # (A+Bx)(1+Lx) + C+Dx+Ex² times (1+Fx)
    # minus corresponding expression for b.
    p = [A + C, B + A*L + D, B*L + E, 0.0]
    q = [G + I, H + G*F + J, H*F + K, 0.0]
    # denominator product is common after cross multiplication.
    r = [p[i] for i in range(4)]
    s = [q[i] for i in range(4)]
    # Correct cross products explicitly.
    # N_a*(1+Lx) - N_b*(1+Fx)
    r = [0.0]*4
    r[0] = A + C - G - I
    r[1] = B + A*L + D - H - G*F - J
    r[2] = B*L + E - H*F - K
    r[3] = E*L - K*F
    return r


def roots_in_interval(coeff, lo, hi):
    # Degree <= 3; use numpy only if available in the repository runtime.
    import numpy as np
    trimmed = list(coeff)
    while len(trimmed) > 1 and abs(trimmed[-1]) < 1e-14:
        trimmed.pop()
    roots = np.roots(list(reversed(trimmed)))
    real = sorted(float(r.real) for r in roots if abs(float(r.imag)) < 1e-8)
    return [x for x in real if lo - TOL <= x <= hi + TOL]


def main():
    source = RESULTS / "convergence_regime_derivatives_continuity_v2.csv"
    if not source.exists():
        raise FileNotFoundError(source)
    with source.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    coefs = [tuple(float(r[k]) for k in ("A","B","C","D","E","F")) for r in rows]
    out = RESULTS / "convergence_exact_breakpoint_intersections_v2.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["boundary","reported_lambda","exact_intersection","local_error","value_left","value_right","value_gap"])
        for idx, (left_row, right_row) in enumerate(zip(rows[:-1], rows[1:]), start=1):
            reported = float(left_row["lambda_end"])
            candidates = roots_in_interval(difference_polynomial(coefs[idx-1], coefs[idx]), reported-1e-3, reported+1e-3)
            if not candidates:
                raise AssertionError(f"no adjacent rational intersection near lambda={reported}")
            x = min(candidates, key=lambda z: abs(z-reported))
            vl, vr = value(coefs[idx-1], x), value(coefs[idx], x)
            gap = abs(vl-vr)
            if gap > 1e-7:
                raise AssertionError(f"intersection mismatch at lambda={x}: {vl} vs {vr}")
            writer.writerow([idx, reported, x, abs(x-reported), vl, vr, gap])
    print(f"Recovered {max(0, len(rows)-1)} exact adjacent-regime intersections.")


if __name__ == "__main__":
    main()
