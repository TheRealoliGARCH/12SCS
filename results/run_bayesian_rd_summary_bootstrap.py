"""Deterministic parametric bootstrap from supplied published RD estimates.

This is a bootstrap testbed based on reported effect estimates and standard errors,
not a substitute for observation-level RD resampling or Bayesian RD estimation.
"""
from __future__ import annotations

import csv
import math
import random
from pathlib import Path

OUTPUT = Path("results/bayesian_rd_summary_bootstrap_v1.csv")
N_REPS = 10_000
SEED = 12032026

# Source: supplied cross-country RDD paper, Table 7.
ESTIMATES = {
    "Pakistan": (-87.4, 35.4, "published_rd_effect_and_se"),
    "Israel": (28.9, 9.2, "published_rd_effect_and_se"),
    "North_Korea": (43.1, 8.9, "published_rd_effect_and_se_proxy_outcome"),
}


def quantile(sorted_values: list[float], p: float) -> float:
    if not 0.0 <= p <= 1.0:
        raise ValueError("quantile probability must lie in [0,1]")
    x = (len(sorted_values) - 1) * p
    lo = int(math.floor(x))
    hi = int(math.ceil(x))
    if lo == hi:
        return sorted_values[lo]
    return sorted_values[lo] + (x - lo) * (sorted_values[hi] - sorted_values[lo])


def main() -> None:
    rng = random.Random(SEED)
    rows = []
    for unit, (estimate, se, source_type) in ESTIMATES.items():
        if not math.isfinite(estimate) or not math.isfinite(se) or se <= 0.0:
            raise ValueError(f"invalid summary input for {unit}")
        draws = sorted(rng.gauss(estimate, se) for _ in range(N_REPS))
        rows.append((
            unit,
            estimate,
            se,
            N_REPS,
            quantile(draws, 0.025),
            quantile(draws, 0.50),
            quantile(draws, 0.975),
            sum(x < 0.0 for x in draws) / N_REPS,
            sum(x > 0.0 for x in draws) / N_REPS,
            source_type,
        ))
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "unit","reported_effect","reported_standard_error","bootstrap_replicates",
            "q025","q500","q975","prob_negative","prob_positive","source_type",
        ])
        w.writerows(rows)
    print(OUTPUT)
    print("RD_SUMMARY_BOOTSTRAP_STATUS=RD_SUMMARY_BOOTSTRAP_COMPLETE")


if __name__ == "__main__":
    main()
