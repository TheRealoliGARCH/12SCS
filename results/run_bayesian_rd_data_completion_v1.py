"""Validate the empirical inputs required before Bayesian RD estimation."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "bayesian_rd_data_completion_v1.csv"
OUTPUT = ROOT / "bayesian_rd_data_completion_status_v1.csv"
REQUIRED = [
    "validated_rd_data", "running_variable", "cutoff", "treatment_rule",
    "outcome", "bandwidth_or_local_model", "continuity",
    "no_precise_manipulation", "local_support",
]

def parse_bool(value):
    if value not in {"True", "False"}:
        raise ValueError(f"expected True or False, got {value!r}")
    return value == "True"

def main():
    if not INPUT.exists():
        raise FileNotFoundError(INPUT)
    with INPUT.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    keys = {r.get("component") for r in rows}
    missing = [k for k in REQUIRED if k not in keys]
    if missing:
        raise AssertionError(f"missing required components: {missing}")
    status = {r["component"]: parse_bool(r["present"]) for r in rows if r["component"] in REQUIRED}
    ready = all(status[k] for k in REQUIRED)
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["component", "value"])
        w.writeheader()
        for key in REQUIRED:
            w.writerow({"component": key, "value": str(status[key])})
        w.writerow({"component": "estimation_ready", "value": str(ready)})
        w.writerow({"component": "status", "value": "RD_ESTIMATION_READY" if ready else "RD_ESTIMATION_NOT_READY"})
    print(f"PASS: Bayesian RD data completion v1 evaluated: ready={ready}.")

if __name__ == "__main__":
    main()
