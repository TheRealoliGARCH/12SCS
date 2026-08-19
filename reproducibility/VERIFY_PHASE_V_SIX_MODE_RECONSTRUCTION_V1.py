#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_stability_trajectory_compression_v1.json'; SPEC=ROOT/'results'/'phase_v_centered_spectral_compression_v1.json'; OUT=ROOT/'results'/'phase_v_six_mode_reconstruction_v1.json'
for path,runner in [(SRC,'run_phase_v_stability_trajectory_compression_v1.py'),(SPEC,'run_phase_v_centered_spectral_compression_v1.py'),(OUT,'run_phase_v_six_mode_reconstruction_v1.py')]:
 if not path.exists(): subprocess.run([sys.executable,str(ROOT/'results'/runner)],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); assert d['status']=='SIX_MODE_RECONSTRUCTION_AUDIT_COMPLETE'; assert d['trajectory_source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['spectral_source_sha256']==hashlib.sha256(SPEC.read_bytes()).hexdigest(); assert d['n_features']==55 and d['trajectory_dimension']==8
A=d['audits']; assert [a['modes'] for a in A]==[5,6,7]
for a in A: assert all(math.isfinite(a[k]) and a[k]>=0 for k in ['residual_frobenius_norm','max_abs_coordinate_residual']) and 0<=a['explained_spectral_energy']<=1
assert A[0]['residual_frobenius_norm']>=A[1]['residual_frobenius_norm']>=A[2]['residual_frobenius_norm']; assert A[0]['explained_spectral_energy']<=A[1]['explained_spectral_energy']<=A[2]['explained_spectral_energy']; assert d['six_mode']==A[1]
print('PASS: Phase V six-mode reconstruction v1 provenance, reconstruction, residual, and energy invariants verified.')
