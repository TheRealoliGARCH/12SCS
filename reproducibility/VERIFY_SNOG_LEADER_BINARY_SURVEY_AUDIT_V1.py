#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'data'/'snog_leader_binary_survey_v1.json'; OUT=ROOT/'results'/'snog_leader_binary_survey_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_snog_leader_binary_survey_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); s=json.loads(SRC.read_text()); R=d['records']; allowed=set(s['allowed_classifications'])
assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['state_count']==9==len(R); assert d['question']==s['question']; assert all(x['classification'] in allowed for x in R)
counts={k:sum(x['classification']==k for x in R) for k in allowed}; assert d['classification_counts']==counts
assert d['status'] in {'LEADER_BINARY_SURVEY_INCOMPLETE','LEADER_BINARY_SURVEY_COMPLETE'}
for x in R:
 if x['classification'] in {'YES','NO','AMBIGUOUS'}: assert x['speaker'] and x['source'] and x['source_url']
 if x['classification']=='NO_PUBLIC_DETERMINATION_LOCATED': assert x['speaker'] is None and x['source'] is None and x['source_url'] is None
print('PASS: SNoG leader binary survey audit v1 provenance, coverage, classification, source-presence, silence, and non-inference invariants verified.')
