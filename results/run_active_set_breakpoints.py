"""Analyze ranking breakpoints and active allocations along heterogeneity paths."""
from __future__ import annotations
import csv
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from model.convergence_analysis import CAPABILITIES, STATES
from model.convergence_optimization import allocate_budget
from model.heterogeneous_scenario import build_scenario
RESULTS=ROOT/'results'
BUDGET=1.0
TOL=1e-12

def read_vector(path):
    with path.open(encoding='utf-8',newline='') as f: rows=list(csv.reader(f))
    return tuple(float(r[1]) for r in rows[1:])
def read_matrix(path):
    with path.open(encoding='utf-8',newline='') as f: rows=list(csv.reader(f))
    return tuple(tuple(float(x) for x in r[1:]) for r in rows[1:])
def crossover(c1,c2,w):
    # w1/c1(l)=w2/c2(l), c(l)=1+l(cH-1); return interior lambda if present.
    w1,w2=w
    a=w1*(c2-1.0)-w2*(c1-1.0)
    b=w2-w1
    if abs(a)<TOL: return None
    x=b/a
    return x if TOL < x < 1.0-TOL else None

def main():
    positive=read_matrix(RESULTS/'capability_gap_positive_v2.csv')
    weights=read_vector(RESULTS/'capability_dispersion_weights_v2.csv')
    feasibility_base,costs_base=build_scenario(STATES,CAPABILITIES)
    cells=[(i,j) for i in range(len(STATES)) for j in range(len(CAPABILITIES))]
    points={0.0,1.0}
    bp=[]
    for a,(i,j) in enumerate(cells):
        for h,k in cells[a+1:]:
            x=crossover(costs_base[i][j],costs_base[h][k],(weights[j],weights[k]))
            if x is not None:
                points.add(x); bp.append((x,i,j,h,k))
    bp.sort()
    with (RESULTS/'convergence_active_set_breakpoints_v2.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f); w.writerow(['lambda','state_a','capability_a','state_b','capability_b','rank_crossover'])
        for x,i,j,h,k in bp: w.writerow([x,STATES[i],CAPABILITIES[j],STATES[h],CAPABILITIES[k],1])
    levels=sorted(points)
    rows=[]
    for level in levels:
        feasibility=tuple(tuple(1+level*(x-1) for x in row) for row in feasibility_base)
        costs=tuple(tuple(1+level*(x-1) for x in row) for row in costs_base)
        alloc=allocate_budget(positive,weights,feasibility,costs,BUDGET)
        active=[(i,j) for i,j in cells if alloc[i][j]>TOL]
        ranks=sorted(((weights[j]/costs[i][j],i,j) for i,j in cells if positive[i][j]*feasibility[i][j]>TOL),reverse=True)
        top=';'.join(f'{STATES[i]}:{CAPABILITIES[j]}' for _,i,j in ranks[:5])
        act=';'.join(f'{STATES[i]}:{CAPABILITIES[j]}' for i,j in active)
        rows.append((level,len(active),act,top))
    with (RESULTS/'convergence_active_set_path_v2.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f); w.writerow(['lambda','active_cell_count','active_cells','top_five_ranked_cells']); w.writerows(rows)
    print(f'Identified {len(bp)} interior ranking crossover points and {len(levels)} analysis levels.')
if __name__=='__main__': main()
