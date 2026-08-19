#!/usr/bin/env python3
import hashlib,json,math,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_stability_trajectory_compression_v1.json'; OUT=ROOT/'results'/'phase_v_intrinsic_dimension_audit_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_stability_trajectory_compression_v1.py')],cwd=ROOT,check=True)
if not OUT.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_intrinsic_dimension_audit_v1.py')],cwd=ROOT,check=True)
d=json.loads(OUT.read_text()); assert d['status']=='INTRINSIC_DIMENSION_AUDIT_COMPLETE'; assert d['source_sha256']==hashlib.sha256(SRC.read_bytes()).hexdigest(); assert d['n_features']==55 and d['trajectory_dimension']==8
sv=d['singular_values']; assert len(sv)==8 and all(math.isfinite(x) and x>=0 for x in sv) and sv==sorted(sv,reverse=True)
assert d['positive_singular_value_count']==sum(x>0 for x in sv)
assert d['interpretation']=='diagnostic_spectrum_no_single_intrinsic_dimension_declared'
r=d['numerical_rank_by_relative_tolerance']; assert set(r)=={'1e-06','1e-08','1e-10','1e-12'}
vals=[r[k] for k in ['1e-06','1e-08','1e-10','1e-12']]; assert vals==sorted(vals)
print('PASS: Phase V intrinsic-dimension audit v1 provenance, spectrum, and rank-diagnostic invariants verified.')
