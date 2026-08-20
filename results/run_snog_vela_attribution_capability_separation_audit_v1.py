#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data'/'snog_vela_attribution_capability_evidence_v1.json'; raw=SRC.read_bytes(); d=json.loads(raw)
assert d['event']=='VELA_INCIDENT_1979'
for r in d['source_records']:
 assert not r['counts_as_nuclear_origin_proof'] and not r['counts_as_attribution_proof']
origin=len(d['nuclear_origin_evidence']); attribution=len(d['attribution_evidence']); candidates=len(d['candidate_entities'])
if origin==0: origin_status='NUCLEAR_ORIGIN_UNRESOLVED'
elif origin>=2: origin_status='NUCLEAR_ORIGIN_CORROBORATED'
else: origin_status='NUCLEAR_ORIGIN_INSUFFICIENTLY_CORROBORATED'
if attribution==0: attribution_status='ATTRIBUTION_UNRESOLVED'
elif attribution>=2: attribution_status='ATTRIBUTION_CORROBORATED'
else: attribution_status='ATTRIBUTION_INSUFFICIENTLY_CORROBORATED'
recognition='NO_CAPABILITY_RECOGNITION_FROM_VELA_RECORD'
if origin_status=='NUCLEAR_ORIGIN_CORROBORATED' and attribution_status=='ATTRIBUTION_CORROBORATED' and candidates==1: recognition='CAPABILITY_CANDIDATE_REQUIRES_SEPARATE_RECOGNITION_RULE'
out={'event':d['event'],'source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'origin_evidence_count':origin,'attribution_evidence_count':attribution,'candidate_entity_count':candidates,'nuclear_origin_status':origin_status,'attribution_status':attribution_status,'recognition_status':recognition,'separation_rule':'NUCLEAR_ORIGIN_EVIDENCE_DOES_NOT_IMPLY_ATTRIBUTION_AND_ATTRIBUTION_EVIDENCE_DOES_NOT_IMPLY_NUCLEAR_ORIGIN'}
OUT=ROOT/'results'/'snog_vela_attribution_capability_separation_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(f"PASS: SNoG Vela attribution and capability separation audit v1 completed: nuclear_origin_status={origin_status}, attribution_status={attribution_status}, candidate_entities={candidates}.")
