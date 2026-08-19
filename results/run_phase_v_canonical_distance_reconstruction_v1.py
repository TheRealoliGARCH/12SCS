#!/usr/bin/env python3
import csv, hashlib, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
decl = ROOT / 'results' / 'phase_v_canonical_distance_source_v1.csv'
with decl.open(newline='', encoding='utf-8') as f:
    row = next(csv.DictReader(f))

result = {'status': row['status'], 'n_states': 0,
          'n_capabilities': int(row['expected_n_capabilities']),
          'source_sha256': '', 'matrix_sha256': ''}

if row['status'] == 'CANONICAL_SOURCE_VALIDATED':
    src = ROOT / row['source_path']
    if not src.exists():
        raise FileNotFoundError(f'declared canonical source missing: {src}')
    raw = src.read_bytes()
    result['source_sha256'] = hashlib.sha256(raw).hexdigest()
    with src.open(newline='', encoding='utf-8') as f:
        rows = list(csv.reader(f))
    header, data = rows[0], rows[1:]
    n, p = int(row['expected_n_states']), int(row['expected_n_capabilities'])
    if len(data) != n or len(header) != p + 1:
        raise ValueError('canonical source dimensionality mismatch')
    states = [r[0] for r in data]
    if len(states) != len(set(states)):
        raise ValueError('state labels must be unique')
    X = [[float(x) for x in r[1:]] for r in data]
    if any(len(x) != p for x in X) or any(not math.isfinite(x) for x in X for x in x):
        raise ValueError('canonical source contains invalid capability values')
    D = [[math.sqrt(sum((X[i][k]-X[j][k])**2 for k in range(p))) for j in range(n)] for i in range(n)]
    for i in range(n):
        if D[i][i] != 0.0: raise ValueError('distance diagonal invariant failed')
        for j in range(n):
            if D[i][j] < 0 or abs(D[i][j]-D[j][i]) > 1e-12: raise ValueError('distance symmetry/nonnegativity invariant failed')
    matrix = ROOT / 'results' / 'phase_v_canonical_distance_matrix_v1.csv'
    with matrix.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['state'] + states)
        for s, d in zip(states, D): w.writerow([s] + [format(x, '.17g') for x in d])
    result.update({'status': 'CANONICAL_DISTANCE_RECONSTRUCTION_COMPLETE', 'n_states': n,
                   'matrix_sha256': hashlib.sha256(matrix.read_bytes()).hexdigest()})

out = ROOT / 'results' / 'phase_v_canonical_distance_reconstruction_v1.json'
out.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
print(f"PASS: Phase V canonical distance reconstruction v1 evaluated: status={result['status']}, n_states={result['n_states']}.")
