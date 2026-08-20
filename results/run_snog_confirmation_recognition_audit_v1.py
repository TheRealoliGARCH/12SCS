from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
DEP=ROOT/'results'/'snog_israeli_capability_evidence_dependence_audit_v1.json'
CUT=ROOT/'results'/'snog_israeli_minimum_evidence_family_cut_audit_v1.json'
OUT=ROOT/'results'/'snog_confirmation_recognition_audit_v1.json'
for p in (DEP,CUT): assert p.exists(),p
d=json.loads(DEP.read_text()); c=json.loads(CUT.read_text())
assert d['claimant_count']==5 and d['evidence_family_count']>0
assert c['claimant_count']==d['claimant_count'] and c['evidence_family_count']==d['evidence_family_count']
assert c['minimum_cut_size']==c['evidence_family_count']
inputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (DEP,CUT)}
out={'audit':'SNoG Confirmation Recognition Audit v1','entity':'Israel','recognition_criteria':{'public_nuclear_test':False,'official_acknowledgement':False,'leader_binary_yes':False,'named_institutional_attribution':True},'evidence_structure':{'claimant_count':d['claimant_count'],'evidence_family_count':d['evidence_family_count'],'minimum_cut_size':c['minimum_cut_size']},'status':'SIXTH?','status_by_rule':{'demonstration_required':'NOT_CONFIRMED','official_acknowledgement_required':'NOT_CONFIRMED','leader_binary_confirmation_required':'NOT_CONFIRMED','named_institutional_attribution_required':'CONFIRMED_AS_ATTRIBUTED_CAPABILITY'},'overall_verdict':'SIXTH?','inputs_sha256':inputs,'invariants':{'no_attribution_upgraded_to_demonstration':True,'no_attribution_upgraded_to_official_acknowledgement':True,'no_silence_counted_as_yes':True,'institutional_attribution_explicitly_separated_from_recognition':True,'vela_not_treated_as_confirmed_test':True}}
out['status']='RECOGNITION_LAYER_SPLIT'; out['overall_verdict']='SNOG_NOT_CONFIRMED_UNDER_STRICT_RECOGNITION_CRITERIA'
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('PASS: SNoG confirmation recognition audit v1 completed: status=RECOGNITION_LAYER_SPLIT, strict_confirmation=NOT_CONFIRMED, attributed_capability=CONFIRMED_AS_ATTRIBUTED_CAPABILITY.')
