#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_dominant_residual_feature_isolation_audit_v1.json'; OUT=ROOT/'results'/'phase_v_dominant_residual_concentration_interpretation_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_dominant_residual_concentration_interpretation_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); s=json.loads(SRC.read_text()); assert d['status']=='DOMINANT_RESIDUAL_CONCENTRATION_INTERPRETATION_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_features']==55
for k in ['top_1_energy_share','top_5_energy_share','top_10_energy_share']:
 assert math.isfinite(d[k]) and abs(d[k]-s[k])<1e-15
assert 0<=d['top_1_energy_share']<=d['top_5_energy_share']<=d['top_10_energy_share']<=1; assert d['dominant_feature_rank']==1
expected='SINGLE_FEATURE_DOMINANT' if d['top_1_energy_share']>=.5 else ('SMALL_HEAD_CONCENTRATED' if d['top_5_energy_share']>=.5 else 'BROADLY_DISTRIBUTED'); assert d['concentration_shape']==expected
assert d['decision_rule']=='top_1_share_at_least_half_else_top_5_share_at_least_half_else_broad'; assert d['interpretation']=='descriptive_concentration_shape_only_no_outlier_classification_feature_removal_or_dimension_redefinition'
print('PASS: Phase V dominant residual concentration interpretation audit v1 provenance, concentration-shape, and non-redefinition invariants verified.')
