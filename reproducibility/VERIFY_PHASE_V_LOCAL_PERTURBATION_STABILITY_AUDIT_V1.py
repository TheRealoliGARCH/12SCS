#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results' / 'phase_v_local_perturbation_stability_v1.json'
SRC = ROOT / 'results' / 'capability_latent_matrix_v2.csv'
BARS = ROOT / 'results' / 'phase_v_h1_persistence_bars_v2.csv'
d = json.loads(OUT.read_text())
assert d['status'] == 'LOCAL_PERTURBATION_STABILITY_AUDIT_COMPLETE'
assert d['source_latent_matrix_path'] == 'results/capability_latent_matrix_v2.csv'
assert d['source_latent_matrix_sha256'] == hashlib.sha256(SRC.read_bytes()).hexdigest()
assert d['baseline_bars_sha256'] == hashlib.sha256(BARS.read_bytes()).hexdigest()
assert d['perturbation_levels'] == [0.01, 0.02, 0.05]
assert len(d['results']) == 3
for level, r in zip(d['perturbation_levels'], d['results']):
    assert r['level'] == level
    assert r['n_finite_h1_features'] >= 0
    assert r['max_persistence'] >= 0 and r['mean_persistence'] >= 0
    assert 0 <= r['top_k_compared'] <= 10
    assert r['top_k_l1_difference'] >= 0
print('PASS: Phase V local perturbation stability audit v1 provenance and perturbation invariants verified.')
