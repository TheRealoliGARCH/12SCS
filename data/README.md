# Data Acquisition Window

## Purpose

This directory begins the empirical handoff from the completed structural phases to Phase IV. Raw data acquired during the collection window should be preserved unchanged and registered in `data_acquisition_provenance_manifest_v1.csv`.

## Acquisition rule

For each dataset, create one manifest row at acquisition time. Record the source, acquisition timestamp in UTC, coverage, frequency, units, raw filename, SHA-256 checksum, dimensions, missingness status, and any transformation or access notes.

The raw file named in `raw_filename` should remain unchanged after its checksum is recorded.

## Status vocabulary

- `template_not_populated`: placeholder row only.
- `acquired`: raw file obtained and registered.
- `verified`: checksum and basic metadata verified.
- `frozen`: included in the end-of-window empirical snapshot.
- `pending`: reproducibility or verification work remains.
- `reproducible`: acquisition and verification information are sufficient to repeat the dataset capture, subject to source availability.

## End-of-window freeze

At the close of the acquisition window, the manifest should be audited for completeness, checksums, coverage, missingness, and provenance. The resulting inventory becomes the frozen empirical starting point for Phase IV.
