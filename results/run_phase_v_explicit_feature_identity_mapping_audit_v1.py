#!/usr/bin/env python3
import ast,csv,hashlib,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_feature_construction_backtrace_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_feature_construction_backtrace_audit_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw)
cands=[x for x in d['candidate_files'] if 'feature_names' in x['markers'] or 'columns' in x['markers']]
assert len(cands)==d['identity_candidate_count']
index_name=re.compile(r'(?i)(?:feature_index|feature[_ -]?id|index)\s*[:=]\s*(\d+)')
map_rows=[]; reports=[]
for x in cands:
 p=ROOT/x['path']; text=p.read_text(errors='ignore'); found=[]
 # JSON dictionaries/lists and CSV rows are inspected conservatively for explicit numeric-index/name pairs.
 try:
  obj=json.loads(text)
  def walk(z):
   if isinstance(z,dict):
    ks={str(k).lower():v for k,v in z.items()}
    ik=next((k for k in ks if k in {'feature_index','feature_id','index'}),None)
    nk=next((k for k in ks if k in {'feature_name','name','column','variable','source_variable'}),None)
    if ik and nk and isinstance(ks[ik],int) and isinstance(ks[nk],str): found.append((ks[ik],ks[nk]))
    for v in z.values(): walk(v)
   elif isinstance(z,list):
    for v in z: walk(v)
  walk(obj)
 except Exception: pass
 try:
  for row in csv.DictReader(text.splitlines()):
   if row and any(k in row for k in ('feature_index','feature_id','index')):
    ik=next(k for k in ('feature_index','feature_id','index') if k in row)
    nk=next((k for k in ('feature_name','name','column','variable','source_variable') if k in row),None)
    if nk and row.get(ik,'').strip().isdigit() and row.get(nk): found.append((int(row[ik]),row[nk]))
 except Exception: pass
 for m in index_name.finditer(text):
  # free-text index declarations are deliberately not accepted as mappings without an adjacent named field
  pass
 unique=[]; seen=set()
 for a,b in found:
  if 0<=a<55 and (a,b) not in seen: seen.add((a,b)); unique.append({'feature_index':a,'source_variable':b,'candidate_path':x['path']})
 reports.append({'path':x['path'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'explicit_pairs':len(unique)})
 map_rows.extend(unique)
by={}
for r in map_rows: by.setdefault(r['feature_index'],set()).add(r['source_variable'])
conflicts=sorted(k for k,v in by.items() if len(v)>1)
coverage=sorted(by)
status='FEATURE_IDENTITY_MAPPING_FULL' if len(coverage)==55 and not conflicts else ('FEATURE_IDENTITY_MAPPING_PARTIAL' if coverage and not conflicts else ('FEATURE_IDENTITY_MAPPING_CONFLICT' if conflicts else 'FEATURE_IDENTITY_MAPPING_NOT_FOUND'))
out={'status':status,'source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features':55,'identity_candidate_count':len(cands),'candidate_reports':reports,'mapping_rows':map_rows,'mapped_feature_count':len(coverage),'mapped_feature_indices':coverage,'conflicting_feature_indices':conflicts,'scope':'accepts_only_explicit_numeric_feature_index_to_named_variable_pairs_in_candidate_artifacts; marker_words_and_free_text_are_not_mappings','interpretation':'mapping status is determined solely by explicit candidate-artifact pairs and does not impute identities for unmapped features'}
OUT=ROOT/'results'/'phase_v_explicit_feature_identity_mapping_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(f'PASS: Phase V explicit feature identity mapping audit v1 completed: status={status}, candidates={len(cands)}, mapped_features={len(coverage)}, conflicts={len(conflicts)}.')
