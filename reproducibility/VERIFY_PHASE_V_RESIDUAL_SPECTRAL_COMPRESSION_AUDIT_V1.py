#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_canonical_six_mode_coordinates_v1.json'; OUT=ROOT/'results'/'phase_v_residual_spectral_compression_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_residual_spectral_compression_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); assert d['status']=='RESIDUAL_SPECTRAL_COMPRESSION_AUDIT_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_features']==55 and d['ambient_dimension']==6 and d['dominant_projection_dimension']==2
E=d['residual_eigenvalues']; assert len(E)==6 and all(math.isfinite(x) and x>=0 for x in E) and E==sorted(E,reverse=True); assert 0<=d['positive_residual_eigenvalues']<=4
S=d['residual_spectral_energy_shares']; C=d['residual_cumulative_energy_shares']; assert len(S)==6 and len(C)==6 and all(math.isfinite(x) and x>=0 for x in S+C); assert abs(sum(S)-1)<1e-9; assert all(C[i]<=C[i+1]+1e-15 for i in range(5)); assert abs(C[-1]-1)<1e-9
# Leading two original modes must be annihilated by the residual, up to numerical tolerance.
assert E[4]<=max(1e-12,E[0]*1e-10) and E[5]<=max(1e-12,E[0]*1e-10)
assert d['interpretation']=='orthogonal_two_mode_residual_spectrum_descriptive_only_no_automatic_secondary_dimension_selection'
print('PASS: Phase V residual spectral compression audit v1 provenance, rank, spectrum, and orthogonal-residual invariants verified.')
