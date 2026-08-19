#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_canonical_six_mode_coordinates_v1.json'
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
pairs=sorted([(max(0,A[i][i]),[V[j][i] for j in range(p)]) for i in range(p)],reverse=True,key=lambda z:z[0]); lam=[z[0] for z in pairs]; Q=[z[1] for z in pairs]
# Residual after orthogonal projection onto the leading two modes.
R=[[X[i][l]-sum(sum(X[i][j]*Q[m][j] for j in range(p))*Q[m][l] for m in range(2)) for l in range(p)] for i in range(n)]
Cr=[[sum(r[i]*r[j] for r in R) for j in range(p)] for i in range(p)]; B=[r[:] for r in Cr]; W=[[1.0 if i==j else 0.0 for j in range(p)] for i in range(p)]
for _ in range(p*p*300):
 i,j=max(((a,b) for a in range(p) for b in range(a+1,p)),key=lambda q:(abs(B[q[0]][q[1]]),-q[0],-q[1]))
 if abs(B[i][j])<1e-14: break
 phi=.5*math.atan2(2*B[i][j],B[j][j]-B[i][i]); c=math.cos(phi); s=math.sin(phi); bii,bjj,bij=B[i][i],B[j][j],B[i][j]
 for h in range(p):
  if h not in(i,j):
   bik,bjk=B[h][i],B[h][j]; B[h][i]=B[i][h]=c*bik-s*bjk; B[h][j]=B[j][h]=s*bik+c*bjk
  wik,wjk=W[h][i],W[h][j]; W[h][i]=c*wik-s*wjk; W[h][j]=s*wik+c*wjk
 B[i][i]=c*c*bii-2*s*c*bij+s*s*bjj; B[j][j]=s*s*bii+2*s*c*bij+c*c*bjj; B[i][j]=B[j][i]=0
res=sorted([max(0,B[i][i]) for i in range(p)],reverse=True); total=sum(res); positive=sum(x>1e-14 for x in res)
out={'status':'RESIDUAL_SPECTRAL_COMPRESSION_AUDIT_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features':n,'ambient_dimension':p,'dominant_projection_dimension':2,'residual_eigenvalues':res,'positive_residual_eigenvalues':positive,'residual_spectral_energy_shares':[x/total if total else 0.0 for x in res],'residual_cumulative_energy_shares':[sum(res[:k])/total if total else 0.0 for k in range(1,p+1)],'interpretation':'orthogonal_two_mode_residual_spectrum_descriptive_only_no_automatic_secondary_dimension_selection'}
OUT=ROOT/'results'/'phase_v_residual_spectral_compression_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print(f'PASS: Phase V residual spectral compression audit v1 completed: positive_residual_eigenvalues={positive}, residual_rank_upper_bound=4.')
