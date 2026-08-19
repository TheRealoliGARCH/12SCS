#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_canonical_six_mode_coordinates_v1.json'; OUT=ROOT/'results'/'phase_v_rate_distortion_frontier_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_canonical_six_mode_coordinates_v1.py')],cwd=ROOT,check=True)
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_rate_distortion_frontier_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); assert d['status']=='RATE_DISTORTION_FRONTIER_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_features']==55 and d['source_dimension']==6
F=d['frontier']; assert [x['dimension'] for x in F]==[5,4,3,2,1]
for x in F:
 for k in ['retained_energy','residual_energy','residual_frobenius_norm','max_abs_coordinate_distortion']: assert math.isfinite(x[k]) and x[k]>=0
 assert abs(x['retained_energy']+x['residual_energy']-1)<1e-9
# Traversal is descending k, so retained energy and reconstruction quality must not improve.
for a,b in zip(F,F[1:]): assert a['retained_energy']>=b['retained_energy']; assert a['residual_frobenius_norm']<=b['residual_frobenius_norm']; assert a['max_abs_coordinate_distortion']<=b['max_abs_coordinate_distortion']+1e-9
assert d['interpretation']=='deterministic_pca_reconstruction_frontier_no_loss_threshold_or_canonical_dimension_selection'
print('PASS: Phase V rate-distortion frontier v1 provenance, ordering, energy, and monotonic-distortion invariants verified.')
