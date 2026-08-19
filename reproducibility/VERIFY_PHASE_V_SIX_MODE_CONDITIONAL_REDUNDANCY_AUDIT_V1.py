#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_canonical_six_mode_coordinates_v1.json'; OUT=ROOT/'results'/'phase_v_six_mode_conditional_redundancy_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_canonical_six_mode_coordinates_v1.py')],cwd=ROOT,check=True)
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_six_mode_conditional_redundancy_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); assert d['status']=='SIX_MODE_CONDITIONAL_REDUNDANCY_AUDIT_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_features']==55 and d['mode_dimension']==6
lam=d['centered_gram_eigenvalues']; assert len(lam)==6 and lam==sorted(lam,reverse=True) and all(math.isfinite(x) and x>=0 for x in lam); assert d['positive_eigenvalue_count']==sum(x>0 for x in lam)
P=d['partial_correlation_matrix']
if d['gram_invertible']:
 assert P is not None and len(P)==6 and all(len(r)==6 for r in P)
 for i in range(6):
  assert abs(P[i][i]-1)<1e-12
  for j in range(6): assert math.isfinite(P[i][j]) and abs(P[i][j]-P[j][i])<1e-9
else: assert P is None
assert d['interpretation']=='conditional_redundancy_diagnostic_no_automatic_dimension_reduction'
print('PASS: Phase V six-mode conditional redundancy audit v1 provenance, rank, inversion, and partial-correlation invariants verified.')
