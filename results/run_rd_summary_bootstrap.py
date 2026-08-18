"""Deterministic parametric bootstrap from reported RD estimates and standard errors.

This is a summary-statistic testbed. It does not replace observation-level RD data.
"""
from __future__ import annotations

import csv
import math
import random
from pathlib import Path

OUTPUT = Path("results/rd_summary_bootstrap_v1.csv")
REPS = 10_000
SEED = 12032026
STUDIES = (
    ("Pakistan", -87.4, 35.4),
    ("Israel", 28.9, 9.2),
    ("North Korea", 43.1, 8.9),
)


def quantile(values: list[float], q: float) -> float:
    if not 0.0 <= q <= 1.0:
        raise ValueError("quantile probability must lie in [0,1]")
    x = sorted(values)
    if len(x) == 1:
        return x[0]
    position = (len(x) - 1) * q
    lo = math.floor(position)
    hi = math.ceil(position)
    if lo == hi:
        return x[lo]
    weight = position - lo
    return x[lo] * (1.0 - weight) + x[hi] * weight


def main() -> None:
    rows = []
    for index, (country, estimate, standard_error) in enumerate(STUDIES):
        if not math.isfinite(estimate) or not math.isfinite(standard_error) or standard_error <= 0.0:
            raise ValueError(f"invalid reported summary statistics for {country}")
        rng = random.Random(SEED + index)
        draws = [rng.gauss(estimate, standard_error) for _ in range(REPS)]
        prob_negative = sum(x < 0.0 for x in draws) / REPS
        prob_positive = sum(x >= 0.0 for x in draws) / REPS
        rows.append((
            country,
            estimate,
            standard_error,
            REPS,
            quantile(draws, 0.025),
            quantile(draws, 0.5),
            quantile(draws, 0.975),
            prob_negative,
            prob_positive,
            "reported_estimate_and_standard_error",
        ))
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "country", "estimate", "standard_error", "bootstrap_reps",
            "q025", "median", "q975", "prob_negative", "prob_positive",
            "source_type",
        ])
        writer.writerows(rows)
    print(OUTPUT)
    print("RD_SUMMARY_BOOTSTRAP_STATUS=RD_SUMMARY_BOOTSTRAP_COMPLETE")


if __name__ == "__main__":
    main()
