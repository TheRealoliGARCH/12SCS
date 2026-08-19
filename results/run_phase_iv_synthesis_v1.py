#!/usr/bin/env python3
"""Build a deterministic, read-only Phase IV provenance synthesis manifest."""
from __future__ import annotations
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUT = RESULTS / "phase_iv_synthesis_v1.csv"
META = RESULTS / "phase_iv_synthesis_v1_metadata.csv"

SOURCES = [
    ("rd_data_contract", "bayesian_rd_data_contract_v1.csv", "inference_readiness"),
    ("rd_identification_design", "bayesian_rd_identification_design_v1.csv", "inference_readiness"),
    ("rd_likelihood", "bayesian_rd_likelihood_specification_v1.csv", "inference_readiness"),
    ("rd_prior", "bayesian_rd_prior_specification_v1.csv", "inference_readiness"),
    ("rd_bootstrap_summary", "bayesian_rd_summary_bootstrap_v1.csv", "empirical_summary"),
    ("rd_readiness_audit", "bayesian_rd_estimation_readiness_audit_v1.csv", "validated_structural"),
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    rows = []
    for domain, name, interpretation in SOURCES:
        path = RESULTS / name
        if not path.exists():
            raise FileNotFoundError(path)
        with path.open(newline="", encoding="utf-8") as handle:
            source_rows = list(csv.DictReader(handle))
        rows.append({
            "domain": domain,
            "metric": "source_row_count",
            "value": str(len(source_rows)),
            "source_artifact": f"results/{name}",
            "interpretation": interpretation,
        })

    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["domain", "metric", "value", "source_artifact", "interpretation"])
        writer.writeheader(); writer.writerows(rows)

    metadata = [
        {"key": "synthesis_version", "value": "v1"},
        {"key": "source_count", "value": str(len(SOURCES))},
    ]
    for domain, name, _ in SOURCES:
        metadata.append({"key": f"sha256:{domain}", "value": digest(RESULTS / name)})
    with META.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["key", "value"])
        writer.writeheader(); writer.writerows(metadata)

    print(f"PASS: Phase IV synthesis v1 generated from {len(SOURCES)} source artifacts.")

if __name__ == "__main__":
    main()
