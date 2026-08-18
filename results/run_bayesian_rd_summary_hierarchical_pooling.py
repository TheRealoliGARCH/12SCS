"""Deterministic hierarchical Bayesian pooling for reported RD summary estimates.

This is summary-data inference only. It does not reconstruct or estimate an
observation-level regression-discontinuity model.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

INPUT = Path("results/rd_summary_bootstrap_v1.csv")
OUTPUT = Path("results/bayesian_rd_summary_hierarchical_pooling_v1.csv")
MU_PRIOR_SD = 100.0
KAPPA_PRIOR_SD = 50.0
GRID_SIZE = 2001
KAPPA_MAX = 200.0
Z975 = 1.959963984540054


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def main() -> None:
    if not INPUT.exists():
        raise FileNotFoundError(f"missing summary bootstrap input: {INPUT}")
    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    if len(rows) < 2:
        raise ValueError("hierarchical pooling requires at least two summary estimates")

    y = [float(r["estimate"]) for r in rows]
    se = [float(r["standard_error"]) for r in rows]
    if any((not math.isfinite(a)) for a in y) or any((not math.isfinite(s) or s <= 0.0) for s in se):
        raise ValueError("estimates must be finite and standard errors must be finite and positive")

    step = KAPPA_MAX / (GRID_SIZE - 1)
    components = []
    log_weights = []
    prior_mu_precision = 1.0 / (MU_PRIOR_SD * MU_PRIOR_SD)
    for i in range(GRID_SIZE):
        kappa = i * step
        variances = [s * s + kappa * kappa for s in se]
        precisions = [1.0 / v for v in variances]
        post_precision = prior_mu_precision + sum(precisions)
        post_var = 1.0 / post_precision
        post_mean = post_var * sum(a * p for a, p in zip(y, precisions))
        # Integrated Gaussian likelihood p(y | kappa), with mu integrated out.
        logdet = sum(math.log(v) for v in variances) + math.log(MU_PRIOR_SD * MU_PRIOR_SD * post_precision)
        quad = sum(a * a * p for a, p in zip(y, precisions)) - post_mean * post_mean / post_var
        log_like = -0.5 * (len(y) * math.log(2.0 * math.pi) + logdet + quad)
        # Half-normal prior on kappa, constants retained for numerical transparency.
        log_prior = math.log(math.sqrt(2.0 / math.pi) / KAPPA_PRIOR_SD) - 0.5 * (kappa / KAPPA_PRIOR_SD) ** 2
        trap = 0.5 if i in (0, GRID_SIZE - 1) else 1.0
        log_weights.append(log_like + log_prior + math.log(trap * step))
        components.append((kappa, post_mean, post_var))

    m = max(log_weights)
    weights = [math.exp(w - m) for w in log_weights]
    total = sum(weights)
    weights = [w / total for w in weights]
    pooled_mean = sum(w * c[1] for w, c in zip(weights, components))
    second = sum(w * (c[2] + c[1] * c[1]) for w, c in zip(weights, components))
    pooled_sd = math.sqrt(max(0.0, second - pooled_mean * pooled_mean))
    kappa_mean = sum(w * c[0] for w, c in zip(weights, components))
    prob_negative = sum(w * normal_cdf(-c[1] / math.sqrt(c[2])) for w, c in zip(weights, components))
    prob_positive = 1.0 - prob_negative

    out = [{
        "analysis": "three_country_summary_pool",
        "country_count": len(rows),
        "mu_prior_mean": 0.0,
        "mu_prior_sd": MU_PRIOR_SD,
        "kappa_prior_family": "HalfNormal",
        "kappa_prior_sd": KAPPA_PRIOR_SD,
        "kappa_grid_max": KAPPA_MAX,
        "kappa_grid_size": GRID_SIZE,
        "posterior_mu_mean": pooled_mean,
        "posterior_mu_sd": pooled_sd,
        "posterior_mu_q025_normal_approx": pooled_mean - Z975 * pooled_sd,
        "posterior_mu_median_approx": pooled_mean,
        "posterior_mu_q975_normal_approx": pooled_mean + Z975 * pooled_sd,
        "posterior_mu_prob_negative": prob_negative,
        "posterior_mu_prob_positive": prob_positive,
        "posterior_kappa_mean": kappa_mean,
        "source_type": "reported_estimate_and_standard_error",
        "inference_level": "summary_data_not_observation_level_rd",
    }]
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)
    print(OUTPUT)
    print("RD_SUMMARY_HIERARCHICAL_POOLING_STATUS=RD_SUMMARY_HIERARCHICAL_POOLING_COMPLETE")


if __name__ == "__main__":
    main()
