#!/usr/bin/env python3
import hashlib,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_deep_provenance_backtrace_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_deep_provenance_backtrace_audit_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw); assert d['n_features']==54
patterns={'feature_index':re.compile(r'feature_index'),'feature_names':re.compile(r'feature_names'),'columns':re.compile(r'columns'),'canonical_state':re.compile(r'canonical[_ ]state',re.I)}
roots=['results','reproducibility','data','src','model','tests']
hits=[]
for name in roots:
 p=ROOT/name
 if not p.exists(): continue
 for f in sorted(p.rglob('*')):
  if not f.is_file() or f.suffix not in {'.py','.json','.csv','.md','.txt'}: continue
  try: t=f.read_text(errors='ignore')
  except Exception: continue
  found=[k for k,rx in patterns.items() if rx.search(t)]
  if found: hits.append({'path':str(f.relative_to(ROOT)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'markers':found})
identity_files=[x for x in hits if 'feature_names' in x['markers'] or 'columns' in x['markers']]
status='FEATURE_CONSTRUCTION_PROVENANCE_CANDIDATES_FOUND' if identity_files else 'FEATURE_CONSTRUCTION_PROVENANCE_NOT_FOUND'
out={'status':status,'source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features':54,'search_scope':roots,'candidate_files':hits,'identity_candidate_count':len(identity_files),'interpretation':'repository-level textual provenance candidates are inventoried only; semantic identity is not asserted unless an explicit feature-index-to-source-variable mapping is present'}
OUT=ROOT/'results'/'phase_v_feature_construction_backtrace_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(f'PASS: Phase V feature construction backtrace audit v1 completed: status={status}, candidate_files={len(hits)}, identity_candidates={len(identity_files)}.')
