#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_structural_signature_recovery_identification_audit_v1.json'; OUT=ROOT/'results'/'phase_v_semantic_provenance_loss_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_semantic_provenance_loss_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); s=json.loads(SRC.read_text())
assert d['status']=='SEMANTIC_PROVENANCE_LOSS_AUDIT_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest()
n=len(s.get('unresolved_features',[])); assert d['n_features']==d['link_state_counts'][d['terminal_semantic_state']]==len(d['feature_lineage'])==n
assert d['identified_count']==s.get('identified_count',0)
for rec,x in zip(d['feature_lineage'],s.get('unresolved_features',[])):
 assert rec['feature']==x and len(rec['links'])==1
 L=rec['links'][0]; assert L['from']=='residual_feature' and L['to']=='upstream_structural_signature' and L['state']==d['terminal_semantic_state']
assert d['terminal_semantic_state'] in {'LOST','PRESERVED','PARTIALLY_RECOVERABLE'}
assert d['scope']=='diagnoses_the_observed_recovery_boundary_only_and_does_not_infer_absence_of_upstream_structure'
assert d['interpretation']=='semantic_identity_unrecoverable_at_the_examined_feature_to_structural_signature_boundary_without_claiming_nonexistence_of_upstream_p_q_r_structure'
print('PASS: Phase V semantic provenance loss audit v1 provenance, boundary-state, lineage, and non-nonexistence invariants verified.')
