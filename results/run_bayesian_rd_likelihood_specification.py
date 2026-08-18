"""Machine-checkable local Bayesian sharp-RD likelihood specification.

This records the model contract only; it does not estimate parameters or fabricate data.
"""
from __future__ import annotations
import csv
from pathlib import Path

OUTPUT = Path("results/bayesian_rd_likelihood_specification_v1.csv")


def main() -> None:
    rows = [
        ("model_family", "Normal local regression", True),
        ("outcome", "Y_i", True),
        ("running_variable", "R_i", True),
        ("cutoff", "c", True),
        ("treatment", "D_i=1[R_i>=c]", True),
        ("local_window", "|R_i-c|<=h", True),
        ("conditional_mean", "alpha+tau*D_i+beta*(R_i-c)+gamma*D_i*(R_i-c)", True),
        ("noise", "Normal(0,sigma^2)", True),
        ("causal_estimand", "tau", True),
        ("posterior", "p(alpha,tau,beta,gamma,sigma|Y,R,D)", True),
        ("observed_data_required", "bayesian_rd_input_v1.csv", False),
        ("prior_hyperparameters_supplied", "required before estimation", False),
        ("bandwidth_supplied", "h required before estimation", False),
    ]
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        w=csv.writer(f)
        w.writerow(["component","formalization","specified"])
        w.writerows(rows)
    estimation_ready = all(ok for name, _, ok in rows if name in {"observed_data_required","prior_hyperparameters_supplied","bandwidth_supplied"})
    status = "RD_LIKELIHOOD_SPECIFIED_NOT_ESTIMATION_READY" if not estimation_ready else "RD_LIKELIHOOD_ESTIMATION_READY"
    print(OUTPUT)
    print("RD_LIKELIHOOD_STATUS=" + status)


if __name__ == "__main__":
    main()
