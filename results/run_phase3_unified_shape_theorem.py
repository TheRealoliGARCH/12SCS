"""Phase III unified shape theorem synthesis from certified structural layers."""
from __future__ import annotations
import csv
from pathlib import Path

OUT = Path('results/phase3_unified_shape_theorem_v1.csv')
ROWS = [
 ('domain','F>-1','1+F lambda>0 on [0,1]','exact_domain'),
 ('first_derivative','Pi_prime=P/(1+F lambda)^2','critical points are roots of P','exact_identity'),
 ('curvature','Pi_second=2T/(1+F lambda)^3','sign(Pi_second)=sign(T)','exact_identity'),
 ('discriminant','Delta_P=4ST','root geometry is coupled to S and T','exact_identity'),
 ('convex_decrease','P<0 on [0,1] and T>0','strictly decreasing and strictly convex','necessary_and_sufficient_joint'),
 ('affine_decrease','P<0 on [0,1] and T=0','strictly decreasing and affine','necessary_and_sufficient_joint'),
 ('concave_decrease','P<0 on [0,1] and T<0','strictly decreasing and strictly concave','necessary_and_sufficient_joint'),
 ('global_root_exclusion','ST<0','P has no real roots and no critical points','exact_structural_exclusion'),
 ('zero_curvature_boundary','T=0','P=p0(1+F lambda)^2 and Pi_prime=p0','exact_structural_boundary'),
 ('primitive_pullback','T=E-FD+F^2C under the established primitive map','primitive curvature sign is the sign of the pullback','exact_primitive_pullback'),
 ('sharpness','realized primitive witnesses recorded where emitted','attainability is certified only for witnessed classes','constructive_sharpness'),
 ('scope','curvature or discriminant information alone does not imply decrease','P-sign condition remains required for monotonicity','scope_boundary'),
]
def main():
 with OUT.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=['analysis','theorem_component','condition','consequence','classification','inference_level']);w.writeheader()
  for c,a,b,d in ROWS:w.writerow({'analysis':'phase3_unified_shape_theorem','theorem_component':c,'condition':a,'consequence':b,'classification':d,'inference_level':'unified_shape_theorem'})
 print(OUT);print('PHASE3_UNIFIED_SHAPE_THEOREM_STATUS=PHASE3_UNIFIED_SHAPE_THEOREM_COMPLETE')
if __name__=='__main__':main()
