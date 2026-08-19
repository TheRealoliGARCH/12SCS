#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_canonical_six_mode_coordinates_v1.json'
FRONT=ROOT/'results'/'phase_v_rate_distortion_frontier_v1.json'
for p,s in [(SRC,'run_phase_v_canonical_six_mode_coordinates_v1.py'),(FRONT,'run_phase_v_rate_distortion_frontier_v1.py')]:
 if not p.exists(): subprocess.run([sys.executable,str(ROOT/'results'/s)],cwd=ROOT,check=True)
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
R=[]; residuals=[]
for i in range(n):
 r=[sum(sum(X[i][j]*Q[m][j] for j in range(p))*Q[m][l] for m in range(2)) for l in range(p)]; R.append(r); residuals.append(math.sqrt(sum((X[i][j]-r[j])**2 for j in range(p))))
D=[[X[i][j]-R[i][j] for j in range(p)] for i in range(n)]
out={'status':'TWO_MODE_RECONSTRUCTION_AUDIT_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'frontier_sha256':hashlib.sha256(FRONT.read_bytes()).hexdigest(),'n_features':n,'source_dimension':6,'reduced_dimension':2,'retained_energy':sum(lam[:2])/total if total else 0.0,'residual_energy':sum(lam[2:])/total if total else 0.0,'residual_frobenius_norm':math.sqrt(sum(x*x for r in D for x in r)),'max_abs_coordinate_distortion':max(abs(x) for r in D for x in r),'per_feature_residual_norms':residuals,'max_feature_residual_norm':max(residuals),'interpretation':'two_mode_candidate_reconstruction_audit_no_automatic_canonical_dimension_redefinition'}
OUT=ROOT/'results'/'phase_v_two_mode_reconstruction_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print(f"PASS: Phase V two-mode reconstruction audit v1 completed: n_features={n}, retained_energy={out['retained_energy']:.12g}, residual_energy={out['residual_energy']:.12g}.")
