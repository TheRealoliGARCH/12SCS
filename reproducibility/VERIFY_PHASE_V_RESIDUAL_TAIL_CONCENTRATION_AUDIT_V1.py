#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_hierarchical_four_mode_reconstruction_audit_v1.json'; OUT=ROOT/'results'/'phase_v_residual_tail_concentration_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_hierarchical_four_mode_reconstruction_audit_v1.py')],cwd=ROOT,check=True)
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_residual_tail_concentration_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); assert d['status']=='RESIDUAL_TAIL_CONCENTRATION_AUDIT_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_features']==55
R=d['ranked_residuals']; assert len(R)==55 and [x['rank'] for x in R]==list(range(1,56)); idx=[x['feature_index'] for x in R]; assert sorted(idx)==list(range(55)); vals=[x['squared_residual_energy'] for x in R]; assert all(math.isfinite(x) and x>=0 for x in vals) and vals==sorted(vals,reverse=True); C=[x['cumulative_squared_residual_share'] for x in R]; assert all(0<=x<=1 for x in C) and all(C[i]<=C[i+1]+1e-15 for i in range(54)) and abs(C[-1]-1)<1e-12
K=d['concentration_checkpoints']; assert [x['top_feature_count'] for x in K]==[1,5,10,25,55]; S=[x['squared_residual_energy_share'] for x in K]; assert all(0<=x<=1 for x in S) and all(S[i]<=S[i+1]+1e-15 for i in range(4)) and abs(S[-1]-1)<1e-12
assert math.isfinite(d['herfindahl_squared_residual_energy']) and 1/55<=d['herfindahl_squared_residual_energy']<=1; assert 1<=d['effective_feature_count_squared_residual_energy']<=55
assert d['interpretation']=='threshold_free_ranked_tail_concentration_description_no_outlier_classification'
print('PASS: Phase V residual tail concentration audit v1 provenance, ranking, checkpoint, and concentration invariants verified.')
