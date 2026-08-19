#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'results' / 'bayesian_rd_candidate_design_audit_v1.csv'

with PATH.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

allowed = {'REJECTED', 'INSUFFICIENT', 'CANDIDATE'}
for row in rows:
    assert row['classification'] in allowed
    if row['classification'] == 'CANDIDATE':
        assert all(row[k] != 'UNRESOLVED' for k in ('running_variable','cutoff','treatment','outcome'))
        assert row['independent_cutoff_justification'] == 'True'
        assert row['two_sided_local_support'] == 'True'
        assert row['non_circular'] == 'True'

n_candidate = sum(r['classification'] == 'CANDIDATE' for r in rows)
print(f'PASS: Bayesian RD candidate design audit v1 evaluated: candidates={n_candidate}.')
print('status=RD_CANDIDATE_AUDIT_COMPLETE')
