from pathlib import Path
import csv
import math
import random
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results"
SEED = 12_000
SCENARIOS = 5_000
SCALE = 0.10


def read_matrix(path):
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    header = rows[0][1:]
    states = [r[0] for r in rows[1:]]
    values = [[float(x) for x in r[1:]] for r in rows[1:]]
    return states, header, values


def pairwise_distances(scores):
    n = len(scores)
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = math.sqrt(sum((a - b) ** 2 for a, b in zip(scores[i], scores[j])))
            out[i][j] = out[j][i] = d
    return out


def argmin_pair(distances):
    best = None
    for i in range(len(distances)):
        for j in range(i + 1, len(distances)):
            candidate = (distances[i][j], i, j)
            if best is None or candidate < best:
                best = candidate
    return best[1], best[2]


def most_central(distances):
    means = [sum(row) / (len(row) - 1) for row in distances]
    return min(range(len(means)), key=lambda i: (means[i], i))


def most_peripheral(distances):
    means = [sum(row) / (len(row) - 1) for row in distances]
    return max(range(len(means)), key=lambda i: (means[i], -i))


states, capabilities, scores = read_matrix(DATA / "capability_latent_matrix_v2.csv")
c_states, c_capabilities, confidence = read_matrix(DATA / "capability_confidence_matrix_v2.csv")
if states != c_states or capabilities != c_capabilities:
    raise AssertionError("latent and confidence matrices are not aligned")

rng = random.Random(SEED)
closest = Counter()
central = Counter()
peripheral = Counter()

for _ in range(SCENARIOS):
    perturbed = []
    for score_row, confidence_row in zip(scores, confidence):
        row = []
        for x, c in zip(score_row, confidence_row):
            radius = SCALE * (1.0 - c)
            row.append(min(1.0, max(0.0, x + rng.uniform(-radius, radius))))
        perturbed.append(row)
    distances = pairwise_distances(perturbed)
    i, j = argmin_pair(distances)
    closest[(states[i], states[j])] += 1
    central[states[most_central(distances)]] += 1
    peripheral[states[most_peripheral(distances)]] += 1

out = DATA / "perturbation_sensitivity_v1.csv"
with out.open("w", newline="", encoding="utf-8") as fh:
    writer = csv.writer(fh)
    writer.writerow(["category", "item", "count", "share"])
    for category, counter in (("closest_pair", closest), ("most_central", central), ("most_peripheral", peripheral)):
        for item, count in sorted(counter.items(), key=lambda kv: (-kv[1], str(kv[0]))):
            label = " -- ".join(item) if isinstance(item, tuple) else item
            writer.writerow([category, label, count, f"{count / SCENARIOS:.12f}"])

with (DATA / "perturbation_sensitivity_v1_metadata.csv").open("w", newline="", encoding="utf-8") as fh:
    writer = csv.writer(fh)
    writer.writerow(["parameter", "value"])
    writer.writerow(["seed", SEED])
    writer.writerow(["scenarios", SCENARIOS])
    writer.writerow(["scale", SCALE])
    writer.writerow(["distribution", "Uniform[-scale*(1-confidence), +scale*(1-confidence)]"])
    writer.writerow(["clipping", "[0,1]"])
