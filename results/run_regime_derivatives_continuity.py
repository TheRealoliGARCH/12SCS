"""Derive exact regime coefficients, first/second derivatives, and breakpoint continuity."""
from __future__ import annotations
import csv
import math
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from model.convergence_analysis import CAPABILITIES, STATES
RESULTS = ROOT / "results"
CONTINUITY_TOL = 1e-6

def read_vector(path):
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    return tuple(float(r[1]) for r in rows[1:])

def read_matrix(path):
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    return tuple(tuple(float(x) for x in r[1:]) for r in rows[1:])

def derivs(A, B, C, D, E, F, x):
    q = 1.0 + F * x
    n = C + D*x + E*x*x
    n1 = D + 2.0*E*x
    d1 = B + (n1*q - F*n)/(q*q)
    d2 = 2.0*E/q - 2.0*F*n1/(q*q) + 2.0*F*F*n/(q*q*q)
    return d1, d2

def coefficients(binding_labels, marginal_label, positive, weights, feasibility_base, costs_base):
    index = {f"{STATES[i]}:{CAPABILITIES[j]}": (i,j)
             for i in range(len(STATES)) for j in range(len(CAPABILITIES))}
    p0 = p1 = 0.0
    s0, s1, s2 = 0.0, 0.0, 0.0
    for label in binding_labels:
        i,j = index[label]
        g = positive[i][j]
        k = feasibility_base[i][j] - 1.0
        c = costs_base[i][j] - 1.0
        p0 += weights[j] * g
        p1 += weights[j] * g * k
        s0 += g
        s1 += g * (k + c)
        s2 += g * k * c
    if marginal_label:
        i,j = index[marginal_label]
        cm = costs_base[i][j] - 1.0
        wm = weights[j]
        A = p0
        B = p1
        C = wm * (1.0 - s0)
        D = -wm * s1
        E = -wm * s2
        F = cm
    else:
        A = p0
        B = p1
        C = D = E = F = 0.0
    return A,B,C,D,E,F

def value(coef, x):
    A,B,C,D,E,F = coef
    return A + B*x + (C + D*x + E*x*x)/(1.0 + F*x)

def main():
    positive = read_matrix(RESULTS / "capability_gap_positive_v2.csv")
    weights = read_vector(RESULTS / "capability_dispersion_weights_v2.csv")
    feasibility_base, costs_base = __import__("model.heterogeneous_scenario", fromlist=["build_scenario"]).build_scenario(STATES, CAPABILITIES)
    source = RESULTS / "convergence_exact_regime_value_functions_v2.csv"
    with source.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise AssertionError("no regime rows")
    out = RESULTS / "convergence_regime_derivatives_continuity_v2.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["regime","lambda_start","lambda_end","A","B","C","D","E","F","dPi_start","dPi_mid","dPi_end","ddPi_mid","value_jump_to_next"])
        coefs = []
        diagnostics = []
        for row in rows:
            binding = [x for x in row["binding_cells"].split(";") if x]
            marginal = [x for x in row["marginal_cells"].split(";") if x]
            if len(marginal) > 1:
                raise AssertionError(f"multiple marginal cells in regime {row['regime']}")
            coef = coefficients(binding, marginal[0] if marginal else None, positive, weights, feasibility_base, costs_base)
            coefs.append(coef)
            left, right = float(row["lambda_start"]), float(row["lambda_end"])
            mid = (left + right)/2.0
            d0,_ = derivs(*coef, left)
            dm,d2m = derivs(*coef, mid)
            d1,_ = derivs(*coef, right)
            diagnostics.append([row["regime"],left,right,*coef,d0,dm,d1,d2m])
        for i, (a,b) in enumerate(zip(rows, rows[1:])):
            x = float(a["lambda_end"])
            va = value(coefs[i], x)
            vb = value(coefs[i+1], x)
            jump = abs(va-vb)
            if jump > CONTINUITY_TOL:
                raise AssertionError(f"value discontinuity at lambda={x}: {va} vs {vb} (jump={jump})")
            if not all(math.isfinite(z) for z in (va,vb,jump)):
                raise AssertionError("non-finite breakpoint value")
            diagnostics[i].append(jump)
        diagnostics[-1].append(0.0)
        writer.writerows(diagnostics)
    print(f"Derived derivatives and continuity diagnostics for {len(rows)} regimes; max breakpoint value jump <= {CONTINUITY_TOL:g}.")

if __name__ == "__main__":
    main()
