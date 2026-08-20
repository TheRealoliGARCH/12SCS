#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_residual_spectral_compression_audit_v1.json'
BASE=ROOT/'results'/'phase_v_two_mode_reconstruction_audit_v1.json'
for p,s in [(SRC,'run_phase_v_residual_spectral_compression_audit_v1.py'),(BASE,'run_phase_v_two_mode_reconstruction_audit_v1.py')]:
 if not p.exists(): subprocess.run([sys.executable,str(ROOT/'results'/s)],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw); eig=[float(x) for x in d['residual_eigenvalues'][:4]]; total=sum(eig); assert d['positive_residual_eigenvalues']==4 and total>0
frontier=[]
for k in [3,2,1]:
 retained=sum(eig[:k])/total; residual=1-retained
 frontier.append({'residual_dimension':k,'retained_residual_energy':retained,'discarded_residual_energy':residual,'relative_frobenius_distortion':math.sqrt(residual),'cumulative_total_energy_retained':None})
base=json.loads(BASE.read_text()); dominant=float(base['retained_energy']); residual_total=float(base['residual_energy'])
for x in frontier: x['cumulative_total_energy_retained']=dominant+residual_total*x['retained_residual_energy']
out={'status':'RESIDUAL_RATE_DISTORTION_FRONTIER_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'two_mode_source_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'residual_source_rank':4,'candidate_dimensions':[3,2,1],'frontier':frontier,'interpretation':'conditional_residual_rate_distortion_frontier_relative_to_two_mode_baseline_no_automatic_dimension_selection'}
OUT=ROOT/'results'/'phase_v_residual_rate_distortion_frontier_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print('PASS: Phase V residual rate-distortion frontier v1 completed: residual_source_rank=4, candidate_dimensions=3,2,1.')
