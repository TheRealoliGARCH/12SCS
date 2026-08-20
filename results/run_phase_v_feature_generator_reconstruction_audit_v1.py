#!/usr/bin/env python3
import ast, hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'/'phase_v_feature_generator_reconstruction_audit_v1.json'
EXCLUDE={OUT.resolve()}
ROOTS=['results','reproducibility','src','model','tests','data']
files=[]
for name in ROOTS:
 p=ROOT/name
 if p.exists(): files += [x for x in p.rglob('*') if x.is_file() and x.resolve() not in EXCLUDE and x.suffix in {'.py','.json','.csv','.txt','.md'}]
pat=re.compile(r'\b55\b|n_features|feature(?:_| )?(?:matrix|vector|names|index)|shape|columns|concat|stack|basis',re.I)
hits=[]
for p in sorted(set(files)):
 raw=p.read_bytes()
 try: text=raw.decode('utf-8')
 except UnicodeDecodeError: continue
 if not pat.search(text): continue
 entry={'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(raw).hexdigest(),'markers':sorted(set(m.group(0) for m in pat.finditer(text)),key=str.lower)}
 if p.suffix=='.py':
  try:
   tree=ast.parse(text); calls=[]
   for node in ast.walk(tree):
    if isinstance(node,ast.Call):
     f=node.func; name2=f.id if isinstance(f,ast.Name) else (f.attr if isinstance(f,ast.Attribute) else None)
     if name2 in {'array','asarray','concatenate','concat','hstack','vstack','stack','column_stack','zeros','ones','reshape','append','extend'}: calls.append(name2)
   entry['construction_calls']=sorted(set(calls))
  except SyntaxError: entry['construction_calls']=['SYNTAX_UNAVAILABLE']
 hits.append(entry)
# A generator is identifiable only if repository evidence exposes a concrete width-producing construction mechanism.
strong=[x for x in hits if x.get('construction_calls') and any(c in x['construction_calls'] for c in ['concatenate','concat','hstack','vstack','stack','column_stack','array','append','extend'])]
if strong:
 status='FEATURE_GENERATOR_CANDIDATES_FOUND'
 classification='GENERATOR_CANDIDATES_REQUIRE_EXPLICIT_RECONSTRUCTION'
else:
 status='FEATURE_GENERATOR_NOT_IDENTIFIABLE'
 classification='GENERATOR_NOT_IDENTIFIABLE'
out={'status':status,'classification':classification,'target_width':55,'search_roots':ROOTS,'candidate_files':hits,'strong_generator_candidates':strong,'candidate_count':len(hits),'strong_candidate_count':len(strong),'scope':'inventory_and_classification_only; textual_or_ast_hits_do_not_by_themselves_establish_the_55_dimensional_generator','interpretation':'the_audit_identifies_repository_evidence_that_may_construct_or_establish_feature_width_and_refuses_to_impute_a_generator_or_semantic_feature_mapping'}
OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(f"PASS: Phase V feature generator reconstruction audit v1 completed: status={status}, candidate_files={len(hits)}, strong_generator_candidates={len(strong)}.")
