#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_canonical_six_mode_coordinates_v1.json'; FRONT=ROOT/'results'/'phase_v_rate_distortion_frontier_v1.json'; OUT=ROOT/'results'/'phase_v_two_mode_reconstruction_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_two_mode_reconstruction_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); assert d['status']=='TWO_MODE_RECONSTRUCTION_AUDIT_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['frontier_sha256']==hashlib.sha256(FRONT.read_bytes()).hexdigest(); assert d['n_features']==55 and d['source_dimension']==6 and d['reduced_dimension']==2
for k in ['retained_energy','residual_energy','residual_frobenius_norm','max_abs_coordinate_distortion','max_feature_residual_norm']: assert math.isfinite(d[k]) and d[k]>=0
assert abs(d['retained_energy']+d['residual_energy']-1)<1e-9; assert len(d['per_feature_residual_norms'])==55; assert all(math.isfinite(x) and x>=0 for x in d['per_feature_residual_norms']); assert abs(max(d['per_feature_residual_norms'])-d['max_feature_residual_norm'])<1e-12
f=json.loads(FRONT.read_text()); x=next(z for z in f['frontier'] if z['dimension']==2); assert abs(x['retained_energy']-d['retained_energy'])<1e-9; assert abs(x['residual_energy']-d['residual_energy'])<1e-9; assert abs(x['residual_frobenius_norm']-d['residual_frobenius_norm'])<1e-8
assert d['interpretation']=='two_mode_candidate_reconstruction_audit_no_automatic_canonical_dimension_redefinition'
print('PASS: Phase V two-mode reconstruction audit v1 provenance, frontier consistency, residual, and per-feature invariants verified.')
