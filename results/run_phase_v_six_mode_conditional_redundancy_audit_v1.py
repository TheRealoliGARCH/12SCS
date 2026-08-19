#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_canonical_six_mode_coordinates_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_canonical_six_mode_coordinates_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw); Y=[f['six_mode_coordinates'] for f in d['features']]; n=len(Y); p=6
assert n==55 and all(len(r)==p for r in Y)
mu=[sum(r[j] for r in Y)/n for j in range(p)]; X=[[r[j]-mu[j] for j in range(p)] for r in Y]
C=[[sum(r[i]*r[j] for r in X) for j in range(p)] for i in range(p)]
# Exact numerical rank diagnostic via deterministic Jacobi spectrum of covariance Gram.
A=[row[:] for row in C]
for _ in range(p*p*300):
 i,j=max(((a,b) for a in range(p) for b in range(a+1,p)),key=lambda q:(abs(A[q[0]][q[1]]),-q[0],-q[1]))
 if abs(A[i][j])<1e-14: break
 phi=.5*math.atan2(2*A[i][j],A[j][j]-A[i][i]); c=math.cos(phi); s=math.sin(phi); aii,ajj,aij=A[i][i],A[j][j],A[i][j]
 for k in range(p):
  if k not in(i,j):
   aik,ajk=A[k][i],A[k][j]; A[k][i]=A[i][k]=c*aik-s*ajk; A[k][j]=A[j][k]=s*aik+c*ajk
 A[i][i]=c*c*aii-2*s*c*aij+s*s*ajj; A[j][j]=s*s*aii+2*s*c*aij+c*c*ajj; A[i][j]=A[j][i]=0
lam=sorted([max(0,A[i][i]) for i in range(p)],reverse=True); rank=sum(x>0 for x in lam)
# Deterministic Gauss-Jordan inverse; unresolved singularity is reported, never regularized.
M=[C[i][:]+[1.0 if i==j else 0.0 for j in range(p)] for i in range(p)]; invertible=True
for col in range(p):
 pivot=max(range(col,p),key=lambda r:abs(M[r][col]))
 if abs(M[pivot][col])<1e-14: invertible=False; break
 M[col],M[pivot]=M[pivot],M[col]; q=M[col][col]; M[col]=[x/q for x in M[col]]
 for r in range(p):
  if r!=col:
   q=M[r][col]; M[r]=[M[r][k]-q*M[col][k] for k in range(2*p)]
Omega=[r[p:] for r in M] if invertible else None
partial=None
if Omega is not None:
 partial=[[1.0 if i==j else -Omega[i][j]/math.sqrt(Omega[i][i]*Omega[j][j]) for j in range(p)] for i in range(p)]
out={'status':'SIX_MODE_CONDITIONAL_REDUNDANCY_AUDIT_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features':n,'mode_dimension':p,'centered_gram_eigenvalues':lam,'positive_eigenvalue_count':rank,'gram_invertible':invertible,'partial_correlation_matrix':partial,'interpretation':'conditional_redundancy_diagnostic_no_automatic_dimension_reduction'}
OUT=ROOT/'results'/'phase_v_six_mode_conditional_redundancy_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print(f'PASS: Phase V six-mode conditional redundancy audit v1 completed: mode_dimension=6, positive_eigenvalues={rank}, gram_invertible={invertible}.')
