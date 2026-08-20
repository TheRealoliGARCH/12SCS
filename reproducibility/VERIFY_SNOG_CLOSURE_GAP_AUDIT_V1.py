from pathlib import Path
import subprocess,sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'snog_confirmation_recognition_audit_v1.json'; OUT=ROOT/'results'/'snog_closure_gap_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_snog_closure_gap_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); raw=SRC.read_bytes()
assert d['source_sha256']==hashlib.sha256(raw).hexdigest()
assert d['status']=='SNoG_STRICT_CLOSURE_GAPS_IDENTIFIED'
assert d['strict_confirmation']=='NOT_CONFIRMED'
assert d['attributed_capability']=='CONFIRMED_AS_ATTRIBUTED_CAPABILITY'
assert d['closure_gap_count']==3==len(d['closure_gaps'])
assert all(x['status']=='NOT_SATISFIED' for x in d['closure_gaps'])
assert all(d['invariants'].values())
print('PASS: SNoG closure gap audit v1 provenance, gap identity, non-upgrade, non-closure, and non-prescription invariants verified.')
