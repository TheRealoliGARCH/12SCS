# Capability Convergence Estimator v2

## Purpose

Version 1 used only the ordinal recognition level $R/4$. Version 2 uses the latent measurement fields collected in the evidence ledgers while preserving a strict distinction between capability and uncertainty.

For State $i$ and capability $j$, define the normalized recognition component

$$r_{ij}=R_{ij}/4.$$

Let $\mathcal A_{ij}$ contain the available values among $Q_{ij},P_{ij},U_{ij},D_{ij}$. The latent capability estimator is

$$
 z_{ij}=\left(r_{ij}\prod_{x\in\mathcal A_{ij}}x\right)^{1/(1+|\mathcal A_{ij}|)}.
$$

All supplied latent components receive equal multiplicative weight. In strict mode, all four latent components are required.

Evidence confidence $C_{ij}$ is **not** multiplied into $z_{ij}$. Confidence measures epistemic reliability, not substantive sovereign capability. It is instead used as an observation weight in cross-sectional convergence statistics.

For each capability $j$, the confidence-weighted mean is

$$
\bar z_j^{(C)}=
\frac{\sum_i C_{ij}z_{ij}}{\sum_i C_{ij}},
$$

and weighted dispersion is

$$
\sigma_j^{(C)}=
\sqrt{\frac{\sum_i C_{ij}(z_{ij}-\bar z_j^{(C)})^2}{\sum_i C_{ij}}}.
$$

The global dispersion is

$$
\Sigma^{(C)}=
\sqrt{\frac1{12}\sum_{j=1}^{12}(\sigma_j^{(C)})^2},
$$

with the same normalized convergence mapping as v1,

$$
C^{(2)}=\max\left\{0,1-\frac{\Sigma^{(C)}}{0.5}\right\}.
$$

## Why confidence is separated

Multiplying a capability estimate by evidence confidence would cause an uncertain but potentially very capable State to receive a lower substantive score. That confuses epistemic uncertainty with capability. Version 2 therefore reports both the latent estimate and its confidence weight.

## Missing data

Missing values are never treated as zero. Non-strict mode computes a geometric mean over the supplied latent components and records the number of supplied components. Strict mode rejects incomplete latent observations.

## Interpretation

Version 2 is an evidence-adjusted estimator, not a causal estimator. It is intended to test the robustness of the v1 convergence result to richer measurement information. Subsequent versions should consider capability-specific weights, uncertainty intervals and inter-capability complementarity/dependency structure.
