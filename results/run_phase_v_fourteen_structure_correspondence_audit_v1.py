#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_post_ablation_residual_concentration_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_post_ablation_residual_concentration_audit_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw)
neff=float(d['effective_feature_count_after_ablation']); target=14
neighbors={str(k):abs(neff-k) for k in (12,13,14,15,16)}
nearest=min((abs(neff-k),k) for k in range(1,55))[1]
out={'status':'FOURTEEN_STRUCTURE_CORRESPONDENCE_AUDIT_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features_after_ablation':54,'observed_effective_feature_count':neff,'structural_target_count':target,'absolute_deviation_from_14':abs(neff-target),'relative_deviation_from_14':abs(neff-target)/target,'nearest_integer_effective_count':nearest,'local_integer_deviations':neighbors,'fourteen_is_unique_nearest_integer':nearest==14 and neighbors['14']<neighbors['13'] and neighbors['14']<neighbors['15'],'interpretation':'numerical_correspondence_only_between_post_ablation_effective_feature_count_and_externally_specified_fourteen_structure_count_no_feature_to_type_mapping_or_causal_claim'}
OUT=ROOT/'results'/'phase_v_fourteen_structure_correspondence_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(f'PASS: Phase V fourteen-structure correspondence audit v1 completed: effective_feature_count={neff:.12g}, nearest_integer={nearest}, abs_deviation_from_14={abs(neff-14):.12g}.')
