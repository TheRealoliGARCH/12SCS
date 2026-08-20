#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_residual_tail_concentration_audit_v1.json'
OUT=ROOT/'results'/'phase_v_post_ablation_residual_concentration_audit_v1.json'
if not OUT.exists():
    subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_post_ablation_residual_concentration_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); s=json.loads(SRC.read_text())
assert d['status']=='POST_ABLATION_RESIDUAL_CONCENTRATION_AUDIT_COMPLETE'
assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest()
assert d['n_features_before']==55 and d['n_features_after']==54
assert d['ablated_feature']==s['ranked_residuals'][0]
assert d['ranked_remaining_residuals']==s['ranked_residuals'][1:]
for k in ['effective_feature_count_after_ablation','largest_remaining_energy_share','top_1_energy_share_after_ablation','top_5_energy_share_after_ablation','top_10_energy_share_after_ablation','concentration_herfindahl_after_ablation']:
    assert math.isfinite(d[k]) and d[k]>=0
assert 1<=d['effective_feature_count_after_ablation']<=54
assert 0<=d['largest_remaining_energy_share']<=1
assert d['top_1_energy_share_after_ablation']==d['largest_remaining_energy_share']
assert d['top_1_energy_share_after_ablation']<=d['top_5_energy_share_after_ablation']<=d['top_10_energy_share_after_ablation']<=1
assert d['top_to_second_energy_ratio_after_ablation'] is None or (math.isfinite(d['top_to_second_energy_ratio_after_ablation']) and d['top_to_second_energy_ratio_after_ablation']>=0)
assert d['rank_order_preserved'] is True
assert d['interpretation']=='renormalized_post_ablation_concentration_description_no_recursive_feature_deletion_or_dimension_redefinition'
print('PASS: Phase V post-ablation residual concentration audit v1 provenance, renormalization, ranking, and non-redefinition invariants verified.')
