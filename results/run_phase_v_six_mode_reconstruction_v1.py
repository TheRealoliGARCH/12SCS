#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_stability_trajectory_compression_v1.json'
SPEC=ROOT/'results'/'phase_v_centered_spectral_compression_v1.json'
for path,runner in [(SRC,'run_phase_v_stability_trajectory_compression_v1.py'),(SPEC,'run_phase_v_centered_spectral_compression_v1.py')]:
 if not path.exists(): subprocess.run([sys.executable,str(ROOT/'results'/runner)],cwd=ROOT,check=True)
raw=SRC.read_bytes(); sraw=SPEC.read_bytes(); d=json.loads(raw); sp=json.loads(sraw)
Z=[[float(x) for x in r['trajectory']] for r in d['classes']]; n=len(Z); p=len(Z[0]); mu=[sum(r[j] for r in Z)/n for j in range(p)]; X=[[r[j]-mu[j] for j in range(p)] for r in Z]
A=[[sum(r[i]*r[j] for r in X) for j in range(p)] for i in range(p)]
# Jacobi eigendecomposition with eigenvectors.
V=[[1.0 if i==j else 0.0 for j in range(p)] for i in range(p)]
for _ in range(p*p*300):
 i,j=max(((a,b) for a in range(p) for b in range(a+1,p)),key=lambda q:(abs(A[q[0]][q[1]]),-q[0],-q[1]))
 if abs(A[i][j])<1e-14: break
 phi=0.5*math.atan2(2*A[i][j],A[j][j]-A[i][i]); c=math.cos(phi); s=math.sin(phi); aii,ajj,aij=A[i][i],A[j][j],A[i][j]
 for k in range(p):
  if k not in (i,j):
   aik,ajk=A[k][i],A[k][j]; A[k][i]=A[i][k]=c*aik-s*ajk; A[k][j]=A[j][k]=s*aik+c*ajk
  vik,vjk=V[k][i],V[k][j]; V[k][i]=c*vik-s*vjk; V[k][j]=s*vik+c*vjk
 A[i][i]=c*c*aii-2*s*c*aij+s*s*ajj; A[j][j]=s*s*aii+2*s*c*aij+c*c*ajj; A[i][j]=A[j][i]=0.0
pairs=sorted([(max(0.0,A[i][i]),[V[j][i] for j in range(p)]) for i in range(p)],reverse=True,key=lambda x:x[0])
vals=[x[0] for x in pairs]; Q=[x[1] for x in pairs]
def audit(k):
 qs=Q[:k]; R=[]
 for row in X:
  rec=[sum(sum(row[t]*q[t] for t in range(p))*q[j] for q in qs) for j in range(p)]
  R.extend([row[j]-rec[j] for j in range(p)])
 return {'modes':k,'residual_frobenius_norm':math.sqrt(sum(x*x for x in R)),'max_abs_coordinate_residual':max(abs(x) for x in R),'explained_spectral_energy':sum(vals[:k])/sum(vals) if sum(vals)>0 else 0.0}
audits=[audit(k) for k in (5,6,7)]
out={'status':'SIX_MODE_RECONSTRUCTION_AUDIT_COMPLETE','trajectory_source_path':str(SRC.relative_to(ROOT)),'trajectory_source_sha256':hashlib.sha256(raw).hexdigest(),'spectral_source_path':str(SPEC.relative_to(ROOT)),'spectral_source_sha256':hashlib.sha256(sraw).hexdigest(),'n_features':n,'trajectory_dimension':p,'audits':audits,'six_mode':audits[1],'interpretation':'six_mode_candidate_evaluated_by_direct_reconstruction_residual'}
OUT=ROOT/'results'/'phase_v_six_mode_reconstruction_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
a=audits[1]; print(f"PASS: Phase V six-mode reconstruction audit v1 completed: residual_frobenius={a['residual_frobenius_norm']:.12g}, max_abs_residual={a['max_abs_coordinate_residual']:.12g}, explained_energy={a['explained_spectral_energy']:.12g}.")
