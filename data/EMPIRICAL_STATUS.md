# Empirical 12SCCM Matrix Status

## Current repository state

The repository currently contains scored dimension-specific datasets for capabilities:

$$
N,M,E,T,I,H,L,D,A,S.
$$

The financial/monetary dimension $F$ and energy/resource-security dimension $R$ do not currently have corresponding dimension-specific CSV datasets in `data/`. They therefore remain missing from the executable empirical matrix.

The master recognition ledger also contains the initial $N$ observations, while unpopulated cells remain blank. The implementation must not infer missing observations from prose descriptions or from earlier provisional tables.

## Consequence

The empirical object currently available to the software is **not yet a complete $12\times12$ matrix**. In particular, a full-vector convergence distance cannot be reported for any State until all twelve dimensions have observations for that State.

This is intentional. The model follows:

$$
\mathrm{missing}\neq0,
$$

and does not perform silent imputation.

## Current next-stage procedure

1. Consolidate all dimension-specific datasets into a normalized matrix.
2. Verify that each State--capability pair occurs at most once.
3. Normalize $R\in\{0,1,2,3,4\}$ to $r=R/4\in[0,1]$.
4. Retain evidence confidence separately from capability magnitude.
5. Calculate dimension-wise dispersion using available observations.
6. Calculate full State-vector distances only for complete vectors.
7. Calculate corridor gaps against an explicitly declared target vector and tolerance vector.
8. Add $F$ and $R$ datasets before publishing a twelve-dimensional convergence statistic.

## Anti-circularity rule

The convergence analysis must not be used to revise the underlying recognition scores. Measurement precedes convergence analysis; convergence analysis is downstream of the evidence ledger.

## Empirical maturity levels

- **Level 0:** schema only.
- **Level 1:** evidence-backed dimension observations.
- **Level 2:** complete 12-dimensional State vectors.
- **Level 3:** validated convergence and dispersion statistics.
- **Level 4:** dependency, substitutability and complementarity tensors.
- **Level 5:** systemic stability and stress-testing.
