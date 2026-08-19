#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'results'/'phase_v_canonical_six_mode_coordinates_v1.json'
if not SRC.exists(): subprocess.run([sys.executable,str(ROOT/'results'/'run_phase_v_canonical_six_mode_coordinates_v1.py')],cwd=ROOT,check=True)
raw=SRC.read_bytes(); d=json.loads(raw); F=d['features']; Y=[tuple(float(x) for x in f['six_mode_coordinates']) for f in F]; assert len(Y)==55 and all(len(y)==6 for y in Y)
# Canonical projective representative: divide by first nonzero coordinate and force it to +1. Exact float arithmetic only.
def key(y):
 for k,x in enumerate(y):
  if x!=0.0:
   z=[v/x for v in y]; return k,tuple(float(v).hex() for v in z)
 return 6,tuple('0x0.0p+0' for _ in y)
g={}
for i,(f,y) in enumerate(zip(F,Y)):
 g.setdefault(key(y),[]).append({'feature_index':i,'representative':f.get('representative')})
classes=sorted(g.values(),key=lambda q:q[0]['feature_index'])
out={'status':'PROJECTIVE_FEATURE_QUOTIENT_AUDIT_COMPLETE','source_path':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'n_features':55,'coordinate_dimension':6,'projective_equivalence_class_count':len(classes),'projective_equivalence_classes':classes,'projective_reduction':55-len(classes),'equivalence_definition':'y_i~y_j iff y_i=c*y_j for some nonzero real scalar c, tested by exact canonical normalization','interpretation':'exact_projective_quotient_audit_no_tolerance_clustering'}
OUT=ROOT/'results'/'phase_v_projective_feature_quotient_audit_v1.json'; OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n'); print(f"PASS: Phase V projective feature quotient audit v1 completed: n_features=55, projective_classes={len(classes)}, reduction={55-len(classes)}.")
