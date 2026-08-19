#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'results'/'phase_v_canonical_six_mode_coordinates_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_canonical_six_mode_coordinates_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw); F=d['features']; assert len(F)==55
# Exact serialized-coordinate equivalence: no tolerance-based clustering.
groups={}
for f in F:
 key=tuple(float(x).hex() for x in f['six_mode_coordinates'])
 groups.setdefault(key,[]).append({'feature_index':f['feature_index'],'representative':f.get('representative')})
classes=sorted(groups.values(),key=lambda g:g[0]['feature_index'])
# Exact central symmetry classes y ~ -y are audited separately.
sym={}
for f in F:
 y=tuple(float(x) for x in f['six_mode_coordinates']); neg=tuple((-x).hex() for x in y); pos=tuple(x.hex() for x in y); key=min(pos,neg)
 sym.setdefault(key,[]).append({'feature_index':f['feature_index'],'representative':f.get('representative')})
sym_classes=sorted(sym.values(),key=lambda g:g[0]['feature_index'])
out={'status':'FEATURE_TRAJECTORY_EQUIVALENCE_AUDIT_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features':55,'coordinate_dimension':6,'exact_equivalence_class_count':len(classes),'exact_equivalence_classes':classes,'central_symmetry_class_count':len(sym_classes),'central_symmetry_classes':sym_classes,'exact_reduction':55-len(classes),'central_symmetry_reduction':55-len(sym_classes),'interpretation':'exact_coordinate_equivalence_and_sign_symmetry_audit_no_tolerance_clustering'}
OUT=ROOT/'results'/'phase_v_feature_trajectory_equivalence_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(f"PASS: Phase V feature trajectory equivalence audit v1 completed: n_features=55, exact_classes={len(classes)}, central_symmetry_classes={len(sym_classes)}.")
