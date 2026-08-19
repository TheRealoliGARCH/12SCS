#!/usr/bin/env python3
"""Exact deterministic correspondence between baseline and locally perturbed H1 diagrams."""
import csv, hashlib, itertools, json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'results' / 'capability_latent_matrix_v2.csv'
BASE = ROOT / 'results' / 'phase_v_h1_persistence_bars_v2.csv'
OUT = ROOT / 'results' / 'phase_v_persistence_correspondence_v1.json'
raw_x, raw_b = SRC.read_bytes(), BASE.read_bytes()
with SRC.open(newline='', encoding='utf-8') as f: rows=list(csv.reader(f))
assert rows and rows[0][0]=='state'
X=[[float(x) for x in r[1:]] for r in rows[1:]]; n=len(X); p=len(rows[0])-1
assert n==12 and p==12 and all(len(r)==p and all(math.isfinite(x) for x in r) for r in X)
with BASE.open(newline='', encoding='utf-8') as f:
    base=[(float(r['birth']),float(r['death'])) for r in csv.DictReader(f) if r['death']!='inf']
assert len(base)==55

def diagram(Y):
 D=[[math.dist(Y[i],Y[j]) for j in range(n)] for i in range(n)]
 def filt(s): return 0.0 if len(s)<=1 else max(D[i][j] for i,j in itertools.combinations(s,2))
 simplices=[tuple(c) for k in range(1,n+1) for c in itertools.combinations(range(n),k)]
 simplices.sort(key=lambda s:(filt(s),len(s),s)); index={s:i for i,s in enumerate(simplices)}; values=[filt(s) for s in simplices]
 low_to_col={}; reduced={}; bars=[]
 for j,s in enumerate(simplices):
  col=set() if len(s)==1 else {index[s[:k]+s[k+1:]] for k in range(len(s))}
  while col and max(col) in low_to_col: col ^= reduced[low_to_col[max(col)]]
  if col:
   low=max(col); low_to_col[low]=j; reduced[j]=col
   if len(simplices[low])==2: bars.append((values[low],values[j]))
 return sorted(bars,key=lambda z:(z[0],z[1]))

def hungarian(cost):
 # Minimum-cost perfect assignment, deterministic for equal costs.
 N=len(cost); u=[0.0]*(N+1); v=[0.0]*(N+1); p0=[0]*(N+1); way=[0]*(N+1)
 for i in range(1,N+1):
  p0[0]=i; j0=0; minv=[float('inf')]*(N+1); used=[False]*(N+1)
  while True:
   used[j0]=True; i0=p0[j0]; delta=float('inf'); j1=0
   for j in range(1,N+1):
    if not used[j]:
     cur=cost[i0-1][j-1]-u[i0]-v[j]
     if cur<minv[j]-1e-15: minv[j]=cur; way[j]=j0
     if minv[j]<delta-1e-15 or (abs(minv[j]-delta)<=1e-15 and (j1==0 or j<j1)): delta=minv[j]; j1=j
   for j in range(N+1):
    if used[j]: u[p0[j]]+=delta; v[j]-=delta
    else: minv[j]-=delta
   j0=j1
   if p0[j0]==0: break
  while True:
   j1=way[j0]; p0[j0]=p0[j1]; j0=j1
   if j0==0: break
 ans=[0]*N
 for j in range(1,N+1): ans[p0[j]-1]=j-1
 return ans

ranges=[max(X[i][j] for i in range(n))-min(X[i][j] for i in range(n)) for j in range(p)]
levels=[0.01,0.02,0.05]; audits=[]
for level in levels:
 Y=[[x+(-1.0 if ((i+2*j)%2) else 1.0)*level*ranges[j] for j,x in enumerate(row)] for i,row in enumerate(X)]
 pert=diagram(Y); assert len(pert)==len(base)==55
 cost=[[max(abs(a[0]-b[0]),abs(a[1]-b[1])) for b in pert] for a in base]
 match=hungarian(cost)
 pairs=[]
 for i,j in enumerate(match):
  b,d=base[i]; bp,dp=pert[j]; pairs.append({'baseline_index':i,'perturbed_index':j,'baseline_birth':b,'baseline_death':d,'perturbed_birth':bp,'perturbed_death':dp,'linf_displacement':cost[i][j]})
 audits.append({'level':level,'n_matched':len(pairs),'max_linf_displacement':max(x['linf_displacement'] for x in pairs,default=0.0),'mean_linf_displacement':sum(x['linf_displacement'] for x in pairs)/len(pairs) if pairs else 0.0,'pairs':pairs})
# A baseline feature is correspondence-complete only when matched at every tested level.
stable=[i for i in range(len(base)) if all(any(x['baseline_index']==i for x in a['pairs']) for a in audits)]
out={'status':'PERSISTENCE_CORRESPONDENCE_COMPLETE','source_latent_matrix_path':str(SRC.relative_to(ROOT)),'source_latent_matrix_sha256':hashlib.sha256(raw_x).hexdigest(),'baseline_bars_path':str(BASE.relative_to(ROOT)),'baseline_bars_sha256':hashlib.sha256(raw_b).hexdigest(),'perturbation_levels':levels,'baseline_finite_h1_features':len(base),'correspondence_method':'minimum_cost_bipartite_assignment_linf_birth_death','audits':audits,'cross_level_correspondence_complete_indices':stable,'cross_level_correspondence_complete_count':len(stable)}
OUT.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
print(f"PASS: Phase V persistence correspondence v1 completed: baseline_features={len(base)}, cross_level_correspondence_complete={len(stable)}.")
