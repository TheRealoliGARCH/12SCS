#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_semantic_provenance_loss_audit_v2.json'; OUT=ROOT/'results'/'phase_v_deep_provenance_backtrace_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_deep_provenance_backtrace_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); s=json.loads(SRC.read_text())
assert d['status']=='DEEP_PROVENANCE_BACKTRACE_AUDIT_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_features']==s['n_features']==len(d['backtrace_records'])
assert d['first_unrecoverable_boundary']=='structural_signature_boundary'
assert d['state_counts']['PRESERVED']==d['n_features'] and d['state_counts']['LOST']==d['n_features']
for r,x in zip(d['backtrace_records'],s['feature_lineage']):
 assert r['feature_index']==x['feature_index'] and len(r['stages'])==2
 a,b=r['stages']; assert a['stage']=='residual_feature' and a['state']=='PRESERVED' and a['identity']==r['feature_index']; assert b['stage']=='structural_signature_boundary' and b['state']=='LOST' and b['identity'] is None
assert d['scope']=='traces_only_provenance_bound_stages_available_from_the_examined_artifact_chain'
assert d['interpretation']=='residual_feature_identity_is_preserved_but_structural_signature_identity_is_lost_at_the_first_observed_boundary; deeper_upstream_nonexistence_is_not_inferred'
print('PASS: Phase V deep provenance backtrace audit v1 provenance, stage-order, first-boundary, and non-nonexistence invariants verified.')
