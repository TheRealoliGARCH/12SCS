#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'results' / 'bayesian_rd_input_provenance_v1.csv'
REQUIRED = ['R', 'c', 'D', 'Y']
FIELDS = ['quantity','source_artifact','source_field','transformation','unit_of_observation','provenance_reference','validation_status']


def main():
    with PATH.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    assert [r['quantity'] for r in rows] == REQUIRED
    assert all(list(r.keys()) == FIELDS for r in rows)
    resolved = all(all(r[k] not in ('', 'UNRESOLVED') for k in FIELDS[1:]) and r['validation_status'] == 'VALIDATED' for r in rows)
    status = 'RD_INPUT_PROVENANCE_READY' if resolved else 'RD_INPUT_PROVENANCE_INCOMPLETE'
    print(f'PASS: Bayesian RD input provenance v1 evaluated: ready={resolved}.')
    print(f'status={status}')

if __name__ == '__main__':
    main()
