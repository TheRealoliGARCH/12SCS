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
    q = 1.0 + F * x
    return A + B*x + (C + D*x + E*x*x)/q


def difference_polynomial(a, b):
    """Return coefficients of the cross-multiplied numerator of Pi_a-Pi_b."""
    A, B, C, D, E, F = a
    G, H, I, J, K, L = b
    # N_a = (A+Bx)(1+Fx) + C+Dx+Ex^2.
    # N_b = (G+Hx)(1+Lx) + I+Jx+Kx^2.
    # The common-denominator numerator is
    # N_a(1+Lx) - N_b(1+Fx).
    return [
        A + C - G - I,
        A*F + A*L + B + C*L + D - F*G - F*I - G*L - H - J,
        A*F*L + B*F + B*L + D*L + E - F*G*L - F*H - F*J - H*L - K,
        B*F*L + E*L - F*H*L - F*K,
    ]


def roots_in_interval(coeff, lo, hi):
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
            candidates = roots_in_interval(
                difference_polynomial(coefs[idx-1], coefs[idx]),
                reported - 1e-3,
                reported + 1e-3,
            )
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
