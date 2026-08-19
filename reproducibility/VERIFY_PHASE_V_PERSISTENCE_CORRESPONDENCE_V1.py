#!/usr/bin/env python3
import hashlib, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'/'phase_v_persistence_correspondence_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_persistence_correspondence_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); BASE=ROOT/'results'/'phase_v_h1_persistence_bars_v2.csv'
assert d['status']=='PERSISTENCE_CORRESPONDENCE_COMPLETE'
assert d['baseline_bars_sha256']==hashlib.sha256(BASE.read_bytes()).hexdigest()
assert d['perturbation_levels']==[0.01,0.02,0.05]
assert d['baseline_finite_h1_features']==55
assert d['correspondence_method']=='minimum_cost_bipartite_assignment_linf_birth_death'
assert len(d['audits'])==3
for a in d['audits']:
 assert a['n_matched']==55 and len(a['pairs'])==55
 assert sorted(x['baseline_index'] for x in a['pairs'])==list(range(55))
 assert sorted(x['perturbed_index'] for x in a['pairs'])==list(range(55))
 assert all(x['linf_displacement']>=0 for x in a['pairs'])
assert sorted(d['cross_level_correspondence_complete_indices'])==list(range(d['cross_level_correspondence_complete_count']))
assert 0<=d['cross_level_correspondence_complete_count']<=55
print('PASS: Phase V persistence correspondence v1 provenance, matching, and cross-level invariants verified.')
