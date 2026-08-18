"""Hyperprior sensitivity for Bayesian hierarchical pooling of RD summary data."""
from __future__ import annotations

import csv
import math
from pathlib import Path

INPUT = Path("results/rd_summary_bootstrap_v1.csv")
OUTPUT = Path("results/bayesian_rd_summary_hierarchical_sensitivity_v1.csv")
KAPPA_PRIOR_SDS = (5.0, 10.0, 20.0, 50.0, 100.0)
KAPPA_GRID_MAX = 300.0
KAPPA_GRID_SIZE = 6001
MU_PRIOR_VAR = 100.0 ** 2
Z975 = 1.959963984540054


def main() -> None:
    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    if len(rows) != 3:
        raise ValueError("expected exactly three summary-data rows")
    y = [float(r["estimate"]) for r in rows]
    se = [float(r["standard_error"]) for r in rows]
    if any((not math.isfinite(a)) for a in y) or any(s <= 0 or not math.isfinite(s) for s in se):
        raise ValueError("invalid summary estimates or standard errors")

    grid = [KAPPA_GRID_MAX * i / (KAPPA_GRID_SIZE - 1) for i in range(KAPPA_GRID_SIZE)]
    delta = KAPPA_GRID_MAX / (KAPPA_GRID_SIZE - 1)
    out = []

    for prior_sd in KAPPA_PRIOR_SDS:
        logw, means, variances = [], [], []
        for kappa in grid:
            vs = [s * s + kappa * kappa for s in se]
            precision = 1.0 / MU_PRIOR_VAR + sum(1.0 / v for v in vs)
            var_mu = 1.0 / precision
            mean_mu = var_mu * sum(a / v for a, v in zip(y, vs))
            loglike = -0.5 * sum(math.log(v) + (a - mean_mu) ** 2 / v for a, v in zip(y, vs))
            logprior = -0.5 * (kappa / prior_sd) ** 2
            logw.append(loglike + logprior)
            means.append(mean_mu)
            variances.append(var_mu)
        m = max(logw)
        weights = [math.exp(x - m) for x in logw]
        norm = sum(weights) * delta
        weights = [w / norm for w in weights]
        mean_mu = sum(w * a for w, a in zip(weights, means)) * delta
        second = sum(w * (v + a * a) for w, v, a in zip(weights, variances, means)) * delta
        var_mu = max(0.0, second - mean_mu * mean_mu)
        sd_mu = math.sqrt(var_mu)
        mean_kappa = sum(w * k for w, k in zip(weights, grid)) * delta
        # Moment-matched normal approximation for sign probabilities and interval summaries.
        pneg = 0.5 * (1.0 + math.erf((-mean_mu / sd_mu) / math.sqrt(2.0))) if sd_mu > 0 else float(mean_mu < 0)
        out.append({
            "analysis": "bayesian_rd_summary_hierarchical_hyperprior_sensitivity",
            "country_count": 3,
            "kappa_prior_family": "HalfNormal",
            "kappa_prior_sd": prior_sd,
            "posterior_mu_mean": mean_mu,
            "posterior_mu_sd": sd_mu,
            "posterior_mu_q025_normal_approx": mean_mu - Z975 * sd_mu,
            "posterior_mu_median_approx": mean_mu,
            "posterior_mu_q975_normal_approx": mean_mu + Z975 * sd_mu,
            "posterior_mu_prob_negative": pneg,
            "posterior_mu_prob_positive": 1.0 - pneg,
            "posterior_kappa_mean": mean_kappa,
            "source_type": "reported_estimate_and_standard_error",
            "inference_level": "summary_data_hierarchical_sensitivity",
        })

    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)
    print(OUTPUT)
    print("RD_SUMMARY_HIERARCHICAL_SENSITIVITY_STATUS=RD_SUMMARY_HIERARCHICAL_SENSITIVITY_COMPLETE")


if __name__ == "__main__":
    main()
