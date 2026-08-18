"""Leave-one-country-out robustness for Bayesian hierarchical RD summary-data pooling."""
from __future__ import annotations

import csv
import math
from pathlib import Path

INPUT = Path("results/rd_summary_bootstrap_v1.csv")
OUTPUT = Path("results/bayesian_rd_summary_hierarchical_leave_one_out_v1.csv")
MU_PRIOR_VAR = 100.0 ** 2
KAPPA_PRIOR_SD = 50.0
KAPPA_GRID_MAX = 300.0
KAPPA_GRID_SIZE = 6001
Z975 = 1.959963984540054


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def fit(y, se):
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
    shift = max(logw)
    weights = [math.exp(v - shift) for v in logw]
    norm = sum(weights) * delta
    weights = [w / norm for w in weights]
    mean_mu = sum(w * m for w, m in zip(weights, means)) * delta
    second = sum(w * (v + m * m) for w, v, m in zip(weights, variances, means)) * delta
    sd_mu = math.sqrt(max(0.0, second - mean_mu * mean_mu))
    mean_kappa = sum(w * k for w, k in zip(weights, grid)) * delta
    pneg = normal_cdf(-mean_mu / sd_mu) if sd_mu > 0 else float(mean_mu < 0)
    return mean_mu, sd_mu, pneg, mean_kappa


def main() -> None:
    rows = list(csv.DictReader(INPUT.open(encoding="utf-8")))
    if len(rows) != 3:
        raise ValueError("expected exactly three summary-data rows")
    countries = [r["country"] for r in rows]
    y = [float(r["estimate"]) for r in rows]
    se = [float(r["standard_error"]) for r in rows]
    if len(set(countries)) != 3 or any(s <= 0 or not math.isfinite(s) for s in se):
        raise ValueError("invalid country or standard-error inputs")

    out = []
    for omit in range(3):
        keep = [i for i in range(3) if i != omit]
        mean_mu, sd_mu, pneg, mean_kappa = fit([y[i] for i in keep], [se[i] for i in keep])
        out.append({
            "analysis": "bayesian_rd_summary_hierarchical_leave_one_out",
            "omitted_country": countries[omit],
            "included_country_count": len(keep),
            "posterior_mu_mean": mean_mu,
            "posterior_mu_sd": sd_mu,
            "posterior_mu_q025_normal_approx": mean_mu - Z975 * sd_mu,
            "posterior_mu_median_approx": mean_mu,
            "posterior_mu_q975_normal_approx": mean_mu + Z975 * sd_mu,
            "posterior_mu_prob_negative": pneg,
            "posterior_mu_prob_positive": 1.0 - pneg,
            "posterior_kappa_mean": mean_kappa,
            "source_type": "reported_estimate_and_standard_error",
            "inference_level": "summary_data_hierarchical_leave_one_out",
        })

    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)
    print(OUTPUT)
    print("RD_SUMMARY_HIERARCHICAL_LEAVE_ONE_OUT_STATUS=RD_SUMMARY_HIERARCHICAL_LEAVE_ONE_OUT_COMPLETE")


if __name__ == "__main__":
    main()
