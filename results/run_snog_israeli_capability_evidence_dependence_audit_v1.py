from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data'/'snog_israeli_capability_evidence_dependence_v1.json'
OUT=ROOT/'results'/'snog_israeli_capability_evidence_dependence_audit_v1.json'
raw=SRC.read_bytes(); d=json.loads(raw)
C=d['claimants']; E=d['evidence_families']
assert len(C)>0 and len(E)>0
ids={x['id'] for x in E}; assert len(ids)==len(E)
for c in C:
    assert c['families'] and set(c['families'])<=ids
    assert c['dependence'] in {'INDEPENDENT_EVIDENCE_CHAIN','PARTIALLY_OVERLAPPING_CHAIN','PARTIALLY_OVERLAPPING','COMMON_SOURCE_DEPENDENCE','UNSPECIFIED_EVIDENCE'}
used=sorted({f for c in C for f in c['families']})
out={'audit':d['audit'],'proposition':d['proposition'],'claimant_count':len(C),'evidence_family_count':len(used),'used_evidence_families':used,'independence_verdict':'CLAIMANT_COUNT_NOT_TREATED_AS_INDEPENDENT_CONFIRMATION','source_sha256':hashlib.sha256(raw).hexdigest(),'invariants':d['invariants']}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(f"PASS: SNoG Israeli capability evidence dependence audit v1 completed: claimants={len(C)}, evidence_families={len(used)}.")
