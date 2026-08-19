#!/usr/bin/env python3
import csv, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/'results'; out=RESULTS/'phase_v_topological_persistence_audit_v1.csv'
assert out.exists(), 'Run the Phase V audit first.'
with out.open(newline='',encoding='utf-8') as f: d={r['metric']:r['value'] for r in csv.DictReader(f)}
required={'source_artifact','n_points','h0_finite_bars','h0_birth','h0_max_death','h0_total_persistence','source_sha256'}
assert required==set(d)
n=int(d['n_points']); assert n>1 and int(d['h0_finite_bars'])==n-1
assert float(d['h0_birth'])==0.0 and float(d['h0_max_death'])>=0 and float(d['h0_total_persistence'])>=0
source=RESULTS/d['source_artifact']; assert source.exists()
assert hashlib.sha256(source.read_bytes()).hexdigest()==d['source_sha256']
print('PASS: Phase V topological persistence audit v1 provenance and H0 invariants verified.')
