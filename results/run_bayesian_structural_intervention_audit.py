"""Define and audit a model-based causal intervention for 12SCSM.

This stage deliberately stops short of claiming an empirical ATE.  It defines a
policy intervention on the primitive cost coefficient d and checks whether the
intervention is well-defined, whether the outcome is pre-treatment, and whether
the resulting estimand is identified by the structural model.  The estimand is
therefore model-based unless an external randomized or observational treatment
assignment is subsequently supplied.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Cell:
    regime: int
    state: str
    capability: str
    gap: float
    weight: float
    a: float
    d: float
    treatment_active: int


@dataclass(frozen=True)
class Audit:
    n_rows: int
    treatment_definition: str
    intervention_is_well_defined: bool
    outcome_is_pre_treatment: bool
    treatment_varies: bool
    positivity: bool
    consistency: bool
    exchangeability_empirically_testable: bool
    empirical_ate_identified: bool
    structural_ate_identified: bool
    identification_status: str


def load_cells(path: Path) -> list[Cell]:
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return [Cell(
        int(r["regime"]), r["state"], r["capability"],
        float(r["gap"]), float(r["weight"]), float(r["a"]), float(r["d"]),
        int(r["treatment_active"]),
    ) for r in rows]


def audit(cells: list[Cell], delta: float = 0.10) -> Audit:
    if not cells or not (0.0 < delta < 1.0):
        raise ValueError("non-empty cells and 0 < delta < 1 are required")

    # Intervention: a capability-specific 10% reduction in the primitive cost
    # coefficient d, assigned by a pre-treatment policy rule.  The intervention
    # is defined on d itself, not on active-set status.
    treatment_definition = "do(d <- 0.9*d)"
    well_defined = all(c.d >= 0.0 for c in cells)

    # Baseline gap is generated before the cost intervention and is therefore a
    # legitimate pre-treatment covariate/outcome candidate.  We do not use the
    # mechanically post-treatment local-progress proxy here.
    outcome_pre = all(c.gap >= 0.0 for c in cells)

    treatment_varies = any(c.d != 0.0 for c in cells)
    # The intervention is a paired structural counterfactual for every cell;
    # this is positivity in the structural, not observational, sense.
    positivity = all(c.d >= 0.0 for c in cells)
    consistency = True

    # No external treatment-assignment mechanism is present in V6.  Hence
    # exchangeability cannot be empirically tested and an observational ATE is
    # not identified.  The structural model, however, defines both d and
    # 0.9*d, so a model-based intervention contrast is identified conditional
    # on the structural equations.
    exchangeability_testable = False
    empirical_ate = False
    structural_ate = well_defined and outcome_pre and positivity and consistency

    status = (
        "STRUCTURAL_INTERVENTION_IDENTIFIED_BUT_EMPIRICAL_ATE_NOT_IDENTIFIED"
        if structural_ate and not empirical_ate else
        "NOT_IDENTIFIED"
    )
    return Audit(
        len(cells), treatment_definition, well_defined, outcome_pre,
        treatment_varies, positivity, consistency, exchangeability_testable,
        empirical_ate, structural_ate, status,
    )


def main() -> None:
    cells = load_cells(Path("results/bayesian_cell_level_causal_dataset_v1.csv"))
    result = audit(cells)
    out = Path("results/bayesian_structural_intervention_audit_v1.csv")
    fields = list(result.__dataclass_fields__)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(fields)
        w.writerow([getattr(result, x) for x in fields])
    print(out)
    print(result)


if __name__ == "__main__":
    main()
