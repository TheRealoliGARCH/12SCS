#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_dominant_residual_feature_isolation_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_dominant_residual_feature_isolation_audit_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw)
c1,c5,c10=d['top_1_energy_share'],d['top_5_energy_share'],d['top_10_energy_share']
shape='SINGLE_FEATURE_DOMINANT' if c1>=0.5 else ('SMALL_HEAD_CONCENTRATED' if c5>=0.5 else 'BROADLY_DISTRIBUTED')
out={'status':'DOMINANT_RESIDUAL_CONCENTRATION_INTERPRETATION_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features':d['n_features'],'top_1_energy_share':c1,'top_5_energy_share':c5,'top_10_energy_share':c10,'dominant_feature_rank':d['dominant_feature']['rank'],'concentration_shape':shape,'decision_rule':'top_1_share_at_least_half_else_top_5_share_at_least_half_else_broad','interpretation':'descriptive_concentration_shape_only_no_outlier_classification_feature_removal_or_dimension_redefinition'}
OUT=ROOT/'results'/'phase_v_dominant_residual_concentration_interpretation_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print(f'PASS: Phase V dominant residual concentration interpretation audit v1 completed: shape={shape}, top_1_energy_share={c1:.12g}.')
