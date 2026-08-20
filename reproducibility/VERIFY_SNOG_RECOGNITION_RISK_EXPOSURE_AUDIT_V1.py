from pathlib import Path
import os,subprocess,sys,json,hashlib
MANIFEST='data/snog_strategic_ambiguity_systemic_risk_v1.json'
def find_root():
    candidates=[]
    for key in ('REPO_ROOT','GITHUB_WORKSPACE'):
        if os.environ.get(key): candidates.append(Path(os.environ[key]))
    candidates += [Path.cwd(), Path(__file__).resolve().parent]
    for start in candidates:
        for p in (start,*start.parents):
            if (p/MANIFEST).exists(): return p
    raise FileNotFoundError(f'Could not locate repository root containing {MANIFEST}; set REPO_ROOT to the 12SCS checkout')
ROOT=find_root(); SRC=ROOT/MANIFEST; OUT=ROOT/'results'/'snog_recognition_risk_exposure_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_snog_recognition_risk_exposure_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); src=json.loads(SRC.read_text())
assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest()
assert d['recognition_layer_count']==len(src['recognition_layers']) and d['risk_pathway_count']==len(src['risk_pathways'])
assert d['cross_layer_exposure_count']==d['recognition_layer_count']*d['risk_pathway_count']
assert all(v==d['risk_pathway_count'] for v in d['layer_pathway_counts'].values())
assert d['status']=='RECOGNITION_RISK_EXPOSURE_MATRIX_COMPLETE' and all(d['guardrails'].values())
print('PASS: SNoG recognition-risk exposure audit v1 provenance, matrix completeness, recognition separation, and non-incidence invariants verified.')
