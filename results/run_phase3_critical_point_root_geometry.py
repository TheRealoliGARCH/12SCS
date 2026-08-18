"""Phase III critical-point and root-geometry theorem."""
from __future__ import annotations

import csv
from pathlib import Path

OUTPUT = Path('results/phase3_critical_point_root_geometry_v1.csv')

ROWS = [
    ('domain', 'F>-1', 'critical points are roots of P because denominator is positive', 'established_domain_condition'),
    ('critical_point_equation', 'P(lambda)=p0+2S*lambda+FS*lambda^2=0', 'exact critical-point equation', 'exact_identity'),
    ('discriminant', 'Delta_P=4ST', 'real-root geometry determined by sign(ST)', 'exact_identity'),
    ('global_root_exclusion', 'ST<0', 'Delta_P<0, hence no real roots and no critical points', 'necessary_and_sufficient_discriminant_regime'),
    ('double_root_regime', 'ST=0', 'Delta_P=0, with degenerate subcases requiring coefficient interpretation', 'exact_boundary'),
    ('two_real_root_regime', 'ST>0', 'Delta_P>0, subject to quadratic nondegeneracy, two distinct real roots', 'necessary_and_sufficient_discriminant_regime'),
    ('root_formula', 'lambda=(-S plus_or_minus sqrt(S*T))/(F*S)', 'valid when F*S!=0 and ST>=0', 'exact_identity'),
    ('interval_critical_point', 'root lies in (0,1)', 'interior criticality requires exact interval membership', 'necessary_and_sufficient_interval_condition'),
    ('T_zero_shape_boundary', 'T=0', 'curvature vanishes identically and P=p0*(1+F*lambda)^2', 'exact_structural_boundary'),
    ('scope', 'discriminant classifies real roots; interval membership remains separate', 'no claim that ST>0 alone creates an interior critical point', 'scope_boundary'),
]

def main() -> None:
    with OUTPUT.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['analysis','theorem_component','statement','certificate','classification','inference_level'])
        w.writeheader()
        for component, statement, certificate, classification in ROWS:
            w.writerow({'analysis':'phase3_critical_point_root_geometry','theorem_component':component,'statement':statement,'certificate':certificate,'classification':classification,'inference_level':'critical_point_root_geometry'})
    print(OUTPUT)
    print('PHASE3_CRITICAL_POINT_ROOT_GEOMETRY_STATUS=PHASE3_CRITICAL_POINT_ROOT_GEOMETRY_COMPLETE')

if __name__ == '__main__':
    main()
