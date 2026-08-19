#!/usr/bin/env python3
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
decl = ROOT / 'results' / 'phase_v_canonical_distance_source_v1.csv'
out = ROOT / 'results' / 'phase_v_canonical_distance_reconstruction_v1.json'
with decl.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 1
r = rows[0]
assert r['expected_n_states'] == '12'
assert r['expected_n_capabilities'] == '12'
assert r['status'] in {'CANONICAL_SOURCE_UNRESOLVED','CANONICAL_SOURCE_VALIDATED'}
d = json.loads(out.read_text())
assert d['status'] == r['status']
if d['status'] == 'CANONICAL_SOURCE_UNRESOLVED':
    assert d['n_states'] == 0
    assert d['source_sha256'] == '' and d['matrix_sha256'] == ''
print('PASS: Phase V canonical distance reconstruction v1 declaration and non-fabrication invariants verified.')
