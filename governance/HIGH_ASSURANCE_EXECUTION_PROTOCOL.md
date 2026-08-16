# High-Assurance Execution and Reproducibility Protocol

## Principle

The Twelve-State Capability System is a sovereign measurement system. No State owns the computational result. The result is accepted only when independently reproducible from the same immutable specification and inputs.

> **Many Nations, One Team.**

The governing principle is:

$$
\text{Reproducibility} > \text{Authority}.
$$

## 1. Independent execution

For a designated high-assurance run, at least three independent execution teams should reproduce the computation:

1. a United States-designated technical team;
2. a Russian-designated technical team;
3. an independent international/scientific verification team mutually acceptable to the participating States.

The designation of the first two teams follows from their exceptional systemic responsibility in the nuclear domain. It does not confer authority over the mathematical specification or the result.

## 2. Common computational input

Every execution must identify exactly:

- Git commit SHA;
- input-file SHA-256 digests;
- operating-system/environment specification;
- interpreter/compiler version;
- dependency versions;
- command and parameters;
- execution timestamp;
- generated-output SHA-256 digests.

No executor may silently substitute a local version of an input file.

## 3. Immutable specification

The following are fixed for a certified run:

$$
\mathcal K=(\text{code},\text{data},\text{parameters},\text{environment}).
$$

A change to any element of $\mathcal K$ creates a new run identifier and requires a new verification cycle.

## 4. Determinism

The v2 estimator is deterministic. Random seeds therefore do not enter the current calculation. If a later estimator introduces stochastic procedures, the seed and stochastic configuration must become part of $\mathcal K$.

## 5. Reproduction tolerances

For scalar outputs $y$ produced by two executions $a$ and $b$, define:

$$
\Delta(y_a,y_b)=|y_a-y_b|.
$$

For matrices $X_a,X_b$ use:

$$
\Delta_\infty(X_a,X_b)=\max_{ij}|X_{a,ij}-X_{b,ij}|.
$$

A certified run requires all differences to be within pre-registered numerical tolerances. Exact equality is preferred for deterministic CSV outputs; a numerical tolerance is permitted only where the computing environment produces justified floating-point differences.

## 6. No averaging of disagreements

If independent executions disagree beyond tolerance, their results must not be averaged to manufacture consensus.

Instead:

$$
\text{disagreement}
\rightarrow
\text{diagnosis}
\rightarrow
\text{correction or documented explanation}
\rightarrow
\text{rerun}.
$$

## 7. Evidence is separate from execution

Computational reproducibility does not validate the substantive truth of an input observation. The evidence ledger remains the authoritative provenance layer for capability observations.

Thus:

$$
\text{reproducible computation}
\not\Rightarrow
\text{correct empirical premise}.
$$

Independent evidence review remains necessary.

## 8. Publication package

A certified run should publish, subject to applicable security and legal restrictions:

- source commit;
- input data;
- evidence ledgers;
- execution manifest;
- environment specification;
- generated matrices;
- scalar diagnostics;
- verification certificates;
- discrepancies and their resolution.

## 9. Security boundary

The protocol concerns reproducibility of the **public 12SCCM computation**. It does not require disclosure of classified nuclear information, weapons designs, operational plans, vulnerabilities, targeting information, or other sensitive national-security material.

No classified nuclear information is an implicit prerequisite for reproducing the public mathematical estimator.

## 10. Governance principle

The exceptional capabilities of a State increase its responsibility for verification but do not increase its authority over the result:

$$
\boxed{
\text{Greater catastrophic capability}
\Rightarrow
\text{greater verification duty}.
}
$$

The final certified result belongs to the common system, not to any individual State.
