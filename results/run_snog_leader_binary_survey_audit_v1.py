#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'data'/'snog_leader_binary_survey_v1.json'; raw=SRC.read_bytes(); d=json.loads(raw)
allowed=set(d['allowed_classifications']); R=d['records']; states=['United States','Russia','United Kingdom','France','China','India','Pakistan','North Korea','Israel']
assert d['question']=='Does Israel have nuclear weapons? Yes or No?'; assert sorted(x['state'] for x in R)==sorted(states); assert len(R)==9
counts={k:sum(x['classification']==k for x in R) for k in sorted(allowed)}
for x in R:
 assert x['classification'] in allowed
 if x['classification'] in {'YES','NO','AMBIGUOUS'}: assert x['speaker'] and x['source'] and x['source_url']
 if x['classification']=='NO_PUBLIC_DETERMINATION_LOCATED': assert x['speaker'] is None and x['source'] is None
status='LEADER_BINARY_SURVEY_INCOMPLETE' if counts['NO_PUBLIC_DETERMINATION_LOCATED'] else 'LEADER_BINARY_SURVEY_COMPLETE'
out={'status':status,'question':d['question'],'source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'state_count':9,'classification_counts':counts,'records':R,'interpretation':'No classification is inferred from silence, institutional assessments, or third-party commentary.'}
OUT=ROOT/'results'/'snog_leader_binary_survey_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(f"PASS: SNoG leader binary survey audit v1 completed: status={status}, YES={counts['YES']}, NO={counts['NO']}, AMBIGUOUS={counts['AMBIGUOUS']}, unresolved={counts['NO_PUBLIC_DETERMINATION_LOCATED']}.")
