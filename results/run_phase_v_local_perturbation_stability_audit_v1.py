#!/usr/bin/env python3
"""Deterministic local-coordinate perturbation audit for Phase V H1 persistence."""
import csv, hashlib, itertools, json, math, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'results' / 'capability_latent_matrix_v2.csv'
BASE_BARS = ROOT / 'results' / 'phase_v_h1_persistence_bars_v2.csv'
OUT = ROOT / 'results' / 'phase_v_local_perturbation_stability_v1.json'

raw = SRC.read_bytes()
source_sha = hashlib.sha256(raw).hexdigest()
base_sha = hashlib.sha256(BASE_BARS.read_bytes()).hexdigest()
with SRC.open(newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f))
assert rows and rows[0][0] == 'state'
capabilities = rows[0][1:]
state_labels = [r[0] for r in rows[1:]]
X = [[float(x) for x in r[1:]] for r in rows[1:]]
n, p = len(X), len(capabilities)
assert n == 12 and p == 12
assert len(set(state_labels)) == n and all(state_labels)
assert all(len(r) == p and all(math.isfinite(x) for x in r) for r in X)

with BASE_BARS.open(newline='', encoding='utf-8') as f:
    baseline = [r for r in csv.DictReader(f) if r['death'] != 'inf']
base_p = sorted([float(r['persistence']) for r in baseline], reverse=True)

def h1_persistence(Y):
    D = [[math.dist(Y[i], Y[j]) for j in range(n)] for i in range(n)]
    def filt(s):
        return 0.0 if len(s) <= 1 else max(D[i][j] for i, j in itertools.combinations(s, 2))
    simplices = [tuple(c) for k in range(1, n + 1) for c in itertools.combinations(range(n), k)]
    simplices.sort(key=lambda s: (filt(s), len(s), s))
    index = {s: i for i, s in enumerate(simplices)}
    values = [filt(s) for s in simplices]
    low_to_col, reduced, pairs = {}, {}, []
    for j, s in enumerate(simplices):
        col = set() if len(s) == 1 else {index[s[:k] + s[k+1:]] for k in range(len(s))}
        while col and max(col) in low_to_col:
            col ^= reduced[low_to_col[max(col)]]
        if col:
            low = max(col); low_to_col[low] = j; reduced[j] = col; pairs.append((low, j))
    return sorted([values[d] - values[b] for b, d in pairs if len(simplices[b]) == 2], reverse=True)

ranges = [max(X[i][j] for i in range(n)) - min(X[i][j] for i in range(n)) for j in range(p)]
levels = [0.01, 0.02, 0.05]
results = []
for level in levels:
    Y = [[x + (-1.0 if ((i + 2*j) % 2) else 1.0) * level * ranges[j]
          for j, x in enumerate(row)] for i, row in enumerate(X)]
    pert = h1_persistence(Y)
    k = min(10, len(base_p), len(pert))
    top_l1 = sum(abs(base_p[q] - pert[q]) for q in range(k)) if k else 0.0
    results.append({'level': level, 'n_finite_h1_features': len(pert),
                    'max_persistence': max(pert, default=0.0),
                    'mean_persistence': statistics.fmean(pert) if pert else 0.0,
                    'top_k_compared': k, 'top_k_l1_difference': top_l1})

out = {'status': 'LOCAL_PERTURBATION_STABILITY_AUDIT_COMPLETE',
       'source_latent_matrix_path': str(SRC.relative_to(ROOT)),
       'source_latent_matrix_sha256': source_sha,
       'baseline_bars_path': str(BASE_BARS.relative_to(ROOT)),
       'baseline_bars_sha256': base_sha,
       'n_states': n, 'n_capabilities': p,
       'perturbation_rule': 'checkerboard_signed_fraction_of_coordinate_range',
       'perturbation_levels': levels,
       'baseline_finite_h1_features': len(base_p),
       'results': results}
OUT.write_text(json.dumps(out, sort_keys=True, indent=2) + '\n')
print(f"PASS: Phase V local perturbation stability audit v1 completed: levels={len(levels)}, baseline_finite_h1_features={len(base_p)}.")
