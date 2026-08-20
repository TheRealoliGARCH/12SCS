#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_feature_generator_reconstruction_audit_v1.json'; OUT=ROOT/'results'/'phase_v_strong_generator_candidate_ranking_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_strong_generator_candidate_ranking_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); s=json.loads(SRC.read_text()); rows=d['ranking']
assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['input_strong_candidate_count']==s['strong_generator_candidate_count']==len(s['strong_generator_candidates'])==d['ranked_candidate_count']==len(rows)
seen=set(); prev=None
for r in rows:
 p=r['path']; assert p not in seen; seen.add(p); q=ROOT/p; assert q.exists(); assert r['sha256']==hashlib.sha256(q.read_bytes()).hexdigest(); assert r['evidence_score']==3*r['width_evidence_count']+r['construction_evidence_count']
 key=(-r['evidence_score'],r['path']); assert prev is None or prev<=key; prev=key
assert d['selection_rule']=='score=3*width_evidence_count+construction_evidence_count; ties sorted lexicographically by path'
assert d['scope']=='ranks_only_verified_upstream_strong_candidates_and_does_not_claim_that_rank_implies_actual_generator_identity'
print('PASS: Phase V strong generator candidate ranking audit v1 provenance, membership, checksum, score, ordering, and non-identification invariants verified.')
