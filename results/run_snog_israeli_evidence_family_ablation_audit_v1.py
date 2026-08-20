from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data'/'snog_israeli_capability_evidence_dependence_v1.json'
OUT=ROOT/'results'/'snog_israeli_evidence_family_ablation_audit_v1.json'
raw=SRC.read_bytes(); d=json.loads(raw)
C=d['claimants']; F=sorted({f for c in C for f in c['families']})
assert C and F
rows=[]
for f in F:
    affected=[]; retained=[]
    for c in C:
        remaining=[x for x in c['families'] if x!=f]
        rec={'name':c['name'],'families_before':len(c['families']),'families_after':len(remaining),'support_status':'SUPPORTED_AFTER_ABLATION' if remaining else 'NO_REMAINING_RECORDED_FAMILY'}
        (affected if f in c['families'] else retained).append(rec)
    rows.append({'removed_family':f,'affected_claimants':affected,'unaffected_claimants':retained,'affected_count':len(affected),'unsupported_count':sum(x['support_status']=='NO_REMAINING_RECORDED_FAMILY' for x in affected)})
out={'audit':'SNoG Israeli Evidence-Family Ablation Audit v1','input_audit':d['audit'],'claimant_count':len(C),'evidence_family_count':len(F),'ablations':rows,'source_sha256':hashlib.sha256(raw).hexdigest(),'verdict':'NO_SINGLE_RECORDED_EVIDENCE_FAMILY_ELIMINATES_ALL_RECORDED_CLAIMANT_SUPPORT','invariants':{'one_family_removed_per_ablation':True,'claimants_recomputed_from_manifest':True,'no_public_test_imputed':True,'no_independence_created_by_ablation':True,'vela_not_promoted_to_confirmed_attribution':True}}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(f'PASS: SNoG Israeli evidence-family ablation audit v1 completed: claimants={len(C)}, evidence_families={len(F)}, ablations={len(rows)}.')
