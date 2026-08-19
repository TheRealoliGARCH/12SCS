#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]; S=R/'results'/'phase_v_canonical_six_mode_coordinates_v1.json'; O=R/'results'/'phase_v_perron_one_factor_audit_v1.json'
if not S.exists(): subprocess.run([sys.executable,str(R/'results'/'run_phase_v_canonical_six_mode_coordinates_v1.py')],cwd=R,check=True)
if not O.exists(): subprocess.run([sys.executable,str(R/'results'/'run_phase_v_perron_one_factor_audit_v1.py')],cwd=R,check=True)
d=json.loads(O.read_text()); assert d['status']=='PERRON_ONE_FACTOR_AUDIT_COMPLETE'; assert d['source_sha256']==hashlib.sha256(S.read_bytes()).hexdigest(); assert d['n_features']==55 and d['input_dimension']==6 and d['candidate_reduced_dimension']==1
W=d['affinity_matrix']; v=d['perron_vector_l1_normalized']; z=d['one_factor_scores']; assert len(W)==len(v)==6 and all(len(r)==6 for r in W) and len(z)==55; assert abs(sum(v)-1)<1e-12 and all(x>=0 and math.isfinite(x) for x in v)
for i in range(6): assert abs(W[i][i])<1e-15 and all(abs(W[i][j]-W[j][i])<1e-12 for j in range(6))
assert all(math.isfinite(x) for x in z) and 0<=d['retained_centered_energy']<=1 and abs(d['retained_centered_energy']+d['residual_centered_energy']-1)<1e-12
assert d['interpretation']=='perron_weighted_one_factor_candidate_no_automatic_canonicalization'; print('PASS: Phase V Perron one-factor audit v1 provenance, affinity, Perron, projection, and energy invariants verified.')
