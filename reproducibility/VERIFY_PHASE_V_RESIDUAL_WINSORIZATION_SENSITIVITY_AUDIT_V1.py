#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_hierarchical_four_mode_reconstruction_audit_v1.json'; OUT=ROOT/'results'/'phase_v_residual_winsorization_sensitivity_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_hierarchical_four_mode_reconstruction_audit_v1.py')],cwd=ROOT,check=True)
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_residual_winsorization_sensitivity_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); s=json.loads(SRC.read_text()); assert d['status']=='RESIDUAL_WINSORIZATION_SENSITIVITY_AUDIT_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_features']==55
r=[float(x) for x in s['per_feature_residual_norms']]; base=sum(x*x for x in r); assert abs(base-d['baseline_squared_residual_energy'])<1e-15
L=d['levels']; assert [x['quantile'] for x in L]==[0.9,0.95,0.99]; prev_cap=-1; prev_changed=56
for x in L:
 for k in ['upper_cap','post_winsor_squared_residual_energy','post_winsor_energy_ratio_to_baseline','post_winsor_max_residual_norm','post_winsor_total_residual_norm']: assert math.isfinite(x[k]) and x[k]>=0
 assert x['upper_cap']>=prev_cap; assert x['changed_feature_count']<=prev_changed; assert x['changed_feature_count']>=0; assert x['post_winsor_squared_residual_energy']<=base+1e-15; assert 0<=x['post_winsor_energy_ratio_to_baseline']<=1+1e-12; assert x['post_winsor_max_residual_norm']<=x['upper_cap']+1e-15; prev_cap=x['upper_cap']; prev_changed=x['changed_feature_count']
assert d['winsorization_scope']=='per_feature_residual_norm_upper_tail_sensitivity_not_coordinatewise_dimension_reduction'; assert d['interpretation']=='explicit_upper_tail_clipping_sensitivity_descriptive_only_no_rank_or_dimension_redefinition'
print('PASS: Phase V residual winsorization sensitivity audit v1 provenance, clipping, monotonicity, and non-redefinition invariants verified.')
