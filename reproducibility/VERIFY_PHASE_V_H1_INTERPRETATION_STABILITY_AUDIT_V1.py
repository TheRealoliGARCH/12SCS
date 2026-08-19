#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results' / 'phase_v_h1_interpretation_stability_v1.json'
BARS = ROOT / 'results' / 'phase_v_h1_persistence_bars_v2.csv'
d = json.loads(OUT.read_text())
s = d['summary']
assert s['source_bars_path'] == 'results/phase_v_h1_persistence_bars_v2.csv'
assert s['source_bars_sha256'] == hashlib.sha256(BARS.read_bytes()).hexdigest()
assert s['n_h1_features'] >= 0
assert s['max_persistence'] >= 0
assert s['mean_persistence'] >= 0
assert s['median_persistence'] >= 0
assert s['total_persistence'] >= 0
assert len(d['top_features']) == min(10, s['n_h1_features'])
for i, x in enumerate(d['top_features'], 1):
    assert x['rank'] == i and x['death'] >= x['birth']
    assert abs(x['persistence'] - (x['death'] - x['birth'])) < 1e-12
assert s['stability_scales'] == [0.95, 1.0, 1.05]
assert s['stability_pass'] is True
for x in d['scale_stability']:
    assert abs(x['normalized_max_ratio'] - 1.0) < 1e-12
print('PASS: Phase V H1 interpretation and stability audit v1 provenance, persistence, and scale-stability invariants verified.')
