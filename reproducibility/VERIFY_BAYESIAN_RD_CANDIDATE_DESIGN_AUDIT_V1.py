#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'results' / 'bayesian_rd_candidate_design_audit_v1.csv'
required = {'candidate_id','running_variable','cutoff','treatment','outcome','independent_cutoff_justification','two_sided_local_support','non_circular','classification','reason'}
allowed = {'REJECTED','INSUFFICIENT','CANDIDATE'}

with PATH.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

assert rows
assert set(rows[0]) == required
for row in rows:
    assert row['classification'] in allowed
    if row['classification'] == 'CANDIDATE':
        assert all(row[k] != 'UNRESOLVED' for k in ('running_variable','cutoff','treatment','outcome'))
        assert row['independent_cutoff_justification'] == 'True'
        assert row['two_sided_local_support'] == 'True'
        assert row['non_circular'] == 'True'

print('PASS: Bayesian RD candidate design audit v1 schema and classification invariants verified.')
