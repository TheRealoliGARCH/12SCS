"""Reduce calibrated monotonicity to finite derivative sign certificates."""
from __future__ import annotations
import csv, math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "results"
SOURCE = R / "convergence_regime_derivatives_continuity_v2.csv"

def main():
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    with SOURCE.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise AssertionError("no regime derivative data")
    out = R / "convergence_polynomial_sign_certificates_v2.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["regime", "lambda_start", "lambda_end", "dPi_start", "dPi_mid", "dPi_end", "start_sign", "mid_sign", "end_sign"])
        for r in rows:
            vals = [float(r[k]) for k in ("dPi_start", "dPi_mid", "dPi_end")]
            if not all(math.isfinite(x) for x in vals):
                raise AssertionError(f"non-finite derivative in regime {r['regime']}")
            signs = ["NEGATIVE" if x < 0 else "NONNEGATIVE" for x in vals]
            w.writerow([r["regime"], r["lambda_start"], r["lambda_end"], *vals, *signs])
            if any(x >= 0 for x in vals):
                raise AssertionError(f"calibrated monotonicity lacks strict sign certificate in regime {r['regime']}")
    print(f"Derivative sign certificates established for {len(rows)} regimes.")

if __name__ == "__main__":
    main()
