#!/usr/bin/env python3
import hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'results' / 'phase_v_local_perturbation_stability_v1.json'
OUT = ROOT / 'results' / 'phase_v_perturbation_synthesis_v1.json'
if not SRC.exists():
    subprocess.run([sys.executable, str(ROOT / 'results' / 'run_phase_v_local_perturbation_stability_audit_v1.py')], cwd=ROOT, check=True)
if not OUT.exists():
    subprocess.run([sys.executable, str(ROOT / 'results' / 'run_phase_v_perturbation_synthesis_v1.py')], cwd=ROOT, check=True)
s = json.loads(SRC.read_text())
d = json.loads(OUT.read_text())
assert d['status'] == 'PERTURBATION_SYNTHESIS_COMPLETE'
assert d['source_path'] == 'results/phase_v_local_perturbation_stability_v1.json'
assert d['source_sha256'] == hashlib.sha256(SRC.read_bytes()).hexdigest()
assert d['baseline_finite_h1_features'] == s['baseline_finite_h1_features']
assert d['perturbation_levels'] == [0.01, 0.02, 0.05]
assert d['results'] == s['results']
c = d['classification']
assert c['classification_rule'] == 'threshold_free_descriptive_synthesis'
assert c['robust_structural_claim'] == 'NOT_ESTABLISHED_BY_THIS_SYNTHESIS_ALONE'
expected = ('PRESERVED_ALL_LEVELS' if all(r['n_finite_h1_features'] == d['baseline_finite_h1_features'] for r in d['results']) else 'CHANGED_AT_SOME_LEVELS')
assert c['feature_count_preservation'] == expected
assert sorted(c['top_k_change_order']) == sorted(d['perturbation_levels'])
print('PASS: Phase V perturbation synthesis v1 provenance and descriptive-classification invariants verified.')
