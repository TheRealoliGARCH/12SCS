#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_residual_rate_distortion_frontier_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_residual_rate_distortion_frontier_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw); F={x['residual_dimension']:x for x in d['frontier']}; assert d['residual_source_rank']==4 and sorted(F)==[1,2,3]
# Marginal loss when reducing the residual representation by one dimension.
spectrum=[]
for hi,lo in [(4,3),(3,2),(2,1)]:
 before=1.0 if hi==4 else F[hi]['retained_residual_energy']
 after=F[lo]['retained_residual_energy']
 loss=before-after
 spectrum.append({'transition':f'{hi}->{lo}','removed_residual_mode':hi,'marginal_retained_residual_energy_loss':loss,'retained_residual_energy_before':before,'retained_residual_energy_after':after,'frontier_identity_error':abs((before-after)-loss)})
losses=[x['marginal_retained_residual_energy_loss'] for x in spectrum]; gaps=[abs(losses[i]-losses[i+1]) for i in range(len(losses)-1)]
idx=min(i for i,g in enumerate(gaps) if g==max(gaps)); candidate=spectrum[idx+1]['removed_residual_mode']
out={'status':'RESIDUAL_MARGINAL_LOSS_SPECTRUM_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'residual_source_rank':4,'marginal_loss_spectrum':spectrum,'adjacent_marginal_loss_gaps':gaps,'largest_gap':max(gaps),'largest_gap_after_transition':spectrum[idx]['transition'],'candidate_residual_dimension_after_gap':candidate,'selection_rule':'largest_adjacent_marginal_loss_gap_with_lowest_index_tie_break','interpretation':'structural_gap_candidate_only_no_automatic_secondary_dimension_selection'}
OUT=ROOT/'results'/'phase_v_residual_marginal_loss_spectrum_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print(f'PASS: Phase V residual marginal-loss spectrum v1 completed: transitions=3, candidate_residual_dimension_after_gap={candidate}.')
