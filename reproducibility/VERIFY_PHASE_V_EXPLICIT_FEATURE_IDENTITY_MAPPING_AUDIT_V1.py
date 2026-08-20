#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_feature_construction_backtrace_audit_v1.json'; OUT=ROOT/'results'/'phase_v_explicit_feature_identity_mapping_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_explicit_feature_identity_mapping_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); s=json.loads(SRC.read_text())
assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_features']==55
assert d['identity_candidate_count']==s['identity_candidate_count']==len(d['candidate_reports'])
assert d['status'] in {'FEATURE_IDENTITY_MAPPING_FULL','FEATURE_IDENTITY_MAPPING_PARTIAL','FEATURE_IDENTITY_MAPPING_CONFLICT','FEATURE_IDENTITY_MAPPING_NOT_FOUND'}
seen={}
for r in d['mapping_rows']:
 assert 0<=r['feature_index']<55 and isinstance(r['source_variable'],str) and r['source_variable']
 seen.setdefault(r['feature_index'],set()).add(r['source_variable'])
assert d['mapped_feature_indices']==sorted(seen)
assert d['mapped_feature_count']==len(seen)
assert d['conflicting_feature_indices']==sorted(k for k,v in seen.items() if len(v)>1)
if d['status']=='FEATURE_IDENTITY_MAPPING_FULL': assert d['mapped_feature_count']==55 and not d['conflicting_feature_indices']
if d['status']=='FEATURE_IDENTITY_MAPPING_PARTIAL': assert 0<d['mapped_feature_count']<55 and not d['conflicting_feature_indices']
if d['status']=='FEATURE_IDENTITY_MAPPING_NOT_FOUND': assert d['mapped_feature_count']==0 and not d['conflicting_feature_indices']
for r in d['candidate_reports']:
 p=ROOT/r['path']; assert p.exists(); assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']; assert r['explicit_pairs']>=0
print('PASS: Phase V explicit feature identity mapping audit v1 provenance, explicit-pair, coverage, conflict, and non-imputation invariants verified.')
