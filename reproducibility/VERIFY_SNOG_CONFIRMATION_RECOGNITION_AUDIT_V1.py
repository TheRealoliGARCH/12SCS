from pathlib import Path
import subprocess,sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'/'snog_confirmation_recognition_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_snog_confirmation_recognition_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text())
for name,sha in d['inputs_sha256'].items():
    p=ROOT/'results'/name; assert p.exists(); assert hashlib.sha256(p.read_bytes()).hexdigest()==sha
assert d['status']=='RECOGNITION_LAYER_SPLIT'
assert d['overall_verdict']=='SNOG_NOT_CONFIRMED_UNDER_STRICT_RECOGNITION_CRITERIA'
s=d['status_by_rule']; assert s['demonstration_required']=='NOT_CONFIRMED'; assert s['official_acknowledgement_required']=='NOT_CONFIRMED'; assert s['leader_binary_confirmation_required']=='NOT_CONFIRMED'; assert s['named_institutional_attribution_required']=='CONFIRMED_AS_ATTRIBUTED_CAPABILITY'
assert all(d['invariants'].values())
print('PASS: SNoG confirmation recognition audit v1 provenance, recognition-layer separation, strict non-upgrade, and attribution invariants verified.')
