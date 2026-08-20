#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'data'/'snog_ninth_capability_evidence_manifest_v1.json'; OUT=ROOT/'results'/'snog_ninth_capability_recognition_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_snog_ninth_capability_recognition_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); s=json.loads(SRC.read_text()); rule=s['recognition_rule']
assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['current_operational_member_count']==8 and d['target_member_count']==9
assert d['candidate_count']==len(d['candidates']); recognized=0
for r,c in zip(d['candidates'],s['candidates']):
 assert r['candidate']==c['candidate']; ev=c['evidence']; groups={e['source_group'] for e in ev}; classes={e['evidence_class'] for e in ev}
 expected=bool(c.get('public_pre_existing_only',False)) and set(rule['required_evidence_classes']).issubset(classes) and len(groups)>=rule['minimum_independent_sources']
 assert (r['verdict']=='RECOGNIZED_FOR_SNO_G_CAPABILITY_PURPOSES')==expected
 recognized+=expected
assert d['recognized_candidate_count']==recognized
assert d['status'] in {'NINTH_CAPABILITY_RECOGNIZED','MULTIPLE_CANDIDATES_REQUIRE_MODEL_ADJUDICATION','NO_NINTH_CAPABILITY_RECOGNIZED_FROM_MANIFEST'}
assert d['interpretation']=='recognition_is_based_only_on_public_pre_existing_evidence_records_present_in_the_manifest; absence_of_recognition_is_not_evidence_of_absence_of_capability'
print('PASS: SNoG ninth capability recognition audit v1 provenance, independence, threshold, verdict, and non-absence invariants verified.')
