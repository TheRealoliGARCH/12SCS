# Version 2 Results Protocol

The v2 result set must contain, at minimum:

- `capability_latent_matrix_v2.csv`: $z_{ij}$ latent capability scores;
- `capability_confidence_matrix_v2.csv`: $C_{ij}$ evidence weights;
- `capability_coverage_v2.csv`: number of latent components supplied per cell;
- `capability_distance_matrix_v2.csv`: Euclidean distances between latent capability vectors;
- `capability_convergence_diagnostics_v2.csv`: weighted dispersion and convergence diagnostics.

No v2 headline statistic should be reported until the strict loader has successfully consumed all 144 State-capability cells.

The v2 estimate must always be compared against v1 rather than replacing it silently. The difference between the two estimators is itself a robustness diagnostic.
