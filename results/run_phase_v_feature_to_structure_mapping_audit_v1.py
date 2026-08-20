#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_post_ablation_residual_concentration_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_post_ablation_residual_concentration_audit_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw); R=d['ranked_remaining_residuals']; assert len(R)==54
feature_keys=sorted(set().union(*(set(x) for x in R))); required={'p','q','r'}; available=required.issubset(feature_keys)
status='FEATURE_TO_STRUCTURE_MAPPING_IDENTIFIABLE' if available else 'FEATURE_TO_STRUCTURE_MAPPING_NOT_IDENTIFIABLE'
out={'status':status,'source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_residual_features':54,'target_structure_count':14,'available_feature_fields':feature_keys,'required_structural_fields':['p','q','r'],'structural_signature_available':available,'mapping_class_count':None,'mapping':None,'reason':'source_residual_artifact_does_not_supply_provenance_bound_p_q_r_structural_signatures_for_feature_level_assignment' if not available else 'structural_signatures_available_but_assignment_not_implemented','interpretation':'identifiability_test_only_no_imputation_of_missing_structural_signatures_no_forced_14_class_partition'}
OUT=ROOT/'results'/'phase_v_feature_to_structure_mapping_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print(f'PASS: Phase V feature-to-structure mapping audit v1 completed: status={status}, n_residual_features=54, target_structure_count=14.')
