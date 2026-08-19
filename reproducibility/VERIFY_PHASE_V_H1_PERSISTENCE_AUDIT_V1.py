#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'results' / 'phase_v_h1_persistence_audit_v1.json'
data = json.loads(PATH.read_text())
required = {'n_points','h1_estimable','max_h1_cycle_rank','status'}
assert set(data) == required
assert isinstance(data['n_points'], int) and data['n_points'] > 0
assert isinstance(data['h1_estimable'], bool)
assert isinstance(data['max_h1_cycle_rank'], int) and data['max_h1_cycle_rank'] >= 0
assert data['status'] in {'H1_INPUT_INSUFFICIENT','H1_SCREENING_COMPLETE'}
if not data['h1_estimable']:
    assert data['max_h1_cycle_rank'] == 0
print('PASS: Phase V H1 persistence audit v1 schema and non-fabrication invariants verified.')
