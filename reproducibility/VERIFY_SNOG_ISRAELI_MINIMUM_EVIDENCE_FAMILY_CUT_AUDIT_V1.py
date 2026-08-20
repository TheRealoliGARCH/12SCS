from pathlib import Path
import subprocess,sys,json,hashlib,itertools
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data'/'snog_israeli_capability_evidence_dependence_v1.json'; OUT=ROOT/'results'/'snog_israeli_minimum_evidence_family_cut_audit_v1.json'
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_snog_israeli_minimum_evidence_family_cut_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); raw=SRC.read_bytes(); src=json.loads(raw); C=src['claimants']; F=sorted({f for c in C for f in c['families']})
assert d['source_sha256']==hashlib.sha256(raw).hexdigest()
assert d['claimant_count']==len(C) and d['evidence_family_count']==len(F)
assert 1<=d['minimum_cut_size']<=len(F) and d['minimum_cuts']
for cut in d['minimum_cuts']:
    assert len(cut)==d['minimum_cut_size']
    assert all(not(set(c['families'])-set(cut)) for c in C)
for k in range(1,d['minimum_cut_size']):
    for cut in itertools.combinations(F,k):
        assert any(set(c['families'])-set(cut) for c in C)
assert d['verdict']=='MINIMUM_CUT_REQUIRED_TO_REMOVE_ALL_RECORDED_CLAIMANT_SUPPORT'
assert d['invariants']['minimum_cut_exhaustively_enumerated']
print('PASS: SNoG Israeli minimum evidence-family cut audit v1 provenance, exhaustive minimum-cut, support, and non-imputation invariants verified.')
