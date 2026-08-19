#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]; S=R/'results'/'phase_v_canonical_six_mode_coordinates_v1.json'
if not S.exists(): subprocess.run([sys.executable,str(R/'results'/'run_phase_v_canonical_six_mode_coordinates_v1.py')],cwd=R,check=True)
raw=S.read_bytes(); d=json.loads(raw); Y=[[float(x) for x in f['six_mode_coordinates']] for f in d['features']]; n=len(Y); p=6
mu=[sum(r[j] for r in Y)/n for j in range(p)]; X=[[r[j]-mu[j] for j in range(p)] for r in Y]
# Nonnegative mode-affinity matrix: absolute normalized inner products, zero diagonal.
G=[[sum(r[i]*r[j] for r in X) for j in range(p)] for i in range(p)]; sd=[math.sqrt(G[i][i]) for i in range(p)]
W=[[0.0 if i==j else abs(G[i][j])/(sd[i]*sd[j]) if sd[i]*sd[j]>0 else 0.0 for j in range(p)] for i in range(p)]
v=[1.0/p]*p
for _ in range(10000):
 u=[sum(W[i][j]*v[j] for j in range(p)) for i in range(p)]; z=sum(u)
 if z==0: break
 u=[x/z for x in u]
 if max(abs(u[i]-v[i]) for i in range(p))<1e-15: v=u; break
 v=u
rho=sum(v[i]*sum(W[i][j]*v[j] for j in range(p)) for i in range(p))/sum(x*x for x in v)
q=[x/math.sqrt(sum(t*t for t in v)) for x in v]; z=[sum(r[j]*q[j] for j in range(p)) for r in X]; total=sum(x*x for r in X for x in r); retained=sum(x*x for x in z)/total if total else 0.0
out={'status':'PERRON_ONE_FACTOR_AUDIT_COMPLETE','source_path':str(S.relative_to(R)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features':n,'input_dimension':6,'candidate_reduced_dimension':1,'affinity_definition':'absolute_centered_mode_correlation_zero_diagonal','affinity_matrix':W,'perron_vector_l1_normalized':v,'spectral_radius':rho,'retained_centered_energy':retained,'residual_centered_energy':1-retained,'one_factor_scores':z,'interpretation':'perron_weighted_one_factor_candidate_no_automatic_canonicalization'}
O=R/'results'/'phase_v_perron_one_factor_audit_v1.json'; O.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print(f'PASS: Phase V Perron one-factor audit v1 completed: input_dimension=6, candidate_dimension=1, retained_energy={retained:.12g}, spectral_radius={rho:.12g}.')
