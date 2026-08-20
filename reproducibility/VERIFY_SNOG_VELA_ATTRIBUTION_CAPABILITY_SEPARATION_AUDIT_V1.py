#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'data'/'snog_vela_attribution_capability_evidence_v1.json'; OUT=ROOT/'results'/'snog_vela_attribution_capability_separation_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_snog_vela_attribution_capability_separation_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); s=json.loads(SRC.read_text())
assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['event']==s['event']=='VELA_INCIDENT_1979'
assert d['origin_evidence_count']==len(s['nuclear_origin_evidence']); assert d['attribution_evidence_count']==len(s['attribution_evidence']); assert d['candidate_entity_count']==len(s['candidate_entities'])
assert d['nuclear_origin_status'] in {'NUCLEAR_ORIGIN_UNRESOLVED','NUCLEAR_ORIGIN_CORROBORATED','NUCLEAR_ORIGIN_INSUFFICIENTLY_CORROBORATED'}
assert d['attribution_status'] in {'ATTRIBUTION_UNRESOLVED','ATTRIBUTION_CORROBORATED','ATTRIBUTION_INSUFFICIENTLY_CORROBORATED'}
assert d['recognition_status'] in {'NO_CAPABILITY_RECOGNITION_FROM_VELA_RECORD','CAPABILITY_CANDIDATE_REQUIRES_SEPARATE_RECOGNITION_RULE'}
assert d['separation_rule']=='NUCLEAR_ORIGIN_EVIDENCE_DOES_NOT_IMPLY_ATTRIBUTION_AND_ATTRIBUTION_EVIDENCE_DOES_NOT_IMPLY_NUCLEAR_ORIGIN'
print('PASS: SNoG Vela attribution and capability separation audit v1 provenance, origin-attribution separation, threshold, verdict, and non-imputation invariants verified.')
