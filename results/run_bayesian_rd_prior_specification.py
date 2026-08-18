"""Machine-checkable proper-prior specification for local Bayesian sharp RD."""
from __future__ import annotations
import csv
import math
from pathlib import Path

OUTPUT = Path("results/bayesian_rd_prior_specification_v1.csv")
PRIORS = {
    "alpha": ("Normal", 0.0, 10.0),
    "tau": ("Normal", 0.0, 10.0),
    "beta": ("Normal", 0.0, 10.0),
    "gamma": ("Normal", 0.0, 10.0),
    "sigma": ("HalfNormal", 0.0, 10.0),
}


def main() -> None:
    rows = []
    for parameter, (family, location, scale) in PRIORS.items():
        if not math.isfinite(location):
            raise ValueError(f"{parameter} location must be finite")
        if not math.isfinite(scale) or scale <= 0.0:
            raise ValueError(f"{parameter} scale must be finite and positive")
        rows.append((parameter, family, location, scale, True))
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["parameter", "family", "location", "scale", "proper"])
        w.writerows(rows)
    print(OUTPUT)
    print("RD_PRIOR_STATUS=RD_PRIORS_SPECIFIED")


if __name__ == "__main__":
    main()
