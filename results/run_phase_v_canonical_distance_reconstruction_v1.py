#!/usr/bin/env python3
import csv, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
decl = ROOT / 'results' / 'phase_v_canonical_distance_source_v1.csv'
with decl.open(newline='', encoding='utf-8') as f:
    row = next(csv.DictReader(f))

result = {
    'status': row['status'],
    'n_states': 0,
    'n_capabilities': int(row['expected_n_capabilities']),
    'source_sha256': '',
    'matrix_sha256': ''
}

if row['status'] == 'CANONICAL_SOURCE_VALIDATED':
    src = ROOT / row['source_path']
    if not src.exists():
        raise FileNotFoundError(f'declared canonical source missing: {src}')
    raw = src.read_bytes()
    result['source_sha256'] = hashlib.sha256(raw).hexdigest()
    with src.open(newline='', encoding='utf-8') as f:
        rows = list(csv.reader(f))
    if len(rows) - 1 != int(row['expected_n_states']):
        raise ValueError('canonical source does not contain expected number of states')
    result['n_states'] = int(row['expected_n_states'])
    result['status'] = 'CANONICAL_SOURCE_VALIDATED'

out = ROOT / 'results' / 'phase_v_canonical_distance_reconstruction_v1.json'
out.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
print(f"PASS: Phase V canonical distance reconstruction v1 evaluated: status={result['status']}.")
