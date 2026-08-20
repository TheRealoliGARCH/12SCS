#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_hierarchical_four_mode_reconstruction_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_hierarchical_four_mode_reconstruction_audit_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw); r=[float(x) for x in d['per_feature_residual_norms']]; assert len(r)==55 and all(math.isfinite(x) and x>=0 for x in r)
def quantile(x,q):
 s=sorted(x); z=(len(s)-1)*q; a=int(math.floor(z)); b=int(math.ceil(z)); return s[a] if a==b else s[a]+(z-a)*(s[b]-s[a])
base=sum(x*x for x in r); levels=[0.90,0.95,0.99]; audits=[]
for q in levels:
 cap=quantile(r,q); w=[min(x,cap) for x in r]; e=sum(x*x for x in w); changed=sum(x>cap for x in r); audits.append({'quantile':q,'upper_cap':cap,'changed_feature_count':changed,'post_winsor_squared_residual_energy':e,'post_winsor_energy_ratio_to_baseline':e/base if base else 0.0,'post_winsor_max_residual_norm':max(w),'post_winsor_total_residual_norm':sum(w)})
out={'status':'RESIDUAL_WINSORIZATION_SENSITIVITY_AUDIT_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features':55,'baseline_squared_residual_energy':base,'baseline_total_residual_energy':d['residual_energy'],'winsorization_scope':'per_feature_residual_norm_upper_tail_sensitivity_not_coordinatewise_dimension_reduction','quantile_method':'linear_order_statistic_interpolation','levels':audits,'interpretation':'explicit_upper_tail_clipping_sensitivity_descriptive_only_no_rank_or_dimension_redefinition'}
OUT=ROOT/'results'/'phase_v_residual_winsorization_sensitivity_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print(f'PASS: Phase V residual winsorization sensitivity audit v1 completed: levels={len(levels)}, n_features=55.')
