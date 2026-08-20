#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_post_ablation_residual_concentration_audit_v1.json'; OUT=ROOT/'results'/'phase_v_feature_to_structure_mapping_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_feature_to_structure_mapping_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_residual_features']==54 and d['target_structure_count']==14
assert d['status'] in {'FEATURE_TO_STRUCTURE_MAPPING_NOT_IDENTIFIABLE','FEATURE_TO_STRUCTURE_MAPPING_IDENTIFIABLE'}
assert d['required_structural_fields']==['p','q','r']
if not d['structural_signature_available']:
 assert d['status']=='FEATURE_TO_STRUCTURE_MAPPING_NOT_IDENTIFIABLE'; assert d['mapping_class_count'] is None and d['mapping'] is None
assert d['interpretation']=='identifiability_test_only_no_imputation_of_missing_structural_signatures_no_forced_14_class_partition'
print('PASS: Phase V feature-to-structure mapping audit v1 provenance, identifiability, and non-imputation invariants verified.')
