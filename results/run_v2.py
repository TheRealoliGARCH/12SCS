from pathlib import Path
import sys

# Make the repository root importable when this script is invoked directly,
# e.g. ``python results/run_v2.py``.  Python otherwise places only the
# ``results/`` directory on sys.path.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from model.evidence_adjusted_convergence import (
    convergence_index,
    global_dispersion,
    load_evidence_adjusted_matrix,
    pairwise_euclidean,
    write_distance_csv,
    write_matrix_csv,
)

DATA = ROOT / "data"
OUT = ROOT / "results"

states, capabilities, scores, confidence, coverage = load_evidence_adjusted_matrix(DATA, strict=True)
distances = pairwise_euclidean(scores)
write_matrix_csv(states, capabilities, scores, OUT / "capability_latent_matrix_v2.csv")
write_distance_csv(states, distances, OUT / "capability_distance_matrix_v2.csv")

with (OUT / "capability_convergence_diagnostics_v2.csv").open("w", encoding="utf-8") as fh:
    fh.write("metric,value\n")
    fh.write(f"global_weighted_dispersion,{global_dispersion(scores, confidence):.12f}\n")
    fh.write(f"weighted_convergence_index,{convergence_index(scores, confidence):.12f}\n")
    fh.write("n_states,12\n")
    fh.write("n_capabilities,12\n")

with (OUT / "capability_confidence_matrix_v2.csv").open("w", encoding="utf-8") as fh:
    fh.write("state," + ",".join(capabilities) + "\n")
    for state, row in zip(states, confidence):
        fh.write(state + "," + ",".join(f"{x:.6f}" for x in row) + "\n")

with (OUT / "capability_coverage_v2.csv").open("w", encoding="utf-8") as fh:
    fh.write("state," + ",".join(capabilities) + "\n")
    for state, row in zip(states, coverage):
        fh.write(state + "," + ",".join(str(x) for x in row) + "\n")
