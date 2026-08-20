#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_residual_spectral_compression_audit_v1.json'; BASE=ROOT/'results'/'phase_v_two_mode_reconstruction_audit_v1.json'; OUT=ROOT/'results'/'phase_v_residual_rate_distortion_frontier_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_residual_rate_distortion_frontier_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); assert d['status']=='RESIDUAL_RATE_DISTORTION_FRONTIER_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['two_mode_source_sha256']==hashlib.sha256(BASE.read_bytes()).hexdigest(); assert d['residual_source_rank']==4 and d['candidate_dimensions']==[3,2,1]
F=d['frontier']; assert [x['residual_dimension'] for x in F]==[3,2,1]
prev=0.0
for x in reversed(F):
 for k in ['retained_residual_energy','discarded_residual_energy','relative_frobenius_distortion','cumulative_total_energy_retained']: assert math.isfinite(x[k]) and x[k]>=0
 assert abs(x['retained_residual_energy']+x['discarded_residual_energy']-1)<1e-12; assert abs(x['relative_frobenius_distortion']**2-x['discarded_residual_energy'])<1e-12
# Retained residual energy must increase with residual dimension.
assert F[0]['retained_residual_energy']>=F[1]['retained_residual_energy']>=F[2]['retained_residual_energy']
assert F[0]['cumulative_total_energy_retained']>=F[1]['cumulative_total_energy_retained']>=F[2]['cumulative_total_energy_retained']
assert d['interpretation']=='conditional_residual_rate_distortion_frontier_relative_to_two_mode_baseline_no_automatic_dimension_selection'
print('PASS: Phase V residual rate-distortion frontier v1 provenance, ordering, conditional energy, and monotonic-distortion invariants verified.')
