from pathlib import Path
import subprocess,sys,json,hashlib

def find_root():
    for start in (Path.cwd().resolve(), Path(__file__).resolve().parent):
        for p in (start,*start.parents):
            if (p/'data'/'snog_strategic_ambiguity_systemic_risk_v1.json').exists() and (p/'results').is_dir() and (p/'reproducibility').is_dir():
                return p
    raise FileNotFoundError('Could not locate 12SCS repository root containing the strategic ambiguity manifest')

ROOT=find_root()
SRC=ROOT/'data'/'snog_strategic_ambiguity_systemic_risk_v1.json'; OUT=ROOT/'results'/'snog_recognition_risk_exposure_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_snog_recognition_risk_exposure_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); src=json.loads(SRC.read_text())
assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest()
assert d['recognition_layer_count']==len(src['recognition_layers'])
assert d['risk_pathway_count']==len(src['risk_pathways'])
assert d['cross_layer_exposure_count']==d['recognition_layer_count']*d['risk_pathway_count']
assert all(v==d['risk_pathway_count'] for v in d['layer_pathway_counts'].values())
assert d['status']=='RECOGNITION_RISK_EXPOSURE_MATRIX_COMPLETE'
assert all(d['guardrails'].values())
print('PASS: SNoG recognition-risk exposure audit v1 provenance, matrix completeness, recognition separation, and non-incidence invariants verified.')
