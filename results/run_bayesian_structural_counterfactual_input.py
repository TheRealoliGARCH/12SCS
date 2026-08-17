"""Create the canonical input artifact for Bayesian structural counterfactual analysis.

This step intentionally separates deterministic primitive reconstruction from
Bayesian uncertainty analysis.
"""
from __future__ import annotations
import csv
from pathlib import Path

SOURCE = Path("results/convergence_primitive_counterfactual_coefficient_map_v1.csv")
OUTPUT = Path("results/bayesian_structural_counterfactual_cells_v1.csv")

REQUIRED = {
    "A", "B", "C", "D", "E", "F",
    "lambda_start", "lambda_end", "D_cf_unit", "E_cf_unit"
}


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)

    with SOURCE.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise ValueError("empty primitive counterfactual map")
    if not REQUIRED.issubset(rows[0]):
        missing = sorted(REQUIRED - set(rows[0]))
        raise ValueError(f"missing canonical fields: {missing}")

    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "A", "B", "C", "D", "E", "F",
            "lambda_start", "lambda_end",
            "d", "D_cf_unit", "E_cf_unit", "weight"
        ])
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "A": row["A"], "B": row["B"], "C": row["C"],
                "D": row["D"], "E": row["E"], "F": row["F"],
                "lambda_start": row["lambda_start"],
                "lambda_end": row["lambda_end"],
                "d": row.get("d", "1.0"),
                "D_cf_unit": row["D_cf_unit"],
                "E_cf_unit": row["E_cf_unit"],
                "weight": row.get("weight", "1.0"),
            })

    print(OUTPUT)


if __name__ == "__main__":
    main()
