from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'snog_recognition_risk_exposure_audit_v1.json'
OUT=ROOT/'results'/'snog_recognition_risk_exposure_concentration_audit_v1.json'
raw=SRC.read_bytes(); d=json.loads(raw)
L=d['recognition_layer_count']; P=d['risk_pathway_count']; total=d['cross_layer_exposure_count']
assert L>0 and P>0 and total==L*P
counts=d['layer_pathway_counts']; assert len(counts)==L and sum(counts.values())==total
shares={k:v/total for k,v in counts.items()}
hhi=sum(v*v for v in shares.values())
effective=1/hhi
uniform=all(v==P for v in counts.values())
verdict='UNIFORM_STRUCTURAL_EXPOSURE_NO_LAYER_DOMINANCE' if uniform else 'NONUNIFORM_STRUCTURAL_EXPOSURE_REQUIRES_FURTHER_AUDIT'
out={'audit':'SNoG Recognition-Risk Exposure Concentration Audit v1','input_audit':d['audit'],'recognition_layer_count':L,'risk_pathway_count':P,'structural_exposure_count':total,'layer_counts':counts,'layer_shares':shares,'hhi':hhi,'effective_layer_count':effective,'uniform_exposure':uniform,'verdict':verdict,'source_sha256':hashlib.sha256(raw).hexdigest(),'invariants':{'counts_derived_from_input_matrix':True,'no_incidence_imputed':True,'no_probability_imputed':True,'no_layer_dominance_imputed':True}}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(f'PASS: SNoG recognition-risk exposure concentration audit v1 completed: layers={L}, exposures={total}, hhi={hhi:.12g}, effective_layers={effective:.12g}, uniform={uniform}.')
