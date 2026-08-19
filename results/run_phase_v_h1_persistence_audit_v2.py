#!/usr/bin/env python3
"""Exact Vietoris--Rips H1 persistence over F2 for the canonical 12-state metric."""
import csv, hashlib, itertools, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'results' / 'phase_v_canonical_distance_matrix_v1.csv'
OUT = ROOT / 'results' / 'phase_v_h1_persistence_audit_v2.json'
BARS = ROOT / 'results' / 'phase_v_h1_persistence_bars_v2.csv'

raw = SRC.read_bytes()
source_sha256 = hashlib.sha256(raw).hexdigest()
with SRC.open(newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f))
labels = rows[0][1:]
n = len(labels)
assert n == 12 and len(rows) == n + 1
assert [r[0] for r in rows[1:]] == labels
D = [[float(x) for x in r[1:]] for r in rows[1:]]
assert all(len(r) == n for r in D)
assert all(math.isfinite(x) and x >= 0 for r in D for x in r)
assert all(D[i][i] == 0 for i in range(n))
assert all(abs(D[i][j] - D[j][i]) <= 1e-12 for i in range(n) for j in range(n))

def filt(simplex):
    return 0.0 if len(simplex) <= 1 else max(D[i][j] for i, j in itertools.combinations(simplex, 2))

# Full Rips complex has at most 2^12-1 simplices. Order by filtration, then dimension, then lexicographically.
simplices = [tuple(c) for k in range(1, n + 1) for c in itertools.combinations(range(n), k)]
simplices.sort(key=lambda s: (filt(s), len(s), s))
index = {s: i for i, s in enumerate(simplices)}
values = [filt(s) for s in simplices]

# Standard column reduction of the boundary matrix over F2 using sparse sets.
low_to_col = {}
reduced = {}
positive = set()
pairs = []
for j, s in enumerate(simplices):
    if len(s) == 1:
        col = set()
    else:
        col = {index[s[:k] + s[k+1:]] for k in range(len(s))}
    while col and max(col) in low_to_col:
        col ^= reduced[low_to_col[max(col)]]
    if col:
        low = max(col)
        low_to_col[low] = j
        reduced[j] = col
        pairs.append((low, j))
    else:
        positive.add(j)

bars = []
paired_births = {b for b, d in pairs}
for b, d in pairs:
    if len(simplices[b]) == 2:  # H1 class born at an edge, killed by a triangle or higher simplex boundary pairing
        birth, death = values[b], values[d]
        bars.append((birth, death, death - birth))
for b in positive:
    if len(simplices[b]) == 2 and b not in paired_births:
        bars.append((values[b], math.inf, math.inf))

finite = [x for x in bars if math.isfinite(x[1])]
with BARS.open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['feature_id','birth','death','persistence'])
    for k, (birth, death, persistence) in enumerate(sorted(bars)):
        w.writerow([k, repr(birth), 'inf' if math.isinf(death) else repr(death), 'inf' if math.isinf(persistence) else repr(persistence)])

summary = {
    'status': 'H1_PERSISTENCE_COMPUTATION_COMPLETE',
    'source_matrix_path': str(SRC.relative_to(ROOT)),
    'source_matrix_sha256': source_sha256,
    'n_points': n,
    'n_simplices': len(simplices),
    'n_h1_features': len(bars),
    'n_finite_h1_features': len(finite),
    'n_infinite_h1_features': len(bars) - len(finite),
    'max_persistence': max((x[2] for x in finite), default=0.0),
    'total_h1_persistence': sum(x[2] for x in finite),
}
OUT.write_text(json.dumps(summary, sort_keys=True, indent=2) + '\n')
print(f"PASS: Phase V H1 persistence computation v2 completed: n_points={n}, n_h1_features={len(bars)}.")
