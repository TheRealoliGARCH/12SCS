"""Deterministic posterior predictive check for hierarchical RD summary-data pooling."""
from __future__ import annotations

import csv
import math
import random
from pathlib import Path

INPUT = Path("results/rd_summary_bootstrap_v1.csv")
OUTPUT = Path("results/bayesian_rd_summary_hierarchical_ppc_v1.csv")
REPS = 10000
SEED = 20260818
MU_PRIOR_VAR = 100.0 ** 2
KAPPA_PRIOR_SD = 50.0
KAPPA_GRID_MAX = 300.0
KAPPA_GRID_SIZE = 6001


def main() -> None:
    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    if len(rows) != 3:
        raise ValueError("expected exactly three summary-data rows")
    countries = [r["country"] for r in rows]
    y = [float(r["estimate"]) for r in rows]
    se = [float(r["standard_error"]) for r in rows]
    if any(s <= 0.0 or not math.isfinite(s) for s in se):
        raise ValueError("standard errors must be positive and finite")

    grid = [KAPPA_GRID_MAX * i / (KAPPA_GRID_SIZE - 1) for i in range(KAPPA_GRID_SIZE)]
    delta = KAPPA_GRID_MAX / (KAPPA_GRID_SIZE - 1)
    logw, means, variances = [], [], []
    for kappa in grid:
        vs = [s * s + kappa * kappa for s in se]
        precision = 1.0 / MU_PRIOR_VAR + sum(1.0 / v for v in vs)
        var_mu = 1.0 / precision
        mean_mu = var_mu * sum(a / v for a, v in zip(y, vs))
        loglike = -0.5 * sum(math.log(v) + (a - mean_mu) ** 2 / v for a, v in zip(y, vs))
        logprior = -0.5 * (kappa / KAPPA_PRIOR_SD) ** 2
        logw.append(loglike + logprior)
        means.append(mean_mu)
        variances.append(var_mu)
    m = max(logw)
    weights = [math.exp(v - m) for v in logw]
    norm = sum(weights) * delta
    weights = [w / norm for w in weights]
    masses = [w * delta for w in weights]
    total = sum(masses)
    masses = [x / total for x in masses]
    cdf = []
    acc = 0.0
    for mass in masses:
        acc += mass
        cdf.append(acc)

    rng = random.Random(SEED)
    observed_max_abs = max(abs(v) for v in y)
    observed_range = max(y) - min(y)
    exceed_max_abs = 0
    exceed_range = 0
    country_exceed = [0, 0, 0]
    rep_means = [0.0, 0.0, 0.0]

    for _ in range(REPS):
        u = rng.random()
        idx = next(i for i, c in enumerate(cdf) if c >= u)
        kappa = grid[idx]
        mu = rng.gauss(means[idx], math.sqrt(variances[idx]))
        reps = [rng.gauss(mu, math.sqrt(kappa * kappa + s * s)) for s in se]
        for j, value in enumerate(reps):
            rep_means[j] += value
            if abs(value) >= abs(y[j]):
                country_exceed[j] += 1
        if max(abs(v) for v in reps) >= observed_max_abs:
            exceed_max_abs += 1
        if max(reps) - min(reps) >= observed_range:
            exceed_range += 1

    out = []
    for j, country in enumerate(countries):
        out.append({
            "analysis": "bayesian_rd_summary_hierarchical_posterior_predictive_check",
            "scope": "country",
            "country": country,
            "observed_estimate": y[j],
            "replicated_mean": rep_means[j] / REPS,
            "two_sided_predictive_tail_probability": country_exceed[j] / REPS,
            "source_type": "reported_estimate_and_standard_error",
            "inference_level": "summary_data_hierarchical_ppc",
        })
    out.extend([
        {
            "analysis": "bayesian_rd_summary_hierarchical_posterior_predictive_check",
            "scope": "global",
            "country": "ALL",
            "observed_estimate": observed_max_abs,
            "replicated_mean": observed_range,
            "two_sided_predictive_tail_probability": exceed_max_abs / REPS,
            "source_type": "reported_estimate_and_standard_error",
            "inference_level": "summary_data_hierarchical_ppc",
        },
        {
            "analysis": "bayesian_rd_summary_hierarchical_posterior_predictive_check",
            "scope": "global_range",
            "country": "ALL",
            "observed_estimate": observed_range,
            "replicated_mean": observed_range,
            "two_sided_predictive_tail_probability": exceed_range / REPS,
            "source_type": "reported_estimate_and_standard_error",
            "inference_level": "summary_data_hierarchical_ppc",
        },
    ])
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)
    print(OUTPUT)
    print("RD_SUMMARY_HIERARCHICAL_PPC_STATUS=RD_SUMMARY_HIERARCHICAL_PPC_COMPLETE")


if __name__ == "__main__":
    main()
