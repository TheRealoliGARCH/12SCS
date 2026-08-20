#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_residual_tail_concentration_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_residual_tail_concentration_audit_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw); R=d['ranked_residuals']; assert len(R)==55
# Deterministic ranking from the source audit; isolate only descriptively.
E=[x['squared_residual_energy'] for x in R]; total=sum(E); assert total>0
def share(k): return sum(E[:k])/total
out={'status':'DOMINANT_RESIDUAL_FEATURE_ISOLATION_AUDIT_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features':55,'dominant_feature':R[0],'top_1_energy_share':share(1),'top_5_energy_share':share(5),'top_10_energy_share':share(10),'remaining_energy_after_top_1':1-share(1),'remaining_energy_after_top_5':1-share(5),'remaining_energy_after_top_10':1-share(10),'top_to_second_energy_ratio':E[0]/E[1] if E[1]>0 else None,'top_to_rest_energy_ratio':E[0]/sum(E[1:]) if sum(E[1:])>0 else None,'interpretation':'deterministic_ranked_feature_isolation_and_concentration_description_no_outlier_classification_or_dimension_redefinition'}
OUT=ROOT/'results'/'phase_v_dominant_residual_feature_isolation_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print('PASS: Phase V dominant residual feature isolation audit v1 completed: n_features=55, dominant_rank=1.')
