from pathlib import Path
import subprocess,sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data'/'snog_israeli_capability_evidence_dependence_v1.json'; OUT=ROOT/'results'/'snog_israeli_capability_evidence_dependence_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_snog_israeli_capability_evidence_dependence_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); raw=SRC.read_bytes()
assert d['source_sha256']==hashlib.sha256(raw).hexdigest()
assert d['claimant_count']>0 and d['evidence_family_count']>0
assert d['independence_verdict']=='CLAIMANT_COUNT_NOT_TREATED_AS_INDEPENDENT_CONFIRMATION'
assert d['invariants']['claimant_count_is_not_evidence_family_count']
assert d['invariants']['no_public_test_imputed'] and d['invariants']['vela_not_confirmed_as_attribution']
print('PASS: SNoG Israeli capability evidence dependence audit v1 provenance, family, dependence, and non-imputation invariants verified.')
