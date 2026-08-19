#!/usr/bin/env python3
"""Exact, threshold-free compression of matched persistence trajectories."""
import hashlib, json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_persistence_correspondence_v1.json'
UP=ROOT/'results'/'run_phase_v_persistence_correspondence_v1.py'
if not SRC.exists(): subprocess.run([sys.executable,str(UP)],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw)
assert d['status']=='PERSISTENCE_CORRESPONDENCE_COMPLETE'
assert d['baseline_finite_h1_features']==55
levels=d['perturbation_levels']; audits=d['audits']; assert len(levels)==len(audits)==3
# Construct each trajectory in fixed perturbation-level order. Exact equality only:
# no tolerance or post-hoc similarity threshold is introduced in this first compression stage.
traj={}
for i in range(55):
    v=[]
    for a in audits:
        pair=next(x for x in a['pairs'] if x['baseline_index']==i)
        v.extend([pair['baseline_birth'],pair['baseline_death'],pair['perturbed_birth'],pair['perturbed_death']])
    # baseline coordinates repeat across levels; canonical signature retains one baseline pair
    signature=(v[0],v[1],v[2],v[3],v[6],v[7],v[10],v[11])
    traj.setdefault(signature,[]).append(i)
classes=sorted(({'representative_index':min(m),'member_indices':sorted(m),'class_size':len(m),'trajectory':list(sig)} for sig,m in traj.items()),key=lambda x:x['representative_index'])
out={'status':'STABILITY_TRAJECTORY_COMPRESSION_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'compression_rule':'exact_coordinate_equality_threshold_free','baseline_feature_count':55,'trajectory_dimension':8,'compressed_feature_count':len(classes),'reduction':55-len(classes),'classes':classes}
OUT=ROOT/'results'/'phase_v_stability_trajectory_compression_v1.json'
OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(f"PASS: Phase V stability-trajectory compression v1 completed: input_features=55, compressed_features={len(classes)}, reduction={55-len(classes)}.")
