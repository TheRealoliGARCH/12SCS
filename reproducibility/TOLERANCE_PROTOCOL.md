# v2 Reproducibility Tolerance Protocol

## Deterministic expectation

The v2 estimator is deterministic and uses the Python standard library. Independent executions using identical inputs and a compatible Python implementation should therefore agree to floating-point precision.

## Pre-registered tolerances

For a scalar diagnostic $y$:

$$
\Delta_s=|y_a-y_b|.
$$

For a matrix $X$:

$$
\Delta_\infty=\max_{ij}|X_{a,ij}-X_{b,ij}|.
$$

The initial acceptance thresholds are:

- scalar diagnostics: $\Delta_s\le 10^{-12}$;
- latent capability matrix: $\Delta_\infty\le 10^{-12}$;
- distance matrix: $\Delta_\infty\le 10^{-12}$;
- confidence and coverage matrices: exact equality expected.

These are reproducibility thresholds, not statistical uncertainty intervals.

## Failure rule

If any threshold is exceeded, the result is not certified. The teams must identify whether the cause is:

1. different commit;
2. different input hash;
3. different interpreter/runtime;
4. different parameters;
5. floating-point implementation;
6. software defect;
7. unexplained discrepancy.

No averaging is permitted to conceal disagreement.

## Consensus rule

For three executions $a,b,c$:

$$
\max_{k,\ell\in\{a,b,c\}}\Delta_s(y_k,y_\ell)\le 10^{-12}
$$

and the corresponding matrix criteria must both hold.

Only then may the result be labelled **reproducibly verified**.
