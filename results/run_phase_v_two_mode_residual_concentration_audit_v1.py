#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_two_mode_reconstruction_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_two_mode_reconstruction_audit_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw); r=[float(x) for x in d['per_feature_residual_norms']]; n=len(r); assert n==55
order=sorted(range(n),key=lambda i:(-r[i],i)); total=sum(r); sq=sum(x*x for x in r)
cum=0.0; ranked=[]
for rank,i in enumerate(order,1):
 cum+=r[i]; ranked.append({'rank':rank,'feature_index':i,'residual_norm':r[i],'cumulative_residual_share':cum/total if total else 0.0})
# Threshold-free concentration diagnostics: normalized Herfindahl and Gini coefficient.
shares=[x/total for x in r] if total else [0.0]*n; h=sum(x*x for x in shares); h_norm=(h-1/n)/(1-1/n) if n>1 else 0.0
sr=sorted(r); g=(sum((2*i-n-1)*x for i,x in enumerate(sr,1))/(n*total) if total else 0.0)
# Effective number under squared-residual energy shares.
es=[x*x/sq for x in r] if sq else [0.0]*n; participation=(1/sum(x*x for x in es)) if sq else 0.0
out={'status':'TWO_MODE_RESIDUAL_CONCENTRATION_AUDIT_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features':n,'total_residual_norm':total,'max_residual_norm':max(r),'min_residual_norm':min(r),'ranked_residuals':ranked,'gini_residual_norm':g,'herfindahl_residual_norm':h,'normalized_herfindahl_residual_norm':h_norm,'effective_feature_count_squared_residual':participation,'interpretation':'threshold_free_residual_concentration_and_ranked_tail_description_no_outlier_classification'}
OUT=ROOT/'results'/'phase_v_two_mode_residual_concentration_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print(f'PASS: Phase V two-mode residual concentration audit v1 completed: n_features={n}, effective_feature_count={participation:.12g}.')
