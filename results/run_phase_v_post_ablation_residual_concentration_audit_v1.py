#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_residual_tail_concentration_audit_v1.json'
if not SRC.exists():
    subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_residual_tail_concentration_audit_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw); R=d['ranked_residuals']; assert len(R)==55
A=R[1:]; E=[float(x['squared_residual_energy']) for x in A]; total=sum(E); assert total>0
P=[x/total for x in E]; H=sum(x*x for x in P); neff=1/H
out={
 'status':'POST_ABLATION_RESIDUAL_CONCENTRATION_AUDIT_COMPLETE',
 'source_path':str(SRC.relative_to(ROOT)),
 'source_sha256':hashlib.sha256(raw).hexdigest(),
 'n_features_before':55,'n_features_after':54,
 'ablated_feature':R[0],
 'ranked_remaining_residuals':A,
 'effective_feature_count_after_ablation':neff,
 'largest_remaining_energy_share':P[0],
 'top_1_energy_share_after_ablation':sum(P[:1]),
 'top_5_energy_share_after_ablation':sum(P[:5]),
 'top_10_energy_share_after_ablation':sum(P[:10]),
 'top_to_second_energy_ratio_after_ablation':E[0]/E[1] if E[1]>0 else None,
 'concentration_herfindahl_after_ablation':H,
 'rank_order_preserved':all(E[i]>=E[i+1] for i in range(len(E)-1)),
 'interpretation':'renormalized_post_ablation_concentration_description_no_recursive_feature_deletion_or_dimension_redefinition'
}
OUT=ROOT/'results'/'phase_v_post_ablation_residual_concentration_audit_v1.json'
OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(f'PASS: Phase V post-ablation residual concentration audit v1 completed: n_features=54, effective_feature_count={neff:.12g}.')
