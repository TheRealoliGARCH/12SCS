# v2 Execution Protocol

## 1. Freeze the source

Record the exact Git commit SHA before execution. Do not execute from a moving branch name alone.

## 2. Verify inputs

Run:

```text
python reproducibility/HASH_MANIFEST.py
```

Compare the resulting hashes with the independently agreed input manifest before execution.

## 3. Fresh environment

Use a fresh, isolated environment with Python 3.x and no unrecorded local modifications. The v2 estimator uses only the Python standard library.

## 4. Execute

From the repository root:

```text
python results/run_v2.py
```

Strict mode is mandatory for a certified run.

## 5. Verify outputs

Run:

```text
python reproducibility/VERIFY_RESULTS.py
```

The verifier must confirm all twelve States, all twelve capabilities and all 144 cells, and validate matrix dimensions and diagonal distances.

## 6. Hash outputs

Run the hash manifest again and record output hashes in the team execution manifest.

## 7. Preserve the environment record

Record OS, architecture, Python version, repository commit, command, UTC timestamp and any relevant interpreter/build information.

## 8. Compare independent executions

For teams $a,b$ compare the scalar diagnostics and matrices using the tolerances in `TOLERANCE_PROTOCOL.md`.

If a comparison fails:

$$
\text{fail}
\rightarrow
\text{diagnose}
\rightarrow
\text{document}
\rightarrow
\text{rerun}.
$$

Do not average incompatible outputs.

## 9. Security boundary

This package operates only on the public 12SCCM source code and public empirical datasets. No classified nuclear information, operational plans, targeting data or sensitive vulnerabilities are required or requested.
