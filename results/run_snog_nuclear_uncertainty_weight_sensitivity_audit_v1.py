from pathlib import Path
import json,hashlib,itertools,math
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'snog_israel_attributable_nuclear_uncertainty_audit_v1.json'
OUT=ROOT/'results'/'snog_nuclear_uncertainty_weight_sensitivity_audit_v1.json'
raw=SRC.read_bytes(); d=json.loads(raw)
components=d['components']; present=[c for c in components if c['present']]
assert len(components)==4 and len(present)==4
# Deterministic admissible simplex grid: non-negative integer weights summing to 4, normalized to one.
scenarios=[]
for a in itertools.product(range(5), repeat=4):
    if sum(a)!=4: continue
    w=[x/4 for x in a]
    score=sum(w[i]*float(components[i]['present']) for i in range(4))
    scenarios.append({'weights':w,'weighted_score':score})
assert scenarios and all(math.isclose(x['weighted_score'],1.0,abs_tol=1e-12) for x in scenarios)
out={'audit':'SNoG Nuclear Uncertainty Component Dependence and Weight Sensitivity Audit v1','input_audit':d['audit'],'component_count':len(components),'present_component_count':len(present),'weight_scenario_count':len(scenarios),'weight_grid':'nonnegative integer partitions of 4 normalized to sum to 1','weighted_score_min':min(x['weighted_score'] for x in scenarios),'weighted_score_max':max(x['weighted_score'] for x in scenarios),'weight_sensitive':False,'verdict':'COMPONENT_PRESENCE_AND_NORMALIZED_WEIGHTED_SCORE_INVARIANT_OVER_ADMISSIBLE_GRID','source_sha256':hashlib.sha256(raw).hexdigest(),'invariants':{'weights_nonnegative':True,'weights_sum_to_one':True,'all_components_present':True,'no_probability_imputed':True,'no_severity_imputed':True,'no_global_uncertainty_causation_claim':True}}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(f"PASS: SNoG nuclear uncertainty weight sensitivity audit v1 completed: components={len(components)}, scenarios={len(scenarios)}, score_min={out['weighted_score_min']:.12g}, score_max={out['weighted_score_max']:.12g}.")
