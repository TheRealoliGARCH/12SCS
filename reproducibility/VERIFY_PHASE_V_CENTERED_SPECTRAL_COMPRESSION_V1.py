#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_stability_trajectory_compression_v1.json'; OUT=ROOT/'results'/'phase_v_centered_spectral_compression_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_stability_trajectory_compression_v1.py')],cwd=ROOT,check=True)
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_centered_spectral_compression_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); assert d['status']=='CENTERED_SPECTRAL_COMPRESSION_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_features']==55 and d['trajectory_dimension']==8
lam=d['centered_eigenvalues']; assert len(lam)==8 and lam==sorted(lam,reverse=True) and all(math.isfinite(x) and x>=0 for x in lam)
e=d['cumulative_spectral_energy']; assert len(e)==8 and all(0<=x<=1 for x in e) and e==sorted(e) and abs(e[-1]-1)<1e-12
g=d['spectral_gaps']; assert len(g)==7 and all(x is None or (math.isfinite(x) and x>=0) for x in g)
assert 1<=d['largest_observed_gap_after_mode']<=7; assert d['interpretation']=='spectral_diagnostics_no_automatic_dimension_selection'
print('PASS: Phase V centered spectral compression v1 provenance, centering, spectrum, energy, and gap invariants verified.')
