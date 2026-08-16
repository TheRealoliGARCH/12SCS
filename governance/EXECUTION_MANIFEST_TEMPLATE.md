# 12SCCM High-Assurance Execution Manifest

This manifest is completed separately by each execution team. It records the exact computational state used for a certified reproduction.

## Run identity

- Run ID:
- Date/time (UTC):
- Executing organization:
- Lead technical officer:
- Independent observer:

## Source specification

- Git repository: `TheRealoliGARCH/12SCS`
- Commit SHA:
- Branch/tag:
- Estimator version:
- Execution command:

## Input integrity

Record SHA-256 hashes for every input file used in the run.

| File | SHA-256 |
|---|---|
| | |

## Computational environment

- Operating system:
- Architecture:
- Python/interpreter version:
- Relevant package versions:
- Container/VM identifier, if applicable:

## Parameters

- Strict mode:
- Numerical tolerances:
- Any non-default parameters:

## Outputs

| Output | SHA-256 | Size | Status |
|---|---|---:|---|
| `capability_latent_matrix_v2.csv` | | | |
| `capability_distance_matrix_v2.csv` | | | |
| `capability_convergence_diagnostics_v2.csv` | | | |
| `capability_confidence_matrix_v2.csv` | | | |
| `capability_coverage_v2.csv` | | | |

## Verification

- Complete 144-cell coverage: YES / NO
- Strict estimator completed: YES / NO
- Internal validation tests passed: YES / NO
- Reproduced by independent team: YES / NO
- Maximum scalar discrepancy:
- Maximum matrix discrepancy:

## Discrepancies

Describe every discrepancy, however small, between this run and other certified runs.

## Certification statement

> I certify that this execution used the identified source commit, inputs, computational environment and parameters, and that the reported outputs are the direct outputs of the specified 12SCCM workflow.

Name:

Role:

Date:

Signature / cryptographic attestation:
