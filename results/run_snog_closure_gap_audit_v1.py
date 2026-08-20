from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'snog_confirmation_recognition_audit_v1.json'
OUT=ROOT/'results'/'snog_closure_gap_audit_v1.json'
if not SRC.exists(): raise FileNotFoundError(SRC)
raw=SRC.read_bytes(); d=json.loads(raw)
strict=d['strict_confirmation']; attributed=d['attributed_capability']
assert strict=='NOT_CONFIRMED'
assert attributed=='CONFIRMED_AS_ATTRIBUTED_CAPABILITY'
gaps=[
 {'criterion':'PUBLIC_NUCLEAR_DEMONSTRATION','status':'NOT_SATISFIED'},
 {'criterion':'OFFICIAL_ACKNOWLEDGEMENT','status':'NOT_SATISFIED'},
 {'criterion':'LEADER_LEVEL_BINARY_YES','status':'NOT_SATISFIED'}]
out={'audit':'SNoG Closure Gap Audit v1','input_audit':d.get('audit'),'strict_confirmation':strict,'attributed_capability':attributed,'closure_gaps':gaps,'closure_gap_count':len(gaps),'status':'SNoG_STRICT_CLOSURE_GAPS_IDENTIFIED','source_sha256':hashlib.sha256(raw).hexdigest(),'invariants':{'no_gap_treated_as_satisfied_without_evidence':True,'attributed_capability_not_upgraded':True,'closure_not_declared':True,'no_nuclear_activity_prescribed':True}}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(f"PASS: SNoG closure gap audit v1 completed: status={out['status']}, closure_gap_count={len(gaps)}, strict_confirmation={strict}.")
