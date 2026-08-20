#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_structural_signature_recovery_identification_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_structural_signature_recovery_identification_audit_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw)
unresolved=d.get('unresolved_features',[]); n=d.get('n_unresolved',len(unresolved))
# Structural recovery audit is the direct evidence for the terminal semantic state.
terminal='LOST' if n>0 and d.get('identified_count',0)==0 else ('PRESERVED' if n==0 else 'PARTIALLY_RECOVERABLE')
links=['residual_feature','upstream_structural_signature']
records=[]
for x in unresolved:
    records.append({'feature':x,'links':[{'from':links[0],'to':links[1],'state':terminal,'reason':'no_explicit_provenance_bound_feature_level_p_q_r_signature_recovered'}]})
counts={terminal:len(records)}
out={'status':'SEMANTIC_PROVENANCE_LOSS_AUDIT_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features':n,'identified_count':d.get('identified_count',0),'terminal_semantic_state':terminal,'link_state_counts':counts,'feature_lineage':records,'scope':'diagnoses_the_observed_recovery_boundary_only_and_does_not_infer_absence_of_upstream_structure','interpretation':'semantic_identity_unrecoverable_at_the_examined_feature_to_structural_signature_boundary_without_claiming_nonexistence_of_upstream_p_q_r_structure'}
OUT=ROOT/'results'/'phase_v_semantic_provenance_loss_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(f'PASS: Phase V semantic provenance loss audit v1 completed: n_features={n}, terminal_semantic_state={terminal}.')
