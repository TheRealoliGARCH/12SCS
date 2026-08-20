#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_feature_generator_reconstruction_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_feature_generator_reconstruction_audit_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw); assert d['target_width']==55
C=d['strong_generator_candidates']; assert len(C)==d['strong_candidate_count']
markers=('nation','nations','country','countries','entity','entities','state','states','20','twenty')
ops=('concatenate','concat','hstack','vstack','stack','column_stack','array','append','extend')
rows=[]
for x in C:
 text=(ROOT/x['path']).read_text(encoding='utf-8',errors='ignore').lower()
 mh=sorted({m for m in markers if m in text}); oh=sorted(set(x.get('construction_calls',[])) & set(ops))
 if mh and oh: cls='TWENTY_ENTITY_CONSTRUCTION_CANDIDATE'
 elif mh: cls='TWENTY_ENTITY_REFERENCE_ONLY'
 else: cls='NO_TWENTY_ENTITY_EVIDENCE'
 rows.append({'path':x['path'],'sha256':x['sha256'],'entity_markers':mh,'construction_calls':oh,'classification':cls})
construct=[r for r in rows if r['classification']=='TWENTY_ENTITY_CONSTRUCTION_CANDIDATE']
refs=[r for r in rows if r['classification']=='TWENTY_ENTITY_REFERENCE_ONLY']
if construct: status='TWENTY_ENTITY_CONSTRUCTION_CANDIDATES_FOUND'
elif refs: status='TWENTY_ENTITY_REFERENCES_FOUND'
else: status='TWENTY_ENTITY_CORRESPONDENCE_NOT_IDENTIFIABLE'
out={'status':status,'source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'target_feature_width':55,'structural_ceiling':20,'input_strong_candidate_count':len(C),'candidate_assessment':rows,'construction_candidate_count':len(construct),'reference_only_count':len(refs),'hypothesis':'tests_for_repository_evidence_linking_the_55_feature_generator_to_a_20_entity_architecture_without_imputing_a_mapping','interpretation':'candidate_or_reference_evidence_does_not_by_itself_establish_that_the_55_features_decompose_over_20_entities'}
OUT=ROOT/'results'/'phase_v_twenty_entity_structural_ceiling_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(f'PASS: Phase V twenty-entity structural ceiling audit v1 completed: status={status}, input_strong_candidates={len(C)}, construction_candidates={len(construct)}, reference_only={len(refs)}.')
