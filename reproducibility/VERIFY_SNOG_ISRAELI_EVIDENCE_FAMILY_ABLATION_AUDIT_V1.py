from pathlib import Path
import subprocess,sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data'/'snog_israeli_capability_evidence_dependence_v1.json'; OUT=ROOT/'results'/'snog_israeli_evidence_family_ablation_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_snog_israeli_evidence_family_ablation_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); raw=SRC.read_bytes(); src=json.loads(raw)
assert d['source_sha256']==hashlib.sha256(raw).hexdigest()
F=sorted({f for c in src['claimants'] for f in c['families']})
assert d['evidence_family_count']==len(F)==len(d['ablations'])
assert d['claimant_count']==len(src['claimants'])
for a in d['ablations']:
    assert a['removed_family'] in F
    assert a['affected_count']+len(a['unaffected_claimants'])==d['claimant_count']
    assert all(x['families_after']==x['families_before']-1 for x in a['affected_claimants'])
    assert a['unsupported_count']==0
assert d['verdict']=='NO_SINGLE_RECORDED_EVIDENCE_FAMILY_ELIMINATES_ALL_RECORDED_CLAIMANT_SUPPORT'
print('PASS: SNoG Israeli evidence-family ablation audit v1 provenance, ablation, support, and non-imputation invariants verified.')
