#!/usr/bin/env python3
"""Exact and numerical dimension diagnostics for Phase V stability trajectories."""
import hashlib, json, math, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_stability_trajectory_compression_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_stability_trajectory_compression_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw)
assert d['status']=='STABILITY_TRAJECTORY_COMPRESSION_COMPLETE'
Z=[r['trajectory'] for r in d['classes']]
assert len(Z)==55 and all(len(r)==8 and all(math.isfinite(float(x)) for x in r) for r in Z)
# Gram matrix and deterministic Jacobi eigenvalue iteration for singular-value diagnostics.
A=[[sum(Z[k][i]*Z[k][j] for k in range(len(Z))) for j in range(8)] for i in range(8)]
for _ in range(8*8*100):
 p,q=max(((i,j) for i in range(8) for j in range(i+1,8)),key=lambda ij:abs(A[ij[0]][ij[1]]))
 if abs(A[p][q])<1e-12: break
 phi=0.5*math.atan2(2*A[p][q],A[q][q]-A[p][p]); c=math.cos(phi); s=math.sin(phi)
 app,aqq=A[p][p],A[q][q]
 for k in range(8):
  if k not in (p,q):
   aik,aqk=A[k][p],A[k][q]; A[k][p]=A[p][k]=c*aik-s*aqk; A[k][q]=A[q][k]=s*aik+c*aqk
 A[p][p]=c*c*app-2*s*c*A[p][q]+s*s*aqq; A[q][q]=s*s*app+2*s*c*A[p][q]+c*c*aqq; A[p][q]=A[q][p]=0.0
sv=sorted([math.sqrt(max(0.0,A[i][i])) for i in range(8)],reverse=True)
scale=sv[0] if sv and sv[0]>0 else 1.0
exact_rank=sum(x>0.0 for x in sv)
# Diagnostics only: report relative spectrum and common machine-scale numerical ranks; no one cutoff is declared intrinsic truth.
tolerances=[1e-6,1e-8,1e-10,1e-12]
ranks={str(t):sum(x/scale>t for x in sv) for t in tolerances}
out={'status':'INTRINSIC_DIMENSION_AUDIT_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features':55,'trajectory_dimension':8,'singular_values':sv,'relative_singular_values':[x/scale for x in sv],'positive_singular_value_count':exact_rank,'numerical_rank_by_relative_tolerance':ranks,'interpretation':'diagnostic_spectrum_no_single_intrinsic_dimension_declared'}
OUT=ROOT/'results'/'phase_v_intrinsic_dimension_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(f"PASS: Phase V intrinsic-dimension audit v1 completed: n_features=55, trajectory_dimension=8, positive_singular_values={exact_rank}.")
