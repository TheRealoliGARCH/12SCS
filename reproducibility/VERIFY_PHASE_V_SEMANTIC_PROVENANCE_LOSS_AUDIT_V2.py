#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_structural_signature_recovery_identification_audit_v1.json'; OUT=ROOT/'results'/'phase_v_semantic_provenance_loss_audit_v2.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_semantic_provenance_loss_audit_v2.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); s=json.loads(SRC.read_text())
assert d['status']=='SEMANTIC_PROVENANCE_LOSS_AUDIT_V2_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest()
i=int(s['identified_feature_count']); u=int(s['unresolved_feature_count']); n=int(s['n_residual_features']); assert i+u==n
assert d['n_features']==n and d['identified_count']==i and d['unresolved_count']==u
ids=s.get('unresolved_feature_indices')
if u>0:
 assert ids is not None and len(ids)==u and d['unresolved_feature_indices']==ids and len(d['feature_lineage'])==u
 expected='LOST' if i==0 else 'PARTIALLY_RECOVERABLE'
else:
 assert d['unresolved_feature_indices']==[] and len(d['feature_lineage'])==0; expected='PRESERVED'
assert d['terminal_semantic_state']==expected
for rec,i0 in zip(d['feature_lineage'],d['unresolved_feature_indices']):
 assert rec['feature_index']==i0 and len(rec['links'])==1 and rec['links'][0]['state']==expected
assert d['scope']=='authoritative_scalar_counts_with_fail_closed_identity_consistency_and_no_inference_of_upstream_nonexistence'
assert d['interpretation']=='semantic_identity_unrecoverable_at_the_examined_feature_to_structural_signature_boundary_without_claiming_nonexistence_of_upstream_p_q_r_structure'
print('PASS: Phase V semantic provenance loss audit v2 provenance, count-identity consistency, fail-closed, lineage, and non-nonexistence invariants verified.')
