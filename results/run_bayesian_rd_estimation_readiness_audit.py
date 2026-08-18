"""Audit whether the Bayesian sharp-RD stack is ready for estimation."""
from __future__ import annotations

import csv
from pathlib import Path

DATA = Path("results/bayesian_rd_data_contract_v1.csv")
LIKELIHOOD = Path("results/bayesian_rd_likelihood_specification_v1.csv")
PRIORS = Path("results/bayesian_rd_prior_specification_v1.csv")
OUTPUT = Path("results/bayesian_rd_estimation_readiness_audit_v1.csv")


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise FileNotFoundError(path)
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    if not rows:
        raise ValueError(f"empty artifact: {path}")
    return rows[0]


def main() -> None:
    data = read_one(DATA)
    likelihood_rows = list(csv.DictReader(LIKELIHOOD.open(encoding="utf-8")))
    prior_rows = list(csv.DictReader(PRIORS.open(encoding="utf-8")))
    likelihood = {r["component"]: r["specified"] for r in likelihood_rows}
    priors = {r["parameter"]: r for r in prior_rows}

    data_valid = data["status"] == "RD_DATA_CONTRACT_VALID"
    likelihood_specified = all(
        likelihood.get(k) == "True"
        for k in ("model_family","outcome","running_variable","cutoff","treatment","local_window","conditional_mean","noise","causal_estimand","posterior")
    )
    priors_specified = set(priors) == {"alpha","tau","beta","gamma","sigma"} and all(
        r["proper"] == "True" for r in priors.values()
    )
    bandwidth_supplied = likelihood.get("bandwidth_supplied") == "True"
    estimation_ready = data_valid and likelihood_specified and priors_specified and bandwidth_supplied
    status = "RD_ESTIMATION_READY" if estimation_ready else "RD_ESTIMATION_NOT_READY"

    rows = [
        ("validated_rd_data", data_valid),
        ("likelihood_specified", likelihood_specified),
        ("proper_priors_specified", priors_specified),
        ("bandwidth_supplied", bandwidth_supplied),
        ("estimation_ready", estimation_ready),
        ("status", status),
    ]
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["component", "value"])
        w.writerows(rows)
    print(OUTPUT)
    print("RD_ESTIMATION_READINESS_STATUS=" + status)


if __name__ == "__main__":
    main()
