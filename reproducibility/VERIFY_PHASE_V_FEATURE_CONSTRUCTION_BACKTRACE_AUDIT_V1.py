#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_deep_provenance_backtrace_audit_v1.json'; OUT=ROOT/'results'/'phase_v_feature_construction_backtrace_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_feature_construction_backtrace_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); s=json.loads(SRC.read_text())
assert d['status'] in {'FEATURE_CONSTRUCTION_PROVENANCE_CANDIDATES_FOUND','FEATURE_CONSTRUCTION_PROVENANCE_NOT_FOUND'}
assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_features']==s['n_features']==54
assert d['search_scope']==['results','reproducibility','data','src','model','tests']
assert d['excluded_paths']==[str(OUT.relative_to(ROOT))]
for x in d['candidate_files']:
 p=ROOT/x['path']; assert p.exists() and p.resolve()!=OUT.resolve(); assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']; assert x['markers']
assert d['identity_candidate_count']==sum(1 for x in d['candidate_files'] if 'feature_names' in x['markers'] or 'columns' in x['markers'])
assert d['interpretation']=='repository-level textual provenance candidates are inventoried only; semantic identity is not asserted unless an explicit feature-index-to-source-variable mapping is present'
print('PASS: Phase V feature construction backtrace audit v1 provenance, inventory, candidate, self-exclusion, and non-imputation invariants verified.')
