"""Audit whether the current Bayesian structural counterfactual is data-identified."""
from __future__ import annotations
import csv
from pathlib import Path

OUTPUT = Path("results/bayesian_structural_identification_audit_v1.csv")


def main() -> None:
    # The current pipeline supplies a deterministic structural map and priors,
    # but no observed-outcome likelihood or data-backed identification design.
    structural_map_present = Path("results/bayesian_structural_counterfactual_cells_v1.csv").exists()
    prior_specification_present = True
    observed_outcome_data_present = False
    likelihood_present = False
    intervention_identification_strategy_present = False

    data_identified = (
        observed_outcome_data_present
        and likelihood_present
        and intervention_identification_strategy_present
    )
    status = "IDENTIFIED" if data_identified else "NOT_IDENTIFIED_FROM_DATA"

    fields = [
        "structural_map_present",
        "prior_specification_present",
        "observed_outcome_data_present",
        "likelihood_present",
        "intervention_identification_strategy_present",
        "data_identified",
        "status",
    ]
    row = [
        structural_map_present,
        prior_specification_present,
        observed_outcome_data_present,
        likelihood_present,
        intervention_identification_strategy_present,
        data_identified,
        status,
    ]
    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(fields)
        w.writerow(row)
    print(OUTPUT)
    print("CAUSAL_EFFECT_IDENTIFIED=" + str(data_identified))
    print("IDENTIFICATION_STATUS=" + status)


if __name__ == "__main__":
    main()
