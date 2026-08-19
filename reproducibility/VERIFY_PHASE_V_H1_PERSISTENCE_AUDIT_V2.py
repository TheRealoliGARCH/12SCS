#!/usr/bin/env python3
import csv, hashlib, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'results' / 'phase_v_canonical_distance_matrix_v1.csv'
OUT = ROOT / 'results' / 'phase_v_h1_persistence_audit_v2.json'
BARS = ROOT / 'results' / 'phase_v_h1_persistence_bars_v2.csv'
d = json.loads(OUT.read_text())
required = {'status','source_matrix_path','source_matrix_sha256','n_points','n_simplices','n_h1_features','n_finite_h1_features','n_infinite_h1_features','max_persistence','total_h1_persistence'}
assert set(d) == required
assert d['status'] == 'H1_PERSISTENCE_COMPUTATION_COMPLETE'
assert d['source_matrix_path'] == 'results/phase_v_canonical_distance_matrix_v1.csv'
assert d['source_matrix_sha256'] == hashlib.sha256(SRC.read_bytes()).hexdigest()
assert d['n_points'] == 12
assert d['n_simplices'] == 2**12 - 1
assert d['n_h1_features'] == d['n_finite_h1_features'] + d['n_infinite_h1_features']
assert d['n_infinite_h1_features'] == 0
with BARS.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
assert len(rows) == d['n_h1_features']
finite = []
for r in rows:
    birth = float(r['birth']); death = float(r['death'])
    assert math.isfinite(birth) and math.isfinite(death)
    assert death >= birth
    persistence = float(r['persistence'])
    assert abs(persistence - (death - birth)) <= 1e-12
    finite.append(persistence)
assert d['n_finite_h1_features'] == len(finite)
assert abs(d['max_persistence'] - max(finite, default=0.0)) <= 1e-12
assert abs(d['total_h1_persistence'] - sum(finite)) <= 1e-12
print('PASS: Phase V H1 persistence computation v2 provenance and algebraic invariants verified.')
