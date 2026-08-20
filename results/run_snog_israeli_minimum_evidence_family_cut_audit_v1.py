from pathlib import Path
import itertools,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data'/'snog_israeli_capability_evidence_dependence_v1.json'
OUT=ROOT/'results'/'snog_israeli_minimum_evidence_family_cut_audit_v1.json'
raw=SRC.read_bytes(); d=json.loads(raw); C=d['claimants']
F=sorted({f for c in C for f in c['families']}); assert C and F
cuts=[]; minimum=None
for k in range(1,len(F)+1):
    for cut in itertools.combinations(F,k):
        removed=set(cut)
        survivors=[c['name'] for c in C if set(c['families'])-removed]
        if not survivors:
            cuts.append(list(cut)); minimum=k
    if minimum is not None: break
assert minimum is not None
out={'audit':'SNoG Israeli Minimum Evidence-Family Cut Audit v1','input_audit':d['audit'],'claimant_count':len(C),'evidence_family_count':len(F),'minimum_cut_size':minimum,'minimum_cuts':cuts,'source_sha256':hashlib.sha256(raw).hexdigest(),'verdict':'MINIMUM_CUT_REQUIRED_TO_REMOVE_ALL_RECORDED_CLAIMANT_SUPPORT','invariants':{'cuts_enumerated_in_increasing_cardinality':True,'minimum_cut_exhaustively_enumerated':True,'support_derived_only_from_manifest':True,'no_public_test_imputed':True,'vela_not_promoted_to_confirmed_attribution':True}}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(f'PASS: SNoG Israeli minimum evidence-family cut audit v1 completed: claimants={len(C)}, evidence_families={len(F)}, minimum_cut_size={minimum}, minimum_cuts={len(cuts)}.')
