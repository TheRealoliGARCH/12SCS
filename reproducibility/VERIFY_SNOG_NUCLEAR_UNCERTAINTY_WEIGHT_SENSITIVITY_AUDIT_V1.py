from pathlib import Path
import subprocess,sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'snog_israel_attributable_nuclear_uncertainty_audit_v1.json'
OUT=ROOT/'results'/'snog_nuclear_uncertainty_weight_sensitivity_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_snog_nuclear_uncertainty_weight_sensitivity_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); raw=SRC.read_bytes(); src=json.loads(raw)
assert d['source_sha256']==hashlib.sha256(raw).hexdigest()
assert d['component_count']==4 and d['present_component_count']==4
assert d['weight_scenario_count']==35
assert math.isclose(d['weighted_score_min'],1.0,abs_tol=1e-12)
assert math.isclose(d['weighted_score_max'],1.0,abs_tol=1e-12)
assert d['weight_sensitive'] is False
assert d['verdict']=='COMPONENT_PRESENCE_AND_NORMALIZED_WEIGHTED_SCORE_INVARIANT_OVER_ADMISSIBLE_GRID'
assert all(d['invariants'].values())
print('PASS: SNoG nuclear uncertainty weight sensitivity audit v1 provenance, simplex-grid, score-invariance, component-presence, and non-causation invariants verified.')
