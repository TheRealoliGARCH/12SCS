"""Cross-diagnostic synthesis for Bayesian RD summary-data analyses."""
from __future__ import annotations

import csv
import math
from pathlib import Path

FILES = {
    "full": Path("results/bayesian_rd_summary_hierarchical_pooling_v1.csv"),
    "sensitivity": Path("results/bayesian_rd_summary_hierarchical_sensitivity_v1.csv"),
    "ppc": Path("results/bayesian_rd_summary_hierarchical_ppc_v1.csv"),
    "loo": Path("results/bayesian_rd_summary_hierarchical_leave_one_out_v1.csv"),
    "influence": Path("results/bayesian_rd_summary_hierarchical_influence_v1.csv"),
}
OUTPUT = Path("results/bayesian_rd_summary_cross_diagnostic_synthesis_v1.csv")


def rows(path):
    return list(csv.DictReader(path.open(encoding="utf-8")))


def main() -> None:
    data = {name: rows(path) for name, path in FILES.items()}
    if len(data["full"]) != 1 or len(data["sensitivity"]) != 5 or len(data["ppc"]) != 5 or len(data["loo"]) != 3 or len(data["influence"]) != 3:
        raise ValueError("unexpected diagnostic row counts")
    full = data["full"][0]
    mu = float(full["posterior_mu_mean"])
    sd = float(full["posterior_mu_sd"])
    pneg = float(full["posterior_mu_prob_negative"])
    sens_mu = [float(r["posterior_mu_mean"]) for r in data["sensitivity"]]
    sens_p = [float(r["posterior_mu_prob_negative"]) for r in data["sensitivity"]]
    loo_mu = [float(r["posterior_mu_mean"]) for r in data["loo"]]
    loo_p = [float(r["posterior_mu_prob_negative"]) for r in data["loo"]]
    ppc_p = [float(r["two_sided_predictive_tail_probability"]) for r in data["ppc"]]
    influence_abs_mu = [float(r["absolute_mean_shift"]) for r in data["influence"]]
    influence_abs_p = [float(r["absolute_sign_probability_shift"]) for r in data["influence"]]
    values = [mu, sd, pneg] + sens_mu + sens_p + loo_mu + loo_p + ppc_p + influence_abs_mu + influence_abs_p
    if not all(math.isfinite(x) for x in values) or sd <= 0.0:
        raise ValueError("non-finite diagnostic value")
    out = [
        ("full_sample", "posterior_mu_mean", mu),
        ("full_sample", "posterior_mu_sd", sd),
        ("full_sample", "posterior_mu_prob_negative", pneg),
        ("hyperprior_sensitivity", "posterior_mu_mean_min", min(sens_mu)),
        ("hyperprior_sensitivity", "posterior_mu_mean_max", max(sens_mu)),
        ("hyperprior_sensitivity", "posterior_mu_mean_range", max(sens_mu) - min(sens_mu)),
        ("hyperprior_sensitivity", "posterior_mu_prob_negative_min", min(sens_p)),
        ("hyperprior_sensitivity", "posterior_mu_prob_negative_max", max(sens_p)),
        ("leave_one_out", "posterior_mu_mean_min", min(loo_mu)),
        ("leave_one_out", "posterior_mu_mean_max", max(loo_mu)),
        ("leave_one_out", "max_absolute_mean_shift", max(influence_abs_mu)),
        ("leave_one_out", "max_absolute_sign_probability_shift", max(influence_abs_p)),
        ("posterior_predictive_check", "minimum_tail_probability", min(ppc_p)),
        ("posterior_predictive_check", "maximum_tail_probability", max(ppc_p)),
    ]
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["analysis", "diagnostic_layer", "metric", "value", "source_type", "inference_level"])
        writer.writeheader()
        for layer, metric, value in out:
            writer.writerow({
                "analysis": "bayesian_rd_summary_cross_diagnostic_synthesis",
                "diagnostic_layer": layer,
                "metric": metric,
                "value": value,
                "source_type": "reported_estimate_and_standard_error",
                "inference_level": "summary_data_cross_diagnostic_synthesis",
            })
    print(OUTPUT)
    print("RD_SUMMARY_CROSS_DIAGNOSTIC_SYNTHESIS_STATUS=RD_SUMMARY_CROSS_DIAGNOSTIC_SYNTHESIS_COMPLETE")


if __name__ == "__main__":
    main()
