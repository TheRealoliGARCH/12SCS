"""Machine-checkable Bayesian regression-discontinuity identification design."""
from __future__ import annotations
import csv
from pathlib import Path

OUTPUT = Path("results/bayesian_rd_identification_design_v1.csv")


def main() -> None:
    rows = [
        ("design", "regression_discontinuity", True, "Regression-discontinuity identification route selected."),
        ("running_variable", "R", False, "Running variable must be supplied with observed units."),
        ("cutoff", "c", False, "Known treatment-assignment threshold must be specified before analysis."),
        ("treatment_rule", "D=1[R>=c]", False, "Sharp assignment rule must be verified from the institutional design."),
        ("outcome", "Y", False, "Observed outcome variable must be supplied."),
        ("local_likelihood", "p(Y|R,theta)", False, "Likelihood for observations near the cutoff must be specified."),
        ("continuity", "potential outcomes continuous at c", False, "RD continuity assumption must be explicitly adopted and defended."),
        ("no_precise_manipulation", "density/support diagnostic", False, "Running-variable manipulation must be assessed around the cutoff."),
        ("local_support", "both sides of c", False, "Sufficient observations must exist on both sides of the cutoff."),
        ("bandwidth_or_local_model", "h or local specification", False, "Local window or Bayesian local-function specification must be pre-specified."),
    ]
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["component", "formalization", "present", "description"])
        w.writerows(rows)
    required = {r[0] for r in rows if r[0] != "design"}
    present = {name for name, _, ok, _ in rows if ok}
    status = "RD_IDENTIFICATION_DESIGN_INCOMPLETE" if not required.issubset(present) else "RD_IDENTIFICATION_DESIGN_COMPLETE"
    print(OUTPUT)
    print("RD_IDENTIFICATION_DESIGN_STATUS=" + status)


if __name__ == "__main__":
    main()
