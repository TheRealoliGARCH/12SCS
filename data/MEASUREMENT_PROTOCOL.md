# 12SCCM Empirical Measurement Protocol

## Purpose

This protocol governs construction of the 144-cell Twelve-State Capability Recognition Matrix. It is designed to prevent intuitive country ranking from entering the model before observable evidence has been defined and recorded.

## Unit of observation

Each observation is a State--capability pair `(state_id, capability_id)` at a specified date.

There are 12 States, 12 capability dimensions, and therefore 144 primary observations per measurement date.

## Recognition variables

For each cell, record:

- `R`: Charter recognition level, integer 0--4.
- `Q`: quality of demonstrated capability, normalized to [0,1].
- `P`: persistence, normalized to [0,1].
- `U`: strategic uniqueness, normalized to [0,1].
- `D`: demonstrated capability/evidence aggregation, normalized to [0,1].
- `evidence_confidence`: confidence in the evidence record, normalized to [0,1].
- `source`: provenance of the evidence.
- `date`: observation/reference date.
- `notes`: methodological qualification.

The latent recognition intensity is:

$$
rho_{ij}=Q_{ij}P_{ij}U_{ij}D_{ij}.
$$

Recognition level is then assigned by the calibrated capability-specific thresholds in the model implementation.

## Evidence hierarchy

Evidence should be collected in the following order of preference:

1. Official State disclosures and primary government publications.
2. Treaty bodies, international organizations, and intergovernmental statistical systems.
3. Independent audited or regulated institutional sources.
4. High-quality academic or specialist research with transparent methodology.
5. Reputable secondary reporting used to corroborate, not replace, primary evidence.
6. Analytical inference, explicitly labelled as inference and never represented as sovereign disclosure.

For consequential or disputed observations, use multiple independent evidence streams where feasible.

## Evidence independence

Multiple documents derived from the same underlying dataset, official statement, or reporting chain are not independent observations. Correlated sources must not be multiplied mechanically in the demonstrated-capability aggregator.

## Unknown is not negligible

A missing or insufficiently verified observation remains blank/NA. It must not be converted automatically to `R=0`.

## Capability-specific measurement

The 12 dimensions require different indicator families. GDP, military expenditure, patent counts, diplomatic missions, or any other single indicator must not be treated as the capability itself. Indicators are evidence for the latent capability construct.

## Nuclear dimension

For Nuclear and Strategic Deterrence, distinguish explicitly between:

- nuclear-weapons capability;
- peaceful nuclear capability;
- legitimate nuclear-system participation;
- nuclear safety and security;
- systemic nuclear risk.

Public uncertainty must be retained. The model contains no nuclear-weapons transfer or construction mechanism.

## Temporal rule

Every substantive observation must have a reference date or date range. Persistent capability should be distinguished from a temporary event or historical capability.

## Scoring rule

Do not assign a recognition level merely because a State is generally regarded as powerful. A recognition level must be traceable to the dimension-specific measurement definition and evidence record.

## Review rule

Before publication of a completed matrix, inspect every non-zero and every Level-4 observation for:

- source provenance;
- date validity;
- evidence independence;
- measurement relevance;
- persistence;
- uniqueness/substitutability;
- uncertainty;
- consistency with the Charter.

## Versioning

The recognition matrix is a dated measurement product. Subsequent evidence may change `Q`, `P`, `U`, `D`, confidence, or `R`. Historical versions should remain reproducible rather than being silently overwritten.
