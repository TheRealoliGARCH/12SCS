#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_stability_trajectory_compression_v1.json'; AUD=ROOT/'results'/'phase_v_six_mode_reconstruction_v1.json'; OUT=ROOT/'results'/'phase_v_canonical_six_mode_coordinates_v1.json'
for p,r in [(SRC,'run_phase_v_stability_trajectory_compression_v1.py'),(AUD,'run_phase_v_six_mode_reconstruction_v1.py'),(OUT,'run_phase_v_canonical_six_mode_coordinates_v1.py')]:
 if not p.exists(): subprocess.run([sys.executable,str(ROOT/'results'/r)],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); assert d['status']=='CANONICAL_SIX_MODE_COORDINATES_COMPLETE'; assert d['trajectory_source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['reconstruction_audit_sha256']==hashlib.sha256(AUD.read_bytes()).hexdigest(); assert d['n_features']==55 and d['original_dimension']==8 and d['reduced_dimension']==6
Q=d['canonical_basis_rows']; F=d['features']; assert len(Q)==6 and all(len(q)==8 for q in Q) and len(F)==55 and all(len(x['six_mode_coordinates'])==6 for x in F)
for q in Q:
 k=max(range(8),key=lambda j:(abs(q[j]),-j)); assert q[k]>=0
for i in range(6):
 for j in range(6):
  dot=sum(Q[i][k]*Q[j][k] for k in range(8)); assert abs(dot-(1.0 if i==j else 0.0))<1e-9
assert math.isfinite(d['reconstruction_residual_frobenius_norm']) and math.isfinite(d['reconstruction_max_abs_coordinate_residual']); assert d['sign_convention']=='largest_absolute_loading_positive_lowest_index_tie_break'; print('PASS: Phase V canonical six-mode coordinates v1 provenance, basis, sign, coordinate, and reconstruction invariants verified.')
