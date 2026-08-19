#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_canonical_six_mode_coordinates_v1.json'; OUT=ROOT/'results'/'phase_v_feature_trajectory_equivalence_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_canonical_six_mode_coordinates_v1.py')],cwd=ROOT,check=True)
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_feature_trajectory_equivalence_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); assert d['status']=='FEATURE_TRAJECTORY_EQUIVALENCE_AUDIT_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_features']==55 and d['coordinate_dimension']==6
partitions=[('exact_equivalence_classes','exact_equivalence_class_count','exact_reduction'),('central_symmetry_classes','central_symmetry_class_count','central_symmetry_reduction')]
for classes_key,count_key,reduction_key in partitions:
 classes=d[classes_key]; count=d[count_key]; assert len(classes)==count; flat=[x['feature_index'] for g in classes for x in g]; assert sorted(flat)==list(range(55)); assert len(flat)==len(set(flat)); assert d[reduction_key]==55-count
assert d['interpretation']=='exact_coordinate_equivalence_and_sign_symmetry_audit_no_tolerance_clustering'
print('PASS: Phase V feature trajectory equivalence audit v1 provenance, partition, exact-equivalence, and symmetry invariants verified.')
