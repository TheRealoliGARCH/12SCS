"""Deterministic Bayesian causal-inference baseline for 12SCSM.

This first implementation is deliberately an identification and posterior-
summary layer rather than a black-box MCMC engine.  It uses a finite set of
binary treatment/outcome cells, an explicit Dirichlet prior, and computes the
posterior distribution of a causal risk difference under the standard
conditional-exchangeability intervention functional.

The model is:
    T in {0,1}, Y in {0,1}, Z in {0,...,K-1}
with independent Dirichlet priors on p(Y,T | Z=z).  For each stratum,
posterior cell probabilities are Dirichlet.  The posterior causal risk
under intervention do(T=t) is the weighted standardised sum of
P(Y=1 | T=t,Z=z), with fixed positive stratum weights.

No causal claim is made without the explicit exchangeability assumption.
"""
from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path
from random import Random


@dataclass(frozen=True)
class Observation:
    z: int
    treatment: int
    outcome: int
    count: int


@dataclass(frozen=True)
class PosteriorSummary:
    risk_do_0_mean: float
    risk_do_1_mean: float
    ate_mean: float
    ate_sd: float
    p_ate_positive: float


def validate_observations(observations: list[Observation], weights: list[float]) -> None:
    if not observations:
        raise ValueError("observations must not be empty")
    if any(o.z < 0 or o.treatment not in (0, 1) or o.outcome not in (0, 1) or o.count < 0 for o in observations):
        raise ValueError("invalid observation cell")
    if not weights or any(w <= 0 or not math.isfinite(w) for w in weights):
        raise ValueError("weights must be positive and finite")
    if abs(sum(weights) - 1.0) > 1e-10:
        raise ValueError("weights must sum to one")


def posterior_parameters(observations: list[Observation], strata: int, prior: float = 1.0) -> list[list[float]]:
    if strata <= 0 or prior <= 0:
        raise ValueError("strata and prior must be positive")
    alpha = [[prior] * 4 for _ in range(strata)]
    for o in observations:
        alpha[o.z][2 * o.treatment + o.outcome] += o.count
    return alpha


def posterior_mean_risks(alpha: list[list[float]]) -> tuple[list[float], list[float]]:
    risks0: list[float] = []
    risks1: list[float] = []
    for a in alpha:
        # cell order: (T=0,Y=0), (T=0,Y=1), (T=1,Y=0), (T=1,Y=1)
        risks0.append(a[1] / (a[0] + a[1]))
        risks1.append(a[3] / (a[2] + a[3]))
    return risks0, risks1


def draw_dirichlet(gamma: list[float], rng: Random) -> list[float]:
    xs = [rng.gammavariate(a, 1.0) for a in gamma]
    total = sum(xs)
    return [x / total for x in xs]


def posterior_summary(observations: list[Observation], weights: list[float], draws: int = 20000, seed: int = 20260817, prior: float = 1.0) -> PosteriorSummary:
    strata = len(weights)
    validate_observations(observations, weights)
    alpha = posterior_parameters(observations, strata, prior)
    mean0, mean1 = posterior_mean_risks(alpha)
    risk0_mean = sum(w * r for w, r in zip(weights, mean0))
    risk1_mean = sum(w * r for w, r in zip(weights, mean1))

    rng = Random(seed)
    ates: list[float] = []
    for _ in range(draws):
        r0: list[float] = []
        r1: list[float] = []
        for a in alpha:
            p = draw_dirichlet(a, rng)
            r0.append(p[1] / (p[0] + p[1]))
            r1.append(p[3] / (p[2] + p[3]))
        ates.append(sum(w * (b - a) for w, a, b in zip(weights, r0, r1)))
    ate_mean = sum(ates) / len(ates)
    ate_var = sum((x - ate_mean) ** 2 for x in ates) / (len(ates) - 1)
    return PosteriorSummary(risk0_mean, risk1_mean, ate_mean, math.sqrt(ate_var), sum(x > 0 for x in ates) / len(ates))


def main() -> None:
    # Reproducible smoke-test dataset.  Future versions will replace this with
    # the declared V6 regime-level observational dataset without changing the
    # identification interface.
    observations = [
        Observation(0, 0, 0, 35), Observation(0, 0, 1, 15),
        Observation(0, 1, 0, 25), Observation(0, 1, 1, 25),
        Observation(1, 0, 0, 30), Observation(1, 0, 1, 20),
        Observation(1, 1, 0, 20), Observation(1, 1, 1, 30),
    ]
    weights = [0.5, 0.5]
    summary = posterior_summary(observations, weights)
    out = Path("results/bayesian_causal_inference_v1.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["risk_do_0_mean", "risk_do_1_mean", "ate_mean", "ate_sd", "p_ate_positive"])
        writer.writerow([summary.risk_do_0_mean, summary.risk_do_1_mean, summary.ate_mean, summary.ate_sd, summary.p_ate_positive])
    print(out)
    print(f"ATE posterior mean={summary.ate_mean:.10f}, sd={summary.ate_sd:.10f}, P(ATE>0)={summary.p_ate_positive:.10f}")


if __name__ == "__main__":
    main()
