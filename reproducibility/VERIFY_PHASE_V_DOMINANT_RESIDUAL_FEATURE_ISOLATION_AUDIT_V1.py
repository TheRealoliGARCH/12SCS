#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_residual_tail_concentration_audit_v1.json'; OUT=ROOT/'results'/'phase_v_dominant_residual_feature_isolation_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_dominant_residual_feature_isolation_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); assert d['status']=='DOMINANT_RESIDUAL_FEATURE_ISOLATION_AUDIT_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_features']==55
a=json.loads(SRC.read_text())['ranked_residuals']; top=d['dominant_feature']; assert top==a[0] and top['rank']==1
for k in ['top_1_energy_share','top_5_energy_share','top_10_energy_share','remaining_energy_after_top_1','remaining_energy_after_top_5','remaining_energy_after_top_10']:
 assert math.isfinite(d[k]) and 0<=d[k]<=1
assert d['top_1_energy_share']<=d['top_5_energy_share']<=d['top_10_energy_share']<=1
assert abs(d['top_1_energy_share']+d['remaining_energy_after_top_1']-1)<1e-12
assert abs(d['top_5_energy_share']+d['remaining_energy_after_top_5']-1)<1e-12
assert abs(d['top_10_energy_share']+d['remaining_energy_after_top_10']-1)<1e-12
for k in ['top_to_second_energy_ratio','top_to_rest_energy_ratio']:
 if d[k] is not None: assert math.isfinite(d[k]) and d[k]>=0
assert d['interpretation']=='deterministic_ranked_feature_isolation_and_concentration_description_no_outlier_classification_or_dimension_redefinition'
print('PASS: Phase V dominant residual feature isolation audit v1 provenance, identity, concentration, and non-classification invariants verified.')
