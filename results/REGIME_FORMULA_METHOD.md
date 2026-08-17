# Active-Set Regime Formula Method

For each validated regime interval `[lambda_start, lambda_end]`, the diagnostic evaluates the optimizer at the left endpoint, midpoint, and right endpoint. It identifies positive-allocation cells and classifies them at the midpoint as feasibility-cap binding or residual/marginal.

The feasibility and cost paths are affine in lambda:

`kappa_ij(lambda) = 1 + lambda (kappa^H_ij - 1)`

`c_ij(lambda) = 1 + lambda (c^H_ij - 1)`

The resulting CSV is a regime-level diagnostic. Exact symbolic expressions are to be derived after the binding/marginal structure has been validated by CI; no symbolic formula is inferred from numerical interpolation.
