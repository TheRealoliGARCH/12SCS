#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_structural_signature_recovery_identification_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_structural_signature_recovery_identification_audit_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw)
identified=int(d['identified_feature_count']); unresolved=int(d['unresolved_feature_count']); n=int(d['n_residual_features'])
assert identified>=0 and unresolved>=0 and identified+unresolved==n
ids=d.get('unresolved_feature_indices')
if unresolved>0:
    if ids is None: raise RuntimeError('FAIL_CLOSED: unresolved_feature_count positive but unresolved_feature_indices absent')
    assert len(ids)==unresolved and len(set(ids))==len(ids)
    terminal='LOST' if identified==0 else 'PARTIALLY_RECOVERABLE'
else:
    assert ids in (None,[]); ids=[]; terminal='PRESERVED'
records=[{'feature_index':i,'links':[{'from':'residual_feature','to':'upstream_structural_signature','state':terminal,'reason':'no_explicit_provenance_bound_feature_level_p_q_r_signature_recovered'}]} for i in ids]
out={'status':'SEMANTIC_PROVENANCE_LOSS_AUDIT_V2_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features':n,'identified_count':identified,'unresolved_count':unresolved,'terminal_semantic_state':terminal,'unresolved_feature_indices':ids,'feature_lineage':records,'scope':'authoritative_scalar_counts_with_fail_closed_identity_consistency_and_no_inference_of_upstream_nonexistence','interpretation':'semantic_identity_unrecoverable_at_the_examined_feature_to_structural_signature_boundary_without_claiming_nonexistence_of_upstream_p_q_r_structure'}
OUT=ROOT/'results'/'phase_v_semantic_provenance_loss_audit_v2.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(f'PASS: Phase V semantic provenance loss audit v2 completed: n_features={n}, identified={identified}, unresolved={unresolved}, terminal_semantic_state={terminal}.')
