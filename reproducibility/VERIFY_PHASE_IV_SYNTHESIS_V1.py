#!/usr/bin/env python3
"""Verify Phase IV synthesis v1 structure, provenance and determinism."""
from __future__ import annotations
import csv
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUT = RESULTS / "phase_iv_synthesis_v1.csv"
META = RESULTS / "phase_iv_synthesis_v1_metadata.csv"
REQUIRED = {"domain", "metric", "value", "source_artifact", "interpretation"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    subprocess.run([sys.executable, "results/run_phase_iv_synthesis_v1.py"], cwd=ROOT, check=True)
    before = (sha(OUT), sha(META))
    subprocess.run([sys.executable, "results/run_phase_iv_synthesis_v1.py"], cwd=ROOT, check=True)
    assert before == (sha(OUT), sha(META)), "synthesis is not deterministic"

    with OUT.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows and set(rows[0]) == REQUIRED
    for row in rows:
        source = ROOT / row["source_artifact"]
        assert source.exists(), source
        int(row["value"])
        assert row["interpretation"] in {"inference_readiness", "empirical_summary", "validated_structural"}

    with META.open(newline="", encoding="utf-8") as handle:
        metadata = {r["key"]: r["value"] for r in csv.DictReader(handle)}
    assert metadata["synthesis_version"] == "v1"
    assert int(metadata["source_count"]) == len(rows)
    for row in rows:
        domain = row["domain"]
        assert metadata[f"sha256:{domain}"] == sha(ROOT / row["source_artifact"])

    print("PASS: Phase IV synthesis v1 provenance and determinism verified.")

if __name__ == "__main__":
    main()
