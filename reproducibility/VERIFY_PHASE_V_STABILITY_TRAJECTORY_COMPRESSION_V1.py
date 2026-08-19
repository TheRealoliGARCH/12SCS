#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_persistence_correspondence_v1.json'; OUT=ROOT/'results'/'phase_v_stability_trajectory_compression_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_persistence_correspondence_v1.py')],cwd=ROOT,check=True)
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_stability_trajectory_compression_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text())
assert d['status']=='STABILITY_TRAJECTORY_COMPRESSION_COMPLETE'
assert d['source_path']=='results/phase_v_persistence_correspondence_v1.json'
assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest()
assert d['baseline_feature_count']==55 and d['trajectory_dimension']==8
assert d['compression_rule']=='exact_coordinate_equality_threshold_free'
classes=d['classes']; members=[i for c in classes for i in c['member_indices']]
assert sorted(members)==list(range(55)) and len(set(members))==55
assert d['compressed_feature_count']==len(classes)==len({tuple(c['trajectory']) for c in classes})
assert d['reduction']==55-len(classes)
for c in classes: assert c['representative_index']==min(c['member_indices']) and c['class_size']==len(c['member_indices'])
print('PASS: Phase V stability-trajectory compression v1 provenance, partition, and threshold-free compression invariants verified.')
