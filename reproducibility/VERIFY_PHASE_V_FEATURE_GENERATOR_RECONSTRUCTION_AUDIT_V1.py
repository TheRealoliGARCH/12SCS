#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'results'/'phase_v_feature_generator_reconstruction_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_feature_generator_reconstruction_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text())
assert d['status'] in {'FEATURE_GENERATOR_CANDIDATES_FOUND','FEATURE_GENERATOR_NOT_IDENTIFIABLE'}
assert d['classification'] in {'GENERATOR_CANDIDATES_REQUIRE_EXPLICIT_RECONSTRUCTION','GENERATOR_NOT_IDENTIFIABLE'} and d['target_width']==55
assert d['candidate_count']==len(d['candidate_files']) and d['strong_candidate_count']==len(d['strong_generator_candidates'])
seen=set()
for x in d['candidate_files']:
 assert x['path'] not in seen; seen.add(x['path']); p=ROOT/x['path']; assert p.exists(); assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']; assert x['markers']
for x in d['strong_generator_candidates']: assert x in d['candidate_files'] and x.get('construction_calls')
if d['status']=='FEATURE_GENERATOR_NOT_IDENTIFIABLE': assert not d['strong_generator_candidates']
assert d['scope']=='inventory_and_classification_only; textual_or_ast_hits_do_not_by_themselves_establish_the_55_dimensional_generator'
assert d['interpretation']=='the_audit_identifies_repository_evidence_that_may_construct_or_establish_feature_width_and_refuses_to_impute_a_generator_or_semantic_feature_mapping'
print('PASS: Phase V feature generator reconstruction audit v1 provenance, candidate, width, construction, and non-imputation invariants verified.')
