#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_residual_rate_distortion_frontier_v1.json'; OUT=ROOT/'results'/'phase_v_residual_marginal_loss_spectrum_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_residual_rate_distortion_frontier_v1.py')],cwd=ROOT,check=True)
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_residual_marginal_loss_spectrum_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); assert d['status']=='RESIDUAL_MARGINAL_LOSS_SPECTRUM_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['residual_source_rank']==4
S=d['marginal_loss_spectrum']; assert [x['transition'] for x in S]==['4->3','3->2','2->1']; losses=[]
for x in S:
 for k in ['marginal_retained_residual_energy_loss','retained_residual_energy_before','retained_residual_energy_after','frontier_identity_error']: assert math.isfinite(x[k]) and x[k]>=0
 assert x['frontier_identity_error']<1e-15; losses.append(x['marginal_retained_residual_energy_loss'])
G=d['adjacent_marginal_loss_gaps']; assert len(G)==2 and all(math.isfinite(x) and x>=0 for x in G); assert abs(max(G)-d['largest_gap'])<1e-15
idx=min(i for i,x in enumerate(G) if x==max(G)); assert d['largest_gap_after_transition']==S[idx]['transition']; assert d['candidate_residual_dimension_after_gap']==S[idx+1]['removed_residual_mode']; assert 1<=d['candidate_residual_dimension_after_gap']<=3
assert d['selection_rule']=='largest_adjacent_marginal_loss_gap_with_lowest_index_tie_break'; assert d['interpretation']=='structural_gap_candidate_only_no_automatic_secondary_dimension_selection'
print('PASS: Phase V residual marginal-loss spectrum v1 provenance, frontier identity, gap, and candidate-selection invariants verified.')
