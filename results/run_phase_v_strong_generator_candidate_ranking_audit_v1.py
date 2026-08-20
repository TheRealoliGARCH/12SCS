#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_feature_generator_reconstruction_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_feature_generator_reconstruction_audit_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw)
C=d['strong_generator_candidates']; assert len(C)==d['strong_generator_candidate_count']
WIDTH=('55','n_features','shape','dimension','width'); OPS=('concatenate','concat','hstack','vstack','stack','column_stack','append','extend','feature')
def path_of(x): return x if isinstance(x,str) else x['path']
rows=[]
for x in C:
 p=path_of(x); q=ROOT/p; assert q.exists(); b=q.read_bytes(); text=b.decode('utf-8',errors='ignore').lower()
 wh=sum(k in text for k in WIDTH); op=sum(k in text for k in OPS); score=3*wh+op
 rows.append({'path':p,'sha256':hashlib.sha256(b).hexdigest(),'width_evidence_count':wh,'construction_evidence_count':op,'evidence_score':score,'upstream_record':x if isinstance(x,dict) else None})
rows.sort(key=lambda r:(-r['evidence_score'],r['path']))
status='RANKED_STRONG_GENERATOR_CANDIDATES' if rows else 'NO_STRONG_GENERATOR_CANDIDATES'
out={'status':status,'source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'input_strong_candidate_count':len(C),'ranked_candidate_count':len(rows),'ranking':rows,'selection_rule':'score=3*width_evidence_count+construction_evidence_count; ties sorted lexicographically by path','scope':'ranks_only_verified_upstream_strong_candidates_and_does_not_claim_that_rank_implies_actual_generator_identity','next_action':'inspect_highest_ranked_candidates_for_executable_or_explicit_feature_construction_rules'}
OUT=ROOT/'results'/'phase_v_strong_generator_candidate_ranking_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(f'PASS: Phase V strong generator candidate ranking audit v1 completed: input_strong_candidates={len(C)}, ranked_candidates={len(rows)}, top_score={rows[0]["evidence_score"] if rows else 0}.')
