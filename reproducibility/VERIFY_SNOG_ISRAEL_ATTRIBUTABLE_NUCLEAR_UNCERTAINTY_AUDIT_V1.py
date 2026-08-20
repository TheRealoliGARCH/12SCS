from pathlib import Path
import subprocess,sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data'/'snog_israel_attributable_nuclear_uncertainty_v1.json'; OUT=ROOT/'results'/'snog_israel_attributable_nuclear_uncertainty_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_snog_israel_attributable_nuclear_uncertainty_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); src=json.loads(SRC.read_text())
assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest()
assert d['component_count']==len(src['components'])==4
assert d['present_component_count']==sum(x['present'] for x in src['components'])
assert math.isclose(d['uncertainty_component_coverage_index'],d['present_component_count']/d['component_count'],rel_tol=0,abs_tol=1e-12)
assert d['status']=='ISRAEL_ATTRIBUTABLE_STRUCTURAL_UNCERTAINTY_QUANTIFIED'
assert all(d['guardrails'].values())
print('PASS: SNoG Israel-attributable nuclear uncertainty audit v1 provenance, component, quantification, attribution-boundary, and non-causation invariants verified.')
