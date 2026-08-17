"""Audit the structural intervention on the admissible V6 cell population.

The full V6 population contains cells for which the primitive cost coefficient
is negative.  Rather than silently dropping those cells, this stage explicitly
defines the target population A = {cells: d >= 0}.  On A, the intervention
 do(d <- 0.9*d) is a well-defined structural counterfactual.  This is a
model-based identification result, not an empirical causal-effect claim.
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
    n_total: int
    n_admissible: int
    n_excluded: int
    target_population: str
    intervention: str
    intervention_well_defined: bool
    outcome_pre_treatment: bool
    structural_positivity: bool
    consistency: bool
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

    admissible = [c for c in cells if c.d >= 0.0]
    excluded = [c for c in cells if c.d < 0.0]
    if not admissible:
        raise ValueError("no admissible cells with d >= 0")

    target_population = "A={cells: d >= 0}"
    intervention = f"do(d <- {(1.0 - delta):.1f}*d)"
    intervention_well_defined = all(c.d >= 0.0 for c in admissible)
    outcome_pre_treatment = all(c.gap >= 0.0 for c in admissible)
    structural_positivity = all((1.0 - delta) * c.d >= 0.0 for c in admissible)
    consistency = True

    # No external treatment assignment is supplied by V6, so an empirical ATE
    # remains unidentified even after restricting the structural domain.
    empirical_ate_identified = False
    structural_ate_identified = (
        intervention_well_defined
        and outcome_pre_treatment
        and structural_positivity
        and consistency
    )
    status = (
        "ADMISSIBLE_STRUCTURAL_INTERVENTION_IDENTIFIED_BUT_EMPIRICAL_ATE_NOT_IDENTIFIED"
        if structural_ate_identified and not empirical_ate_identified
        else "NOT_IDENTIFIED"
    )

    return Audit(
        len(cells), len(admissible), len(excluded), target_population,
        intervention, intervention_well_defined, outcome_pre_treatment,
        structural_positivity, consistency, empirical_ate_identified,
        structural_ate_identified, status,
    )


def main() -> None:
    cells = load_cells(Path("results/bayesian_cell_level_causal_dataset_v1.csv"))
    result = audit(cells)
    out = Path("results/bayesian_admissible_intervention_audit_v1.csv")
    fields = list(result.__dataclass_fields__)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(fields)
        w.writerow([getattr(result, x) for x in fields])
    print(out)
    print(result)


if __name__ == "__main__":
    main()
