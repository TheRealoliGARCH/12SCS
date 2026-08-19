#!/usr/bin/env python3
"""Centered spectral diagnostics for Phase V stability trajectories."""
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_stability_trajectory_compression_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_stability_trajectory_compression_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw)
assert d['status']=='STABILITY_TRAJECTORY_COMPRESSION_COMPLETE'
Z=[[float(x) for x in r['trajectory']] for r in d['classes']]
n=len(Z); p=len(Z[0]); assert n==55 and p==8 and all(len(r)==p for r in Z)
mu=[sum(r[j] for r in Z)/n for j in range(p)]
X=[[r[j]-mu[j] for j in range(p)] for r in Z]
A=[[sum(r[i]*r[j] for r in X) for j in range(p)] for i in range(p)]
# Deterministic Jacobi eigensolver for symmetric Gram matrix.
for _ in range(p*p*200):
 pairs=[(i,j) for i in range(p) for j in range(i+1,p)]
 q=max(pairs,key=lambda ij:(abs(A[ij[0]][ij[1]]),-ij[0],-ij[1])); i,j=q
 if abs(A[i][j])<1e-12: break
 phi=0.5*math.atan2(2*A[i][j],A[j][j]-A[i][i]); c=math.cos(phi); s=math.sin(phi); aii,ajj,aij=A[i][i],A[j][j],A[i][j]
 for k in range(p):
  if k not in (i,j):
   aik,ajk=A[k][i],A[k][j]; A[k][i]=A[i][k]=c*aik-s*ajk; A[k][j]=A[j][k]=s*aik+c*ajk
 A[i][i]=c*c*aii-2*s*c*aij+s*s*ajj; A[j][j]=s*s*aii+2*s*c*aij+c*c*ajj; A[i][j]=A[j][i]=0.0
lam=sorted([max(0.0,A[i][i]) for i in range(p)],reverse=True)
total=sum(lam); energy=[sum(lam[:k])/total if total>0 else 0.0 for k in range(1,p+1)]
gaps=[(lam[k]/lam[k+1] if lam[k+1]>0 else None) for k in range(p-1)]
max_gap_index=(max(range(p-1),key=lambda k:(gaps[k] if gaps[k] is not None else float('inf'),-k))+1) if p>1 else 1
out={'status':'CENTERED_SPECTRAL_COMPRESSION_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features':n,'trajectory_dimension':p,'column_means':mu,'centered_eigenvalues':lam,'centered_positive_eigenvalue_count':sum(x>0 for x in lam),'cumulative_spectral_energy':energy,'spectral_gaps':gaps,'largest_observed_gap_after_mode':max_gap_index,'interpretation':'spectral_diagnostics_no_automatic_dimension_selection'}
OUT=ROOT/'results'/'phase_v_centered_spectral_compression_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(f"PASS: Phase V centered spectral compression v1 completed: n_features={n}, trajectory_dimension={p}, centered_positive_eigenvalues={out['centered_positive_eigenvalue_count']}, largest_gap_after_mode={max_gap_index}.")
