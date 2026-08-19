#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_canonical_six_mode_coordinates_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_canonical_six_mode_coordinates_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw); Y=[f['six_mode_coordinates'] for f in d['features']]; n=len(Y); p=6
mu=[sum(r[j] for r in Y)/n for j in range(p)]; X=[[r[j]-mu[j] for j in range(p)] for r in Y]
C=[[sum(r[i]*r[j] for r in X) for j in range(p)] for i in range(p)]; A=[r[:] for r in C]; V=[[1.0 if i==j else 0.0 for j in range(p)] for i in range(p)]
for _ in range(p*p*300):
 i,j=max(((a,b) for a in range(p) for b in range(a+1,p)),key=lambda q:(abs(A[q[0]][q[1]]),-q[0],-q[1]))
 if abs(A[i][j])<1e-14: break
 phi=.5*math.atan2(2*A[i][j],A[j][j]-A[i][i]); c=math.cos(phi); s=math.sin(phi); aii,ajj,aij=A[i][i],A[j][j],A[i][j]
 for h in range(p):
  if h not in(i,j):
   aik,ajk=A[h][i],A[h][j]; A[h][i]=A[i][h]=c*aik-s*ajk; A[h][j]=A[j][h]=s*aik+c*ajk
  vik,vjk=V[h][i],V[h][j]; V[h][i]=c*vik-s*vjk; V[h][j]=s*vik+c*vjk
 A[i][i]=c*c*aii-2*s*c*aij+s*s*ajj; A[j][j]=s*s*aii+2*s*c*aij+c*c*ajj; A[i][j]=A[j][i]=0
pairs=sorted([(max(0,A[i][i]),[V[j][i] for j in range(p)]) for i in range(p)],reverse=True,key=lambda z:z[0]); lam=[z[0] for z in pairs]; Q=[z[1] for z in pairs]; total=sum(lam)
front=[]
for k in [5,4,3,2,1]:
 R=[]
 for i in range(n):
  row=[]
  for l in range(p):
   row.append(sum(sum(X[i][j]*Q[m][j] for j in range(p))*Q[m][l] for m in range(k)))
  R.append(row)
 D=[[X[i][j]-R[i][j] for j in range(p)] for i in range(n)]
 front.append({'dimension':k,'retained_energy':sum(lam[:k])/total if total else 0.0,'residual_energy':sum(lam[k:])/total if total else 0.0,'residual_frobenius_norm':math.sqrt(sum(x*x for r in D for x in r)),'max_abs_coordinate_distortion':max(abs(x) for r in D for x in r)})
out={'status':'RATE_DISTORTION_FRONTIER_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features':n,'source_dimension':6,'eigenvalues':lam,'frontier':front,'interpretation':'deterministic_pca_reconstruction_frontier_no_loss_threshold_or_canonical_dimension_selection'}
OUT=ROOT/'results'/'phase_v_rate_distortion_frontier_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print('PASS: Phase V rate-distortion frontier v1 completed: source_dimension=6, candidate_dimensions=5,4,3,2,1.')
