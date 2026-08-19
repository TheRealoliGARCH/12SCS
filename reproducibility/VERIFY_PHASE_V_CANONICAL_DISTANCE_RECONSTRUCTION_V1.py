#!/usr/bin/env python3
import csv, hashlib, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
decl = ROOT / 'results' / 'phase_v_canonical_distance_source_v1.csv'
out = ROOT / 'results' / 'phase_v_canonical_distance_reconstruction_v1.json'
with decl.open(newline='', encoding='utf-8') as f: rows = list(csv.DictReader(f))
assert len(rows) == 1
r = rows[0]
assert r['expected_n_states'] == '12' and r['expected_n_capabilities'] == '12'
assert r['status'] in {'CANONICAL_SOURCE_UNRESOLVED','CANONICAL_SOURCE_VALIDATED'}
d = json.loads(out.read_text())
if r['status'] == 'CANONICAL_SOURCE_UNRESOLVED':
    assert d['status'] == 'CANONICAL_SOURCE_UNRESOLVED' and d['n_states'] == 0
    assert d['source_sha256'] == '' and d['matrix_sha256'] == ''
else:
    matrix = ROOT / 'results' / 'phase_v_canonical_distance_matrix_v1.csv'
    assert d['status'] == 'CANONICAL_DISTANCE_RECONSTRUCTION_COMPLETE'
    assert d['n_states'] == 12 and d['n_capabilities'] == 12
    assert len(d['source_sha256']) == 64 and hashlib.sha256(matrix.read_bytes()).hexdigest() == d['matrix_sha256']
    with matrix.open(newline='', encoding='utf-8') as f: rows = list(csv.reader(f))
    assert len(rows) == 13 and all(len(x) == 13 for x in rows)
    vals = [[float(x) for x in row[1:]] for row in rows[1:]]
    for i in range(12):
        assert vals[i][i] == 0.0
        for j in range(12):
            assert vals[i][j] >= 0.0 and math.isclose(vals[i][j], vals[j][i], abs_tol=1e-12)
print('PASS: Phase V canonical distance reconstruction v1 provenance and metric invariants verified.')
