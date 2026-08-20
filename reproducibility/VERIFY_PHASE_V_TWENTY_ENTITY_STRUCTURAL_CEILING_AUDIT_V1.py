#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_feature_generator_reconstruction_audit_v1.json'; OUT=ROOT/'results'/'phase_v_twenty_entity_structural_ceiling_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_twenty_entity_structural_ceiling_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); s=json.loads(SRC.read_text()); rows=d['candidate_assessment']
assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['target_feature_width']==55 and d['structural_ceiling']==20
assert d['input_strong_candidate_count']==s['strong_candidate_count']==len(s['strong_generator_candidates'])==len(rows)
assert len({r['path'] for r in rows})==len(rows)
construct=refs=0
for r,x in zip(rows,s['strong_generator_candidates']):
 p=ROOT/r['path']; assert r['path']==x['path'] and p.exists(); assert r['sha256']==hashlib.sha256(p.read_bytes()).hexdigest(); assert r['classification'] in {'TWENTY_ENTITY_CONSTRUCTION_CANDIDATE','TWENTY_ENTITY_REFERENCE_ONLY','NO_TWENTY_ENTITY_EVIDENCE'}
 if r['classification']=='TWENTY_ENTITY_CONSTRUCTION_CANDIDATE': construct+=1; assert r['entity_markers'] and r['construction_calls']
 if r['classification']=='TWENTY_ENTITY_REFERENCE_ONLY': refs+=1; assert r['entity_markers'] and not r['construction_calls']
assert d['construction_candidate_count']==construct and d['reference_only_count']==refs
assert d['status'] in {'TWENTY_ENTITY_CONSTRUCTION_CANDIDATES_FOUND','TWENTY_ENTITY_REFERENCES_FOUND','TWENTY_ENTITY_CORRESPONDENCE_NOT_IDENTIFIABLE'}
print('PASS: Phase V twenty-entity structural ceiling audit v1 provenance, membership, ceiling, classification, and non-imputation invariants verified.')
