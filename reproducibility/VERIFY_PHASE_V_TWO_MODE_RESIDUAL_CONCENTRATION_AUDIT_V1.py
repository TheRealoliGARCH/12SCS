#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_two_mode_reconstruction_audit_v1.json'; OUT=ROOT/'results'/'phase_v_two_mode_residual_concentration_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_two_mode_reconstruction_audit_v1.py')],cwd=ROOT,check=True)
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_two_mode_residual_concentration_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); s=json.loads(SRC.read_text()); assert d['status']=='TWO_MODE_RESIDUAL_CONCENTRATION_AUDIT_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_features']==55
R=d['ranked_residuals']; assert len(R)==55; assert [x['rank'] for x in R]==list(range(1,56)); idx=[x['feature_index'] for x in R]; assert sorted(idx)==list(range(55)); vals=[x['residual_norm'] for x in R]; assert all(math.isfinite(x) and x>=0 for x in vals); assert vals==sorted(vals,reverse=True)
assert all(R[i]['cumulative_residual_share']<=R[i+1]['cumulative_residual_share']+1e-15 for i in range(54)); assert abs(R[-1]['cumulative_residual_share']-1)<1e-12
src=[float(x) for x in s['per_feature_residual_norms']]; assert abs(sum(src)-d['total_residual_norm'])<1e-12; assert abs(max(src)-d['max_residual_norm'])<1e-12; assert abs(min(src)-d['min_residual_norm'])<1e-12
for k in ['gini_residual_norm','herfindahl_residual_norm','normalized_herfindahl_residual_norm']: assert math.isfinite(d[k]) and 0<=d[k]<=1
assert math.isfinite(d['effective_feature_count_squared_residual']) and 1<=d['effective_feature_count_squared_residual']<=55
assert d['interpretation']=='threshold_free_residual_concentration_and_ranked_tail_description_no_outlier_classification'
print('PASS: Phase V two-mode residual concentration audit v1 provenance, ranking, concentration, and threshold-free tail invariants verified.')
