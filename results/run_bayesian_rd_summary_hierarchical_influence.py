"""Quantify leave-one-country-out influence on hierarchical RD summary pooling."""
from __future__ import annotations

import csv
import math
from pathlib import Path

FULL = Path("results/bayesian_rd_summary_hierarchical_pooling_v1.csv")
LOO = Path("results/bayesian_rd_summary_hierarchical_leave_one_out_v1.csv")
OUTPUT = Path("results/bayesian_rd_summary_hierarchical_influence_v1.csv")


def main() -> None:
    full_rows = list(csv.DictReader(FULL.open(encoding="utf-8")))
    loo_rows = list(csv.DictReader(LOO.open(encoding="utf-8")))
    if len(full_rows) != 1:
        raise ValueError("expected exactly one full-sample pooling row")
    if len(loo_rows) != 3:
        raise ValueError("expected exactly three leave-one-out rows")
    full = full_rows[0]
    mu = float(full["posterior_mu_mean"])
    sd = float(full["posterior_mu_sd"])
    pneg = float(full["posterior_mu_prob_negative"])
    if not math.isfinite(mu) or sd <= 0.0 or not (0.0 <= pneg <= 1.0):
        raise ValueError("invalid full-sample posterior")

    out = []
    for row in loo_rows:
        loo_mu = float(row["posterior_mu_mean"])
        loo_sd = float(row["posterior_mu_sd"])
        loo_pneg = float(row["posterior_mu_prob_negative"])
        if not math.isfinite(loo_mu) or loo_sd <= 0.0 or not (0.0 <= loo_pneg <= 1.0):
            raise ValueError("invalid leave-one-out posterior")
        delta_mu = loo_mu - mu
        delta_sd = loo_sd - sd
        delta_pneg = loo_pneg - pneg
        standardized_shift = delta_mu / sd
        out.append({
            "analysis": "bayesian_rd_summary_hierarchical_influence",
            "omitted_country": row["omitted_country"],
            "full_posterior_mu_mean": mu,
            "leave_one_out_posterior_mu_mean": loo_mu,
            "delta_posterior_mu_mean": delta_mu,
            "full_posterior_mu_sd": sd,
            "leave_one_out_posterior_mu_sd": loo_sd,
            "delta_posterior_mu_sd": delta_sd,
            "standardized_mean_shift_full_sd": standardized_shift,
            "full_posterior_mu_prob_negative": pneg,
            "leave_one_out_posterior_mu_prob_negative": loo_pneg,
            "delta_posterior_mu_prob_negative": delta_pneg,
            "absolute_mean_shift": abs(delta_mu),
            "absolute_sign_probability_shift": abs(delta_pneg),
            "source_type": "reported_estimate_and_standard_error",
            "inference_level": "summary_data_hierarchical_influence",
        })
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)
    print(OUTPUT)
    print("RD_SUMMARY_HIERARCHICAL_INFLUENCE_STATUS=RD_SUMMARY_HIERARCHICAL_INFLUENCE_COMPLETE")


if __name__ == "__main__":
    main()
