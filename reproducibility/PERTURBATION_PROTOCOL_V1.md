# Phase IV Perturbation Sensitivity Protocol v1

## Status

This is an exploratory robustness protocol. It formalizes a confidence-informed perturbation rule; it does not claim that the confidence matrix is a calibrated probabilistic posterior.

## Inputs

- `results/capability_latent_matrix_v2.csv`
- `results/capability_confidence_matrix_v2.csv`

Both matrices must have identical State and capability ordering.

## Perturbation rule

For latent score $x_{ij}$ and confidence $c_{ij}$:

$$
\Delta_{ij} \sim \operatorname{Uniform}(-s(1-c_{ij}), +s(1-c_{ij}))
$$

with baseline scale $s=0.10$. The perturbed value is clipped to $[0,1]$.

## Determinism

Use:

- seed: `12000`
- scenarios: `5000`
- Python standard-library pseudorandom generator

## Statistics

For every scenario compute:

1. the closest State pair by Euclidean distance;
2. the most central State by mean distance to the other eleven States;
3. the most peripheral State by mean distance to the other eleven States.

Ties are resolved deterministically by matrix order.

## Outputs

- `results/perturbation_sensitivity_v1.csv`
- `results/perturbation_sensitivity_v1_metadata.csv`

## Execution

```text
python results/run_perturbation_sensitivity_v1.py
```

A certified rerun must record the repository commit and preserve both output files.
