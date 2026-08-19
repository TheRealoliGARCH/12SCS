#!/usr/bin/env python3
"""Synthesize Phase V local perturbation diagnostics deterministically.
The upstream audit is regenerated when its derived artifact is absent, so a
fresh checkout does not depend on untracked prior execution state.
"""
import hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'results' / 'phase_v_local_perturbation_stability_v1.json'
UPSTREAM = ROOT / 'results' / 'run_phase_v_local_perturbation_stability_audit_v1.py'
if not SRC.exists():
    subprocess.run([sys.executable, str(UPSTREAM)], cwd=ROOT, check=True)
if not SRC.exists():
    raise FileNotFoundError(f'upstream perturbation artifact was not generated: {SRC}')
raw = SRC.read_bytes()
d = json.loads(raw)
assert d['status'] == 'LOCAL_PERTURBATION_STABILITY_AUDIT_COMPLETE'
levels = d['perturbation_levels']
rows = d['results']
assert len(levels) == len(rows) and [r['level'] for r in rows] == levels
base = d['baseline_finite_h1_features']
count_preserved = [r['n_finite_h1_features'] == base for r in rows]
ranked = sorted(rows, key=lambda r: (r['top_k_l1_difference'], r['level']))
classification = {
    'feature_count_preservation': 'PRESERVED_ALL_LEVELS' if all(count_preserved) else 'CHANGED_AT_SOME_LEVELS',
    'top_k_change_order': [r['level'] for r in ranked],
    'classification_rule': 'threshold_free_descriptive_synthesis',
    'robust_structural_claim': 'NOT_ESTABLISHED_BY_THIS_SYNTHESIS_ALONE'
}
out = {
    'status': 'PERTURBATION_SYNTHESIS_COMPLETE',
    'source_path': str(SRC.relative_to(ROOT)),
    'source_sha256': hashlib.sha256(raw).hexdigest(),
    'baseline_finite_h1_features': base,
    'perturbation_levels': levels,
    'results': rows,
    'classification': classification
}
PATH = ROOT / 'results' / 'phase_v_perturbation_synthesis_v1.json'
PATH.write_text(json.dumps(out, sort_keys=True, indent=2) + '\n')
print(f"PASS: Phase V perturbation synthesis v1 completed: baseline_features={base}, count_class={classification['feature_count_preservation']}.")
