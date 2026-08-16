# 12SCCM v2 Reproduction Package

This directory defines the reproducible execution package for the evidence-adjusted Twelve-State Capability Convergence Model (v2).

## Objective

Three independent teams should be able to execute the same public computation from the same immutable Git commit and input data:

1. United States designated technical team;
2. Russian designated technical team;
3. independent international/scientific verification team.

The teams have equal evidentiary status. No team has authority to alter the specification or adjudicate a disagreement unilaterally.

## Current estimator

The production command is:

```text
python results/run_v2.py
```

The strict estimator requires all 144 State-capability cells and the five substantive fields represented by $R,Q,P,U,D$ (or documented aliases).

## Package contents

- `RUN_PROTOCOL.md` — exact execution sequence and security boundary.
- `INPUT_MANIFEST.csv` — canonical input-file list.
- `HASH_MANIFEST.py` — deterministic SHA-256 manifest generator.
- `VERIFY_RESULTS.py` — independent output-integrity and 144-cell checks.
- `TOLERANCE_PROTOCOL.md` — pre-registered comparison rules.

The completed team-specific record is `governance/EXECUTION_MANIFEST_TEMPLATE.md`.

## Integrity principle

A certified run is identified by:

$$
\mathcal K=(\text{commit},\text{inputs},\text{environment},\text{parameters}).
$$

Any change to $\mathcal K$ creates a new run identity.

The package follows standard reproducible-build principles: repeatable build steps, fresh execution environments and provenance records for generated artifacts.
