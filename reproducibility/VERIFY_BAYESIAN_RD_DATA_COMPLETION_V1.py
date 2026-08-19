import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
SCRIPT = RESULTS / "run_bayesian_rd_data_completion_v1.py"
OUTPUT = RESULTS / "bayesian_rd_data_completion_status_v1.csv"

subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)
with OUTPUT.open(newline="", encoding="utf-8") as f:
    rows = {r["component"]: r["value"] for r in csv.DictReader(f)}
assert rows["status"] == "RD_ESTIMATION_NOT_READY"
assert rows["estimation_ready"] == "False"
print("PASS: Bayesian RD data completion v1 contract and readiness gate verified.")
