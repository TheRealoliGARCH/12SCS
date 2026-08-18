"""Record the recovered authoritative primitive-to-coefficient map."""
from __future__ import annotations

import csv
from pathlib import Path

OUTPUT = Path("results/phase2_primitive_map_discovery_v1.csv")

ROWS = [
    ("canonical_source_artifact", "canonical primitive-to-(A,B,C,D,E,F) source", "recovered", "results/run_primitive_coefficient_map.py at historical commit ab52d05e47302bbe8b24da44b52f8e76951ef39f"),
    ("primitive_variable_list", "primitive variables", "recovered", "Binding cells use g_i, w_i, a_i=kappa_i^0-1, d_i=c_i^0-1; marginal cell m supplies F=d_m"),
    ("coefficient_A", "formula for A", "recovered", "A=sum_i w_i*g_i"),
    ("coefficient_B", "formula for B", "recovered", "B=sum_i w_i*g_i*a_i"),
    ("coefficient_C", "formula for C", "recovered", "C=r0=B0-sum_i g_i"),
    ("coefficient_D", "formula for D", "recovered", "D=r1=-sum_i g_i*(a_i+d_i)"),
    ("coefficient_E", "formula for E", "recovered", "E=r2=-sum_i g_i*a_i*d_i"),
    ("coefficient_F", "formula for F", "recovered", "F=d_m for the marginal cell; F=0 when no marginal cell is present"),
    ("primitive_domain", "primitive-domain restrictions", "recovered", "g_i>=0, w_i>=0, kappa_i^0 in [0,1], c_i^0>0 imply a_i in [-1,0], d_i>-1, and F>-1"),
    ("endogenous_signs", "endogenous sign consequences", "partially_derivable", "F>-1 is endogenous; q2=2*F^2*E=-2*F^2*sum_i g_i*a_i*d_i, so uniform d_i>=0 implies q2>=0 and uniform d_i<=0 implies q2<=0; signs of p0, S, and T require additional primitive inequalities"),
]


def main() -> None:
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["analysis", "required_object", "description", "discovery_status", "boundary_statement", "inference_level"])
        w.writeheader()
        for required_object, description, status, boundary in ROWS:
            w.writerow({
                "analysis": "phase2_primitive_map_discovery",
                "required_object": required_object,
                "description": description,
                "discovery_status": status,
                "boundary_statement": boundary,
                "inference_level": "primitive_map_recovered_from_repository_history",
            })
    print(OUTPUT)
    print("PHASE2_PRIMITIVE_MAP_DISCOVERY_STATUS=PHASE2_PRIMITIVE_MAP_DISCOVERY_COMPLETE")


if __name__ == "__main__":
    main()
