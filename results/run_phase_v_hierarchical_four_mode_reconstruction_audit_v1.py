#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CAN=ROOT/'results'/'phase_v_canonical_six_mode_coordinates_v1.json'; TWO=ROOT/'results'/'phase_v_two_mode_reconstruction_audit_v1.json'; RES=ROOT/'results'/'phase_v_residual_rate_distortion_frontier_v1.json'
for p,s in [(CAN,'run_phase_v_canonical_six_mode_coordinates_v1.py'),(TWO,'run_phase_v_two_mode_reconstruction_audit_v1.py'),(RES,'run_phase_v_residual_rate_distortion_frontier_v1.py')]:
 if not p.exists(): subprocess.run([sys.executable,str(ROOT/'results'/s)],cwd=ROOT,check=True)
raw=CAN.read_bytes(); traw=TWO.read_bytes(); rraw=RES.read_bytes(); d=json.loads(raw); Y=[[float(x) for x in f['six_mode_coordinates']] for f in d['features']]; n=len(Y); p=6; assert n==55
mu=[sum(r[j] for r in Y)/n for j in range(p)]; X=[[r[j]-mu[j] for j in range(p)] for r in Y]
A=[[sum(r[i]*r[j] for r in X) for j in range(p)] for i in range(p)]; V=[[1.0 if i==j else 0.0 for j in range(p)] for i in range(p)]
for _ in range(p*p*300):
 i,j=max(((a,b) for a in range(p) for b in range(a+1,p)),key=lambda q:(abs(A[q[0]][q[1]]),-q[0],-q[1]))
 if abs(A[i][j])<1e-14: break
 phi=.5*math.atan2(2*A[i][j],A[j][j]-A[i][i]); c=math.cos(phi); s=math.sin(phi); aii,ajj,aij=A[i][i],A[j][j],A[i][j]
 for h in range(p):
  if h not in(i,j):
   aik,ajk=A[h][i],A[h][j]; A[h][i]=A[i][h]=c*aik-s*ajk; A[h][j]=A[j][h]=s*aik+c*ajk
  vik,vjk=V[h][i],V[h][j]; V[h][i]=c*vik-s*vjk; V[h][j]=s*vik+c*vjk
 A[i][i]=c*c*aii-2*s*c*aij+s*s*ajj; A[j][j]=s*s*aii+2*s*c*aij+c*c*ajj; A[i][j]=A[j][i]=0
pairs=sorted([(max(0,A[i][i]),[V[j][i] for j in range(p)]) for i in range(p)],reverse=True,key=lambda z:z[0]); Q=[z[1] for z in pairs]
H=[[sum(sum(X[i][j]*Q[m][j] for j in range(p))*Q[m][l] for m in range(4)) for l in range(p)] for i in range(n)]
E=[[X[i][j]-H[i][j] for j in range(p)] for i in range(n)]; ss=sum(x*x for r in X for x in r); ee=sum(x*x for r in E for x in r); retained=1-ee/ss if ss else 1.0; residual=ee/ss if ss else 0.0; rf=math.sqrt(ee); ma=max(abs(x) for r in E for x in r); per=[math.sqrt(sum(x*x for x in r)) for r in E]
rd=json.loads(rraw); f2=next(x for x in rd['frontier'] if x['residual_dimension']==2); td=json.loads(traw)
out={'status':'HIERARCHICAL_FOUR_MODE_RECONSTRUCTION_AUDIT_COMPLETE','canonical_source_sha256':hashlib.sha256(raw).hexdigest(),'two_mode_source_sha256':hashlib.sha256(traw).hexdigest(),'residual_frontier_source_sha256':hashlib.sha256(rraw).hexdigest(),'n_features':n,'source_dimension':6,'dominant_dimension':2,'residual_correction_dimension':2,'combined_dimension':4,'retained_energy':retained,'residual_energy':residual,'residual_frobenius_norm':rf,'max_abs_coordinate_distortion':ma,'per_feature_residual_norms':per,'max_feature_residual_norm':max(per),'frontier_cumulative_total_energy_retained':float(f2['cumulative_total_energy_retained']),'frontier_consistency_error':abs(retained-float(f2['cumulative_total_energy_retained'])),'dominant_two_mode_retained_energy':float(td['retained_energy']),'residual_correction_retained_energy':float(f2['retained_residual_energy']),'interpretation':'hierarchical_two_plus_two_mode_approximation_audit_no_automatic_canonical_dimension_redefinition'}
OUT=ROOT/'results'/'phase_v_hierarchical_four_mode_reconstruction_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print(f'PASS: Phase V hierarchical four-mode reconstruction audit v1 completed: n_features={n}, combined_dimension=4, retained_energy={retained:.12g}.')
