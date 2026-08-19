#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_canonical_six_mode_coordinates_v1.json'; OUT=ROOT/'results'/'phase_v_projective_feature_quotient_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_canonical_six_mode_coordinates_v1.py')],cwd=ROOT,check=True)
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_projective_feature_quotient_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); assert d['status']=='PROJECTIVE_FEATURE_QUOTIENT_AUDIT_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_features']==55 and d['coordinate_dimension']==6
classes=d['projective_equivalence_classes']; assert len(classes)==d['projective_equivalence_class_count']; flat=[x['feature_index'] for c in classes for x in c]; assert sorted(flat)==list(range(55)); assert len(flat)==len(set(flat)); assert d['projective_reduction']==55-len(classes); assert d['equivalence_definition'].startswith('y_i~y_j iff y_i=c*y_j'); assert d['interpretation']=='exact_projective_quotient_audit_no_tolerance_clustering'
print('PASS: Phase V projective feature quotient audit v1 provenance, partition, normalization, and quotient invariants verified.')
