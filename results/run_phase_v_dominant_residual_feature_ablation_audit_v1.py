#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_residual_tail_concentration_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_residual_tail_concentration_audit_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw); R=d['ranked_residuals']; assert len(R)==55
E=[float(x['squared_residual_energy']) for x in R]; total=sum(E); assert total>0
rest=E[1:]; rest_total=sum(rest); rest_p=[x/rest_total for x in rest] if rest_total>0 else []
rest_h=sum(x*x for x in rest_p); rest_eff=(1/rest_h) if rest_h>0 else 0.0
out={'status':'DOMINANT_RESIDUAL_FEATURE_ABLATION_AUDIT_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features_before':55,'n_features_after':54,'ablated_feature':R[0],'dominant_energy_share_before':E[0]/total,'remaining_energy_share_after_ablation':rest_total/total,'renormalized_effective_feature_count_after_ablation':rest_eff,'largest_remaining_energy_share_after_ablation':max(rest_p) if rest_p else 0.0,'residual_energy_rank_order_preserved':all(rest[i]>=rest[i+1] for i in range(len(rest)-1)),'interpretation':'leave_one_feature_out_stability_description_on_residual_energy_distribution_no_canonical_feature_removal_or_dimension_redefinition'}
OUT=ROOT/'results'/'phase_v_dominant_residual_feature_ablation_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print(f'PASS: Phase V dominant residual feature ablation audit v1 completed: n_before=55, n_after=54, remaining_energy_share={out["remaining_energy_share_after_ablation"]:.12g}.')
