#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_stability_trajectory_compression_v1.json'; AUD=ROOT/'results'/'phase_v_six_mode_reconstruction_v1.json'
for p,r in [(SRC,'run_phase_v_stability_trajectory_compression_v1.py'),(AUD,'run_phase_v_six_mode_reconstruction_v1.py')]:
 if not p.exists(): subprocess.run([sys.executable,str(ROOT/'results'/r)],cwd=ROOT,check=True)
raw=SRC.read_bytes(); araw=AUD.read_bytes(); d=json.loads(raw); Z=[[float(x) for x in c['trajectory']] for c in d['classes']]; n=len(Z); p=len(Z[0]); mu=[sum(r[j] for r in Z)/n for j in range(p)]; X=[[r[j]-mu[j] for j in range(p)] for r in Z]
A=[[sum(r[i]*r[j] for r in X) for j in range(p)] for i in range(p)]; V=[[1.0 if i==j else 0.0 for j in range(p)] for i in range(p)]
for _ in range(p*p*300):
 i,j=max(((a,b) for a in range(p) for b in range(a+1,p)),key=lambda q:(abs(A[q[0]][q[1]]),-q[0],-q[1]))
 if abs(A[i][j])<1e-14: break
 phi=.5*math.atan2(2*A[i][j],A[j][j]-A[i][i]); c=math.cos(phi); s=math.sin(phi); aii,ajj,aij=A[i][i],A[j][j],A[i][j]
 for k in range(p):
  if k not in(i,j):
   aik,ajk=A[k][i],A[k][j]; A[k][i]=A[i][k]=c*aik-s*ajk; A[k][j]=A[j][k]=s*aik+c*ajk
  vik,vjk=V[k][i],V[k][j]; V[k][i]=c*vik-s*vjk; V[k][j]=s*vik+c*vjk
 A[i][i]=c*c*aii-2*s*c*aij+s*s*ajj; A[j][j]=s*s*aii+2*s*c*aij+c*c*ajj; A[i][j]=A[j][i]=0
pairs=sorted([(max(0,A[i][i]),[V[j][i] for j in range(p)]) for i in range(p)],reverse=True,key=lambda x:x[0]); vals=[x[0] for x in pairs[:6]]; Q=[x[1] for x in pairs[:6]]
# Canonical sign: largest-magnitude loading positive; ties resolved by lowest index.
for q in Q:
 k=max(range(p),key=lambda j:(abs(q[j]),-j))
 if q[k]<0: q[:]=[-x for x in q]
Y=[[sum(row[j]*q[j] for j in range(p)) for q in Q] for row in X]
R=[[X[i][j]-sum(Y[i][k]*Q[k][j] for k in range(6)) for j in range(p)] for i in range(n)]
rf=math.sqrt(sum(x*x for r in R for x in r)); mr=max(abs(x) for r in R for x in r)
features=[]
for i,c0 in enumerate(d['classes']): features.append({'feature_index':i,'representative':c0.get('representative',i),'six_mode_coordinates':Y[i]})
out={'status':'CANONICAL_SIX_MODE_COORDINATES_COMPLETE','trajectory_source_path':str(SRC.relative_to(ROOT)),'trajectory_source_sha256':hashlib.sha256(raw).hexdigest(),'reconstruction_audit_path':str(AUD.relative_to(ROOT)),'reconstruction_audit_sha256':hashlib.sha256(araw).hexdigest(),'n_features':n,'original_dimension':p,'reduced_dimension':6,'column_means':mu,'eigenvalues':vals,'canonical_basis_rows':Q,'features':features,'reconstruction_residual_frobenius_norm':rf,'reconstruction_max_abs_coordinate_residual':mr,'sign_convention':'largest_absolute_loading_positive_lowest_index_tie_break','interpretation':'canonical_provenance_bound_six_mode_coordinates'}
OUT=ROOT/'results'/'phase_v_canonical_six_mode_coordinates_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print(f'PASS: Phase V canonical six-mode coordinates v1 completed: n_features={n}, reduced_dimension=6, residual_frobenius={rf:.12g}.')
