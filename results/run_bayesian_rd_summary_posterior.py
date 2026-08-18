"""Deterministic conjugate Bayesian posterior from reported RD estimates and SEs.

This is summary-data inference only and does not constitute observation-level
Bayesian regression-discontinuity estimation.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

INPUT = Path("results/rd_summary_bootstrap_v1.csv")
OUTPUT = Path("results/bayesian_rd_summary_posterior_v1.csv")
PRIOR_MEAN = 0.0
PRIOR_SD = 10.0


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def main() -> None:
    if not INPUT.exists():
        raise FileNotFoundError(f"missing summary bootstrap input: {INPUT}")
    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    if not rows:
        raise ValueError("summary bootstrap input contains no rows")
    out = []
    prior_var = PRIOR_SD ** 2
    for row in rows:
        estimate = float(row["estimate"])
        se = float(row["standard_error"])
        if not math.isfinite(estimate) or not math.isfinite(se) or se <= 0.0:
            raise ValueError("estimate must be finite and standard_error must be positive")
        likelihood_var = se ** 2
        posterior_var = 1.0 / (1.0 / prior_var + 1.0 / likelihood_var)
        posterior_sd = math.sqrt(posterior_var)
        posterior_mean = posterior_var * (PRIOR_MEAN / prior_var + estimate / likelihood_var)
        prob_negative = normal_cdf((0.0 - posterior_mean) / posterior_sd)
        prob_positive = 1.0 - prob_negative
        out.append({
            "country": row["country"],
            "estimate": estimate,
            "standard_error": se,
            "prior_mean": PRIOR_MEAN,
            "prior_sd": PRIOR_SD,
            "posterior_mean": posterior_mean,
            "posterior_sd": posterior_sd,
            "posterior_q025": posterior_mean - 1.959963984540054 * posterior_sd,
            "posterior_median": posterior_mean,
            "posterior_q975": posterior_mean + 1.959963984540054 * posterior_sd,
            "posterior_prob_negative": prob_negative,
            "posterior_prob_positive": prob_positive,
            "source_type": "reported_estimate_and_standard_error",
        })
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)
    print(OUTPUT)
    print("RD_SUMMARY_POSTERIOR_STATUS=RD_SUMMARY_POSTERIOR_COMPLETE")


if __name__ == "__main__":
    main()
