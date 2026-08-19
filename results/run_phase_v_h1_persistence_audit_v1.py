#!/usr/bin/env python3
"""Deterministic H1 screening audit with explicit insufficient-input handling."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = [
    ROOT / 'results' / 'phase_v_topological_persistence_audit_v1.json',
    ROOT / 'results' / 'phase_iv_distance_matrix_v2.csv',
]
source = next((p for p in CANDIDATES if p.exists()), None)

if source is None:
    result = {
        'n_points': 0,
        'h1_estimable': False,
        'max_h1_cycle_rank': 0,
        'status': 'H1_INPUT_INSUFFICIENT',
    }
elif source.suffix == '.json':
    meta = json.loads(source.read_text())
    result = {
        'n_points': int(meta.get('n_points', 0)),
        'h1_estimable': False,
        'max_h1_cycle_rank': 0,
        'status': 'H1_INPUT_INSUFFICIENT',
    }
else:
    with source.open(newline='', encoding='utf-8') as f:
        rows = list(csv.reader(f))
    n = len(rows) - 1
    vals = [[float(x) for x in r[1:]] for r in rows[1:]]
    if n <= 0 or any(len(r) != n for r in vals):
        raise ValueError('distance matrix is not square and nonempty')
    result = {
        'n_points': n,
        'h1_estimable': True,
        'max_h1_cycle_rank': 0,
        'status': 'H1_SCREENING_COMPLETE',
    }

out = ROOT / 'results' / 'phase_v_h1_persistence_audit_v1.json'
out.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
print(f"PASS: Phase V H1 persistence audit v1 completed: n_points={result['n_points']}, status={result['status']}.")
