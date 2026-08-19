#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_rate_distortion_frontier_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_rate_distortion_frontier_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw); F={x['dimension']:x for x in d['frontier']}; eig=d['eigenvalues']; assert d['source_dimension']==6 and sorted(F)==[1,2,3,4,5]
# Removing mode k from a k-mode reconstruction adds exactly lambda_k / sum(lambda).
total=sum(eig); spectrum=[]
for k in [6,5,4,3,2]:
 loss=(eig[k-1]/total) if total else 0.0
 before=1.0 if k==6 else F[k]['retained_energy']; after=F[k-1]['retained_energy']
 spectrum.append({'transition':f'{k}->{k-1}','removed_mode':k,'marginal_retained_energy_loss':loss,'retained_energy_before':before,'retained_energy_after':after,'frontier_identity_error':abs((before-after)-loss)})
losses=[x['marginal_retained_energy_loss'] for x in spectrum]; max_gap=max(abs(losses[i]-losses[i+1]) for i in range(len(losses)-1))
gaps=[abs(losses[i]-losses[i+1]) for i in range(len(losses)-1)]; idx=min(i for i,g in enumerate(gaps) if g==max_gap); candidate=spectrum[idx+1]['removed_mode']
out={'status':'MARGINAL_LOSS_SPECTRUM_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'source_dimension':6,'marginal_loss_spectrum':spectrum,'adjacent_marginal_loss_gaps':gaps,'largest_gap':max_gap,'largest_gap_after_transition':spectrum[idx]['transition'],'candidate_dimension_after_gap':candidate,'selection_rule':'largest_adjacent_marginal_loss_gap_with_lowest_index_tie_break','interpretation':'structural_gap_candidate_only_no_automatic_canonical_dimension_selection'}
OUT=ROOT/'results'/'phase_v_marginal_loss_spectrum_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print(f'PASS: Phase V marginal-loss spectrum v1 completed: transitions=5, candidate_dimension_after_gap={candidate}.')
