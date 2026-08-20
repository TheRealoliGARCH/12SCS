#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_post_ablation_residual_concentration_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_post_ablation_residual_concentration_audit_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw); R=d['ranked_remaining_residuals']; ids=sorted(x['feature_index'] for x in R); assert ids==[i for i in range(55) if i!=d['ablated_feature']['feature_index']]
# Search only repository result JSON artifacts for explicit feature-level p,q,r records.
found={i:[] for i in ids}
for path in sorted((ROOT/'results').glob('*.json')):
    try: obj=json.loads(path.read_text())
    except Exception: continue
    stack=[obj]
    while stack:
        x=stack.pop()
        if isinstance(x,dict):
            if 'feature_index' in x and all(k in x for k in ('p','q','r')):
                try:
                    i=int(x['feature_index']); vals=[float(x[k]) for k in ('p','q','r')]
                    if i in found and all(v==v for v in vals): found[i].append({'source_path':str(path.relative_to(ROOT)),'p':vals[0],'q':vals[1],'r':vals[2]})
                except Exception: pass
            stack.extend(x.values())
        elif isinstance(x,list): stack.extend(x)
identified={i:v for i,v in found.items() if v}
unresolved=[i for i in ids if not found[i]]
out={'status':'STRUCTURAL_SIGNATURE_RECOVERY_NOT_IDENTIFIABLE' if unresolved else 'STRUCTURAL_SIGNATURE_RECOVERY_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_residual_features':54,'target_structure_count':14,'recovery_scope':'explicit_feature_level_p_q_r_records_in_results_json_only','identified_feature_count':len(identified),'unresolved_feature_count':len(unresolved),'identified_candidates':identified,'unresolved_feature_indices':unresolved,'identification_complete':not unresolved,'interpretation':'provenance_constrained_signature_recovery_before_classification_no_energy_based_imputation_no_forced_type_assignment'}
OUT=ROOT/'results'/'phase_v_structural_signature_recovery_identification_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print(f'PASS: Phase V structural signature recovery and identification audit v1 completed: status={out["status"]}, identified={len(identified)}, unresolved={len(unresolved)}.')
