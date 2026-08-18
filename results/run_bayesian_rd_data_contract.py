"""Validate the canonical data contract required for Bayesian sharp RD analysis.

This script defines and validates a contract only. It does not create observations.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

INPUT = Path("results/bayesian_rd_input_v1.csv")
OUTPUT = Path("results/bayesian_rd_data_contract_v1.csv")
REQUIRED = ("unit_id", "running_variable", "outcome", "treatment", "cutoff")


def as_float(value: str, field: str) -> float:
    try:
        x = float(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be numeric") from exc
    if not math.isfinite(x):
        raise ValueError(f"{field} must be finite")
    return x


def main() -> None:
    status = "RD_DATA_NOT_SUPPLIED"
    n_rows = 0
    sharp_assignment_verified = False
    cutoff_consistent = False
    if INPUT.exists():
        rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
        if not rows:
            raise ValueError("RD input exists but contains no observations")
        missing = set(REQUIRED) - set(rows[0])
        if missing:
            raise ValueError(f"missing canonical fields: {sorted(missing)}")
        cutoffs = set()
        sharp_assignment_verified = True
        for r in rows:
            unit_id = r["unit_id"].strip()
            if not unit_id:
                raise ValueError("unit_id must be nonempty")
            running = as_float(r["running_variable"], "running_variable")
            as_float(r["outcome"], "outcome")
            cutoff = as_float(r["cutoff"], "cutoff")
            treatment = r["treatment"].strip()
            if treatment not in {"0", "1"}:
                raise ValueError("treatment must be exactly 0 or 1")
            expected = "1" if running >= cutoff else "0"
            if treatment != expected:
                sharp_assignment_verified = False
            cutoffs.add(cutoff)
        n_rows = len(rows)
        cutoff_consistent = len(cutoffs) == 1
        if not cutoff_consistent:
            raise ValueError("all observations must share one canonical cutoff")
        status = "RD_DATA_CONTRACT_VALID" if sharp_assignment_verified else "RD_SHARP_ASSIGNMENT_VIOLATION"
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["input_present", "canonical_fields", "observation_count", "cutoff_consistent", "sharp_assignment_verified", "status"])
        w.writerow([INPUT.exists(), "|".join(REQUIRED), n_rows, cutoff_consistent, sharp_assignment_verified, status])
    print(OUTPUT)
    print("RD_DATA_CONTRACT_STATUS=" + status)


if __name__ == "__main__":
    main()
