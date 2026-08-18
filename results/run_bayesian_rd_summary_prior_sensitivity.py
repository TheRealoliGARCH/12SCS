"""Prior-scale sensitivity analysis for the Bayesian RD summary-data posterior."""
from __future__ import annotations

import csv
import math
from pathlib import Path

INPUT = Path("results/rd_summary_bootstrap_v1.csv")
OUTPUT = Path("results/bayesian_rd_summary_prior_sensitivity_v1.csv")
PRIOR_SCALES = (1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0)
Z975 = 1.959963984540054


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def main() -> None:
    if not INPUT.exists():
        raise FileNotFoundError(f"missing summary bootstrap input: {INPUT}")
    source = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    if not source:
        raise ValueError("summary bootstrap input contains no rows")

    out = []
    for row in source:
        estimate = float(row["estimate"])
        se = float(row["standard_error"])
        if not math.isfinite(estimate) or not math.isfinite(se) or se <= 0.0:
            raise ValueError("estimate must be finite and standard_error must be positive")
        likelihood_precision = 1.0 / (se * se)
        for prior_sd in PRIOR_SCALES:
            prior_precision = 1.0 / (prior_sd * prior_sd)
            posterior_var = 1.0 / (prior_precision + likelihood_precision)
            posterior_sd = math.sqrt(posterior_var)
            posterior_mean = posterior_var * estimate * likelihood_precision
            pneg = normal_cdf(-posterior_mean / posterior_sd)
            ppos = 1.0 - pneg
            out.append({
                "country": row["country"],
                "estimate": estimate,
                "standard_error": se,
                "prior_mean": 0.0,
                "prior_sd": prior_sd,
                "posterior_mean": posterior_mean,
                "posterior_sd": posterior_sd,
                "posterior_q025": posterior_mean - Z975 * posterior_sd,
                "posterior_median": posterior_mean,
                "posterior_q975": posterior_mean + Z975 * posterior_sd,
                "posterior_prob_negative": pneg,
                "posterior_prob_positive": ppos,
                "source_type": "reported_estimate_and_standard_error",
            })

    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)
    print(OUTPUT)
    print("RD_SUMMARY_PRIOR_SENSITIVITY_STATUS=RD_SUMMARY_PRIOR_SENSITIVITY_COMPLETE")


if __name__ == "__main__":
    main()
