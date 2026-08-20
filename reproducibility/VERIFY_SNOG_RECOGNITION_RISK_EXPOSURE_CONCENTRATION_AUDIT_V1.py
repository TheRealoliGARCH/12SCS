from pathlib import Path
import subprocess,sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'snog_recognition_risk_exposure_audit_v1.json'
OUT=ROOT/'results'/'snog_recognition_risk_exposure_concentration_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_snog_recognition_risk_exposure_concentration_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); raw=SRC.read_bytes()
assert d['source_sha256']==hashlib.sha256(raw).hexdigest()
assert d['structural_exposure_count']==d['recognition_layer_count']*d['risk_pathway_count']
assert math.isclose(sum(d['layer_shares'].values()),1.0,rel_tol=0,abs_tol=1e-12)
assert d['uniform_exposure'] is True
assert math.isclose(d['hhi'],1/d['recognition_layer_count'],rel_tol=0,abs_tol=1e-12)
assert math.isclose(d['effective_layer_count'],d['recognition_layer_count'],rel_tol=0,abs_tol=1e-12)
assert d['verdict']=='UNIFORM_STRUCTURAL_EXPOSURE_NO_LAYER_DOMINANCE'
assert all(d['invariants'].values())
print('PASS: SNoG recognition-risk exposure concentration audit v1 provenance, uniformity, concentration, effective-count, and non-incidence invariants verified.')
