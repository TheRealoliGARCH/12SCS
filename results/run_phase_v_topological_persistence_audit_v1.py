#!/usr/bin/env python3
import csv, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/'results'
candidates=sorted([p for p in RESULTS.glob('*.csv') if 'distance' in p.name.lower() and 'matrix' in p.name.lower()])
if not candidates:
    raise FileNotFoundError('No frozen distance-matrix CSV found in results/.')
path=candidates[0]
with path.open(newline='',encoding='utf-8') as f:
    rows=list(csv.reader(f))
# Accept either labelled square matrix or numeric square matrix.
try:
    matrix=[[float(x) for x in r] for r in rows]
except ValueError:
    matrix=[[float(x) for x in r[1:]] for r in rows[1:]]
n=len(matrix)
assert n>1 and all(len(r)==n for r in matrix)
assert all(abs(matrix[i][i])<1e-12 for i in range(n))
assert all(abs(matrix[i][j]-matrix[j][i])<1e-10 for i in range(n) for j in range(n))
# H0 Vietoris--Rips persistence: finite death times are MST edge lengths.
parent=list(range(n))
def find(x):
    while parent[x]!=x:
        parent[x]=parent[parent[x]]; x=parent[x]
    return x
def union(a,b):
    a,b=find(a),find(b)
    if a==b:return False
    parent[b]=a; return True
edges=sorted((matrix[i][j],i,j) for i in range(n) for j in range(i+1,n))
deaths=[]
for d,i,j in edges:
    if union(i,j):
        deaths.append(d)
        if len(deaths)==n-1: break
out=RESULTS/'phase_v_topological_persistence_audit_v1.csv'
with out.open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['metric','value'])
    for k,v in [('source_artifact',path.name),('n_points',n),('h0_finite_bars',len(deaths)),('h0_birth',0.0),('h0_max_death',max(deaths)),('h0_total_persistence',sum(deaths)),('source_sha256',hashlib.sha256(path.read_bytes()).hexdigest())]: w.writerow([k,v])
print(f'PASS: Phase V topological persistence audit v1 completed: n_points={n}, h0_finite_bars={len(deaths)}.')
