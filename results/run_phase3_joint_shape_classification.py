"""Phase III joint monotonicity-curvature structural classification."""
from __future__ import annotations

import csv
from pathlib import Path

OUTPUT = Path('results/phase3_joint_shape_classification_v1.csv')

ROWS = [
    ('domain', 'F>-1', 'denominators positive on [0,1]', 'domain'),
    ('discriminant_identity', 'Delta_P=4ST', 'root geometry coupled to S and T', 'exact_identity'),
    ('curvature_identity', "Pi_second=2T/(1+F*lambda)^3", 'curvature sign equals sign(T)', 'exact_identity'),
    ('convex_decrease', 'P<0 on [0,1] and T>0', 'strictly decreasing and strictly convex', 'necessary_and_sufficient_joint'),
    ('linear_decrease', 'P<0 on [0,1] and T=0', 'strictly decreasing and affine', 'necessary_and_sufficient_joint'),
    ('concave_decrease', 'P<0 on [0,1] and T<0', 'strictly decreasing and strictly concave', 'necessary_and_sufficient_joint'),
    ('concave_discriminant_exclusion', 'S<0 and T>0', 'Delta_P<0, so P has no real roots', 'exact_structural_exclusion'),
    ('convex_discriminant_exclusion', 'S>0 and T<0', 'Delta_P<0, so P has no real roots', 'exact_structural_exclusion'),
    ('double_root_boundary', 'S*T=0', 'Delta_P=0 boundary regime', 'exact_boundary'),
    ('shape_scope', 'joint classification requires exact P-sign condition for monotonicity', 'curvature alone does not imply decrease', 'scope_boundary'),
]


def main() -> None:
    with OUTPUT.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['analysis','theorem_component','statement','certificate','classification','inference_level'])
        w.writeheader()
        for component, statement, certificate, classification in ROWS:
            w.writerow({'analysis':'phase3_joint_shape_classification','theorem_component':component,'statement':statement,'certificate':certificate,'classification':classification,'inference_level':'joint_shape_classification'})
    print(OUTPUT)
    print('PHASE3_JOINT_SHAPE_CLASSIFICATION_STATUS=PHASE3_JOINT_SHAPE_CLASSIFICATION_COMPLETE')

if __name__ == '__main__':
    main()
