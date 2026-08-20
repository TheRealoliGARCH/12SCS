from pathlib import Path
import os,json,hashlib
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
raw=SRC.read_bytes(); d=json.loads(raw); L=d['recognition_layers']; R=d['risk_pathways']; G=d['guardrails']
assert L and R and all(G.values())
rows=[{'recognition_layer':l,'risk_pathway_id':r['id'],'exposure_status':'PATHWAY_APPLICABLE_AT_STRUCTURAL_LEVEL'} for l in L for r in R]
counts={l:sum(x['recognition_layer']==l for x in rows) for l in L}
out={'audit':'SNoG Recognition-Risk Exposure Audit v1','input_audit':d['audit'],'recognition_layer_count':len(L),'risk_pathway_count':len(R),'cross_layer_exposure_count':len(rows),'layer_pathway_counts':counts,'status':'RECOGNITION_RISK_EXPOSURE_MATRIX_COMPLETE','source_sha256':hashlib.sha256(raw).hexdigest(),'guardrails':{**G,'no_probability_imputed':True,'cross_product_is_not_real_world_incidence':True}}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(f'PASS: SNoG recognition-risk exposure audit v1 completed: recognition_layers={len(L)}, risk_pathways={len(R)}, structural_exposures={len(rows)}.')
