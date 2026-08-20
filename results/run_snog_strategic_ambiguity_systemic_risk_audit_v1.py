from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data'/'snog_strategic_ambiguity_systemic_risk_v1.json'
OUT=ROOT/'results'/'snog_strategic_ambiguity_systemic_risk_audit_v1.json'
raw=SRC.read_bytes(); d=json.loads(raw)
L=d['recognition_layers']; R=d['risk_pathways']; G=d['guardrails']
assert len(set(L))==len(L) and len(L)>=2
assert len({x['id'] for x in R})==len(R) and all(x['mechanism'] for x in R)
assert all(G.values())
out={'audit':d['audit'],'scope':d['scope'],'recognition_layer_count':len(L),'risk_pathway_count':len(R),'risk_pathway_ids':[x['id'] for x in R],'status':'SYSTEMIC_RISK_PATHWAYS_IDENTIFIED','source_sha256':hashlib.sha256(raw).hexdigest(),'guardrails':G}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(f"PASS: SNoG strategic ambiguity and systemic risk audit v1 completed: recognition_layers={len(L)}, risk_pathways={len(R)}.")
