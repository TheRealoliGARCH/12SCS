"""Create the canonical input artifact for Bayesian structural counterfactual analysis.

The primitive counterfactual map is affine in the intervention delta:

    D(delta) = D + delta * D_slope
    E(delta) = E + delta * E_slope.

This generator materializes the exact unit-intervention coefficients rather
than requiring those columns to exist in the upstream deterministic artifact.
"""
from __future__ import annotations
import csv
from pathlib import Path

SOURCE = Path("results/convergence_primitive_counterfactual_coefficient_map_v1.csv")
OUTPUT = Path("results/bayesian_structural_counterfactual_cells_v1.csv")

REQUIRED = {
    "A", "B", "C", "D", "E", "F",
    "D_slope", "E_slope", "lambda_start", "lambda_end"
}


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)

    with SOURCE.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise ValueError("empty primitive counterfactual map")
    missing = sorted(REQUIRED - set(rows[0]))
    if missing:
        raise ValueError(f"missing canonical fields: {missing}")

    fields = [
        "A", "B", "C", "D", "E", "F",
        "lambda_start", "lambda_end",
        "d", "D_cf_unit", "E_cf_unit", "weight"
    ]
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            D = float(row["D"])
            E = float(row["E"])
            D_slope = float(row["D_slope"])
            E_slope = float(row["E_slope"])
            writer.writerow({
                "A": row["A"], "B": row["B"], "C": row["C"],
                "D": row["D"], "E": row["E"], "F": row["F"],
                "lambda_start": row["lambda_start"],
                "lambda_end": row["lambda_end"],
                "d": "1.0",
                "D_cf_unit": repr(D + D_slope),
                "E_cf_unit": repr(E + E_slope),
                "weight": row.get("weight", "1.0"),
            })

    print(OUTPUT)


if __name__ == "__main__":
    main()
