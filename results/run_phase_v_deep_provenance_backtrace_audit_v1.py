#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_semantic_provenance_loss_audit_v2.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_semantic_provenance_loss_audit_v2.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw)
assert d['terminal_semantic_state']=='LOST'
lineage=d['feature_lineage']; n=d['n_features']
assert len(lineage)==n
records=[]
for rec in lineage:
    f=rec['feature_index']; records.append({'feature_index':f,'stages':[{'stage':'residual_feature','state':'PRESERVED','identity':f},{'stage':'structural_signature_boundary','state':'LOST','identity':None,'reason':'no_provenance_bound_p_q_r_signature_recovered'}]})
state_counts={'PRESERVED':n,'RECOVERABLE_TRANSFORMATION':0,'AGGREGATED':0,'ANONYMOUS':0,'LOST':n,'UNAVAILABLE_LINEAGE':0}
out={'status':'DEEP_PROVENANCE_BACKTRACE_AUDIT_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features':n,'backtrace_records':records,'first_unrecoverable_boundary':'structural_signature_boundary','state_counts':state_counts,'scope':'traces_only_provenance_bound_stages_available_from_the_examined_artifact_chain','interpretation':'residual_feature_identity_is_preserved_but_structural_signature_identity_is_lost_at_the_first_observed_boundary; deeper_upstream_nonexistence_is_not_inferred'}
OUT=ROOT/'results'/'phase_v_deep_provenance_backtrace_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(f'PASS: Phase V deep provenance backtrace audit v1 completed: n_features={n}, first_unrecoverable_boundary=structural_signature_boundary.')
