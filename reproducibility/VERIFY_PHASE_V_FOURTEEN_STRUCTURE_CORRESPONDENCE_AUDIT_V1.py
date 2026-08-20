#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_post_ablation_residual_concentration_audit_v1.json'; OUT=ROOT/'results'/'phase_v_fourteen_structure_correspondence_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_fourteen_structure_correspondence_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); s=json.loads(SRC.read_text()); n=float(s['effective_feature_count_after_ablation'])
assert d['status']=='FOURTEEN_STRUCTURE_CORRESPONDENCE_AUDIT_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_features_after_ablation']==54
assert d['structural_target_count']==14 and abs(d['observed_effective_feature_count']-n)<1e-12
assert abs(d['absolute_deviation_from_14']-abs(n-14))<1e-12 and abs(d['relative_deviation_from_14']-abs(n-14)/14)<1e-12
assert d['nearest_integer_effective_count']==round(n)
L=d['local_integer_deviations']; assert set(L)=={'12','13','14','15','16'}
for k,v in L.items(): assert math.isfinite(v) and abs(v-abs(n-int(k)))<1e-12
assert d['fourteen_is_unique_nearest_integer'] is True
assert d['interpretation']=='numerical_correspondence_only_between_post_ablation_effective_feature_count_and_externally_specified_fourteen_structure_count_no_feature_to_type_mapping_or_causal_claim'
print('PASS: Phase V fourteen-structure correspondence audit v1 provenance, nearest-integer, deviation, and non-mapping invariants verified.')
