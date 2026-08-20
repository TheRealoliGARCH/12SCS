#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data'/'snog_ninth_capability_evidence_manifest_v1.json'
raw=SRC.read_bytes(); d=json.loads(raw)
assert d['schema_version']=='v1' and d['scope']=='public_pre_existing_evidence_only'
assert d['current_operational_member_count']==8 and d['target_member_count']==9
rule=d['recognition_rule']; assert rule['minimum_independent_sources']>=2
req=set(rule['required_evidence_classes']); assert req=={'capability_assessment','independent_corroboration'}
rows=[]
for c in d['candidates']:
 name=c['candidate']; ev=c['evidence']; ids=[e['source_id'] for e in ev]
 assert len(ids)==len(set(ids))
 classes={e['evidence_class'] for e in ev}; independent={e['source_group'] for e in ev}
 admissible=bool(c.get('public_pre_existing_only',False)) and req.issubset(classes) and len(independent)>=rule['minimum_independent_sources']
 verdict='RECOGNIZED_FOR_SNO_G_CAPABILITY_PURPOSES' if admissible else 'NOT_RECOGNIZED_UNDER_V1_RULE'
 rows.append({'candidate':name,'source_count':len(ev),'independent_source_groups':len(independent),'evidence_classes':sorted(classes),'verdict':verdict})
recognized=[r for r in rows if r['verdict']=='RECOGNIZED_FOR_SNO_G_CAPABILITY_PURPOSES']
if len(recognized)==1: status='NINTH_CAPABILITY_RECOGNIZED'
elif len(recognized)>1: status='MULTIPLE_CANDIDATES_REQUIRE_MODEL_ADJUDICATION'
else: status='NO_NINTH_CAPABILITY_RECOGNIZED_FROM_MANIFEST'
out={'status':status,'source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'current_operational_member_count':8,'target_member_count':9,'candidate_count':len(rows),'recognized_candidate_count':len(recognized),'candidates':rows,'recognition_rule':rule,'interpretation':'recognition_is_based_only_on_public_pre_existing_evidence_records_present_in_the_manifest; absence_of_recognition_is_not_evidence_of_absence_of_capability'}
OUT=ROOT/'results'/'snog_ninth_capability_recognition_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(f'PASS: SNoG ninth capability recognition audit v1 completed: status={status}, candidates={len(rows)}, recognized={len(recognized)}.')
