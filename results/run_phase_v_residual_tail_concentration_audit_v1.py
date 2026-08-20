#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_hierarchical_four_mode_reconstruction_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_hierarchical_four_mode_reconstruction_audit_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw); r=[float(x) for x in d['per_feature_residual_norms']]; n=len(r); assert n==55
z=[x*x for x in r]; total=sum(z); order=sorted(range(n),key=lambda i:(-z[i],i)); ranked=[]; c=0.0
for rank,i in enumerate(order,1):
 c+=z[i]; ranked.append({'rank':rank,'feature_index':i,'residual_norm':r[i],'squared_residual_energy':z[i],'cumulative_squared_residual_share':c/total if total else 0.0})
# Threshold-free concentration checkpoints at fixed fractions of the ordered feature set.
checkpoints=[]
for num,den in [(1,55),(5,55),(10,55),(25,55),(55,55)]:
 k=num; share=sum(z[i] for i in order[:k])/total if total else 0.0; checkpoints.append({'top_feature_count':k,'feature_fraction':k/n,'squared_residual_energy_share':share})
p=[x/total if total else 0.0 for x in z]; h=sum(x*x for x in p); eff=1/h if h else 0.0
out={'status':'RESIDUAL_TAIL_CONCENTRATION_AUDIT_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features':n,'ranked_residuals':ranked,'concentration_checkpoints':checkpoints,'herfindahl_squared_residual_energy':h,'effective_feature_count_squared_residual_energy':eff,'interpretation':'threshold_free_ranked_tail_concentration_description_no_outlier_classification'}
OUT=ROOT/'results'/'phase_v_residual_tail_concentration_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print(f'PASS: Phase V residual tail concentration audit v1 completed: n_features={n}, effective_feature_count={eff:.12g}.')
