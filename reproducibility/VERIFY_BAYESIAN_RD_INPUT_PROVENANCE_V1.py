#!/usr/bin/env python3
import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'results' / 'bayesian_rd_input_provenance_v1.csv'
RUNNER = ROOT / 'results' / 'run_bayesian_rd_input_provenance_v1.py'
REQUIRED = ['R', 'c', 'D', 'Y']
FIELDS = ['quantity','source_artifact','source_field','transformation','unit_of_observation','provenance_reference','validation_status']

def main():
    with MANIFEST.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    assert [r['quantity'] for r in rows] == REQUIRED
    assert list(rows[0].keys()) == FIELDS
    for r in rows:
        assert all(k in r for k in FIELDS)
        if r['validation_status'] == 'VALIDATED':
            assert all(r[k] not in ('', 'UNRESOLVED') for k in FIELDS[1:])
    out = subprocess.check_output([sys.executable, str(RUNNER)], text=True)
    assert 'PASS: Bayesian RD input provenance v1 evaluated:' in out
    print('PASS: Bayesian RD input provenance v1 contract and unresolved-state invariants verified.')

if __name__ == '__main__':
    main()
