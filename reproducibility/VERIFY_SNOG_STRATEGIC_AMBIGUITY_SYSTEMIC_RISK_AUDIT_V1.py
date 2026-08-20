from pathlib import Path
import subprocess,sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data'/'snog_strategic_ambiguity_systemic_risk_v1.json'; OUT=ROOT/'results'/'snog_strategic_ambiguity_systemic_risk_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_snog_strategic_ambiguity_systemic_risk_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); raw=SRC.read_bytes()
assert d['source_sha256']==hashlib.sha256(raw).hexdigest()
assert d['recognition_layer_count']==4 and d['risk_pathway_count']==4
assert d['status']=='SYSTEMIC_RISK_PATHWAYS_IDENTIFIED'
assert all(d['guardrails'].values())
print('PASS: SNoG strategic ambiguity and systemic risk audit v1 provenance, pathway, recognition-separation, and non-prediction invariants verified.')
