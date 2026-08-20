#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_residual_tail_concentration_audit_v1.json'; OUT=ROOT/'results'/'phase_v_dominant_residual_feature_ablation_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_dominant_residual_feature_ablation_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); s=json.loads(SRC.read_text()); assert d['status']=='DOMINANT_RESIDUAL_FEATURE_ABLATION_AUDIT_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_features_before']==55 and d['n_features_after']==54; assert d['ablated_feature']==s['ranked_residuals'][0]
for k in ['dominant_energy_share_before','remaining_energy_share_after_ablation','renormalized_effective_feature_count_after_ablation','largest_remaining_energy_share_after_ablation']:
 assert math.isfinite(d[k]) and d[k]>=0
assert abs(d['dominant_energy_share_before']+d['remaining_energy_share_after_ablation']-1)<1e-12
assert 1<=d['renormalized_effective_feature_count_after_ablation']<=54
assert 0<=d['largest_remaining_energy_share_after_ablation']<=1
assert d['residual_energy_rank_order_preserved'] is True
assert d['interpretation']=='leave_one_feature_out_stability_description_on_residual_energy_distribution_no_canonical_feature_removal_or_dimension_redefinition'
print('PASS: Phase V dominant residual feature ablation audit v1 provenance, leave-one-out identity, concentration, and non-redefinition invariants verified.')
