"""Exact primitive substitutions and sign-classification boundary for Phase II."""
from __future__ import annotations

import csv
from pathlib import Path

OUTPUT = Path("results/phase2_primitive_sign_restrictions_v1.csv")

ROWS = [
    ("primitive_map", "B", "sum_i w_i*g_i*a_i", "identity", "canonical recovered primitive map"),
    ("primitive_map", "C", "B0-sum_i g_i", "identity", "canonical recovered primitive map"),
    ("primitive_map", "D", "-sum_i g_i*(a_i+d_i)", "identity", "canonical recovered primitive map"),
    ("primitive_map", "E", "-sum_i g_i*a_i*d_i", "identity", "canonical recovered primitive map"),
    ("primitive_map", "F", "d_m", "identity", "canonical recovered primitive map"),
    ("substitution", "p0", "sum_i w_i*g_i*a_i-sum_i g_i*(a_i+d_i)-d_m*(B0-sum_i g_i)", "identity", "p0=B+D-F*C"),
    ("substitution", "S", "d_m*sum_i w_i*g_i*a_i-sum_i g_i*a_i*d_i", "identity", "S=B*F+E"),
    ("substitution", "T", "-sum_i g_i*a_i*d_i+d_m*sum_i g_i*(a_i+d_i)+d_m^2*(B0-sum_i g_i)", "identity", "T=E-F*D+F^2*C"),
    ("structural_bridge", "q0", "2*T", "identity", "q0=2T"),
    ("structural_bridge", "Delta_P", "4*S*T=2*S*q0", "identity", "discriminant factorization"),
    ("basic_domain", "F>-1", "d_m>-1 implies F>-1", "endogenous", "denominator positivity follows from primitive domain"),
    ("basic_domain", "sign(p0)", "not fixed", "not_derivable", "basic domain does not determine sign"),
    ("basic_domain", "sign(S)", "not fixed", "not_derivable", "basic domain does not determine sign"),
    ("basic_domain", "sign(T)", "not fixed", "not_derivable", "basic domain does not determine sign"),
    ("additional_condition", "p0<0", "primitive substituted inequality p0<0", "additional_assumption", "sufficient condition retained at primitive level"),
    ("additional_condition", "S>=0", "d_m*sum_i w_i*g_i*a_i-sum_i g_i*a_i*d_i>=0", "additional_assumption", "convex branch condition"),
    ("additional_condition", "S<0 and T>0", "primitive substituted inequalities S<0 and T>0", "additional_assumption", "equivalent to p2<0 and Delta_P<0 when F>0; otherwise coefficient condition should be checked directly"),
]


def main() -> None:
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["analysis", "layer", "quantity", "primitive_expression_or_condition", "classification", "basis", "inference_level"])
        writer.writeheader()
        for layer, quantity, expression, classification, basis in ROWS:
            writer.writerow({
                "analysis": "phase2_primitive_sign_restrictions",
                "layer": layer,
                "quantity": quantity,
                "primitive_expression_or_condition": expression,
                "classification": classification,
                "basis": basis,
                "inference_level": "primitive_to_structural_sign_classification",
            })
    print(OUTPUT)
    print("PHASE2_PRIMITIVE_SIGN_RESTRICTIONS_STATUS=PHASE2_PRIMITIVE_SIGN_RESTRICTIONS_COMPLETE")


if __name__ == "__main__":
    main()
