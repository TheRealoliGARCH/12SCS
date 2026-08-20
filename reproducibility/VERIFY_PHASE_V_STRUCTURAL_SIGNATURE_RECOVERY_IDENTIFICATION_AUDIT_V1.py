#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_post_ablation_residual_concentration_audit_v1.json'; OUT=ROOT/'results'/'phase_v_structural_signature_recovery_identification_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_structural_signature_recovery_identification_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); s=json.loads(SRC.read_text()); assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_residual_features']==54 and d['target_structure_count']==14
assert d['identified_feature_count']+d['unresolved_feature_count']==54
ids=sorted(x['feature_index'] for x in s['ranked_remaining_residuals']); assert sorted(d['unresolved_feature_indices']+list(map(int,d['identified_candidates'].keys())))==ids
for i,cands in d['identified_candidates'].items():
 assert int(i) in ids and len(cands)>0
 for c in cands: assert all(k in c for k in ('source_path','p','q','r'))
if d['identification_complete']:
 assert d['status']=='STRUCTURAL_SIGNATURE_RECOVERY_COMPLETE' and d['unresolved_feature_count']==0
else: assert d['status']=='STRUCTURAL_SIGNATURE_RECOVERY_NOT_IDENTIFIABLE' and d['unresolved_feature_count']>0
assert d['interpretation']=='provenance_constrained_signature_recovery_before_classification_no_energy_based_imputation_no_forced_type_assignment'
print('PASS: Phase V structural signature recovery and identification audit v1 provenance, coverage, candidate, and non-imputation invariants verified.')
