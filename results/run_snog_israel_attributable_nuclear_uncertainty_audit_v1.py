from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data'/'snog_israel_attributable_nuclear_uncertainty_v1.json'
OUT=ROOT/'results'/'snog_israel_attributable_nuclear_uncertainty_audit_v1.json'
raw=SRC.read_bytes(); d=json.loads(raw); C=d['components']; G=d['guardrails']
assert C and len({x['id'] for x in C})==len(C) and all(x['basis'] for x in C)
present=sum(bool(x['present']) for x in C); n=len(C); index=present/n
out={'audit':d['audit'],'scope':d['scope'],'component_count':n,'present_component_count':present,'uncertainty_component_coverage_index':index,'scale':'0_to_1','interpretation':d['scoring_rule']['interpretation'],'status':'ISRAEL_ATTRIBUTABLE_STRUCTURAL_UNCERTAINTY_QUANTIFIED','source_sha256':hashlib.sha256(raw).hexdigest(),'components':C,'guardrails':G}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(f'PASS: SNoG Israel-attributable nuclear uncertainty audit v1 completed: components={n}, present={present}, uncertainty_component_coverage_index={index:.12g}.')
