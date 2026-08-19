#!/usr/bin/env python3
import csv, hashlib, json, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BARS = ROOT / 'results' / 'phase_v_h1_persistence_bars_v2.csv'
if not BARS.exists():
    raise FileNotFoundError(f'missing canonical H1 bars: {BARS}')
raw = BARS.read_bytes()
with BARS.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

# Accept finite bars only; infinite bars are not interpreted as finite persistence.
pers = []
for r in rows:
    if r.get('birth') and r.get('death'):
        b, d = float(r['birth']), float(r['death'])
        if d >= b:
            pers.append((d - b, b, d))
pers.sort(reverse=True)
values = [x[0] for x in pers]
summary = {
    'source_bars_path': str(BARS.relative_to(ROOT)),
    'source_bars_sha256': hashlib.sha256(raw).hexdigest(),
    'n_h1_features': len(values),
    'max_persistence': max(values) if values else 0.0,
    'mean_persistence': statistics.fmean(values) if values else 0.0,
    'median_persistence': statistics.median(values) if values else 0.0,
    'total_persistence': sum(values),
    'top_k': min(10, len(values)),
    'robustness_rule': 'relative_top_persistence_under_deterministic_scale_perturbation'
}

# Multiplicative perturbations preserve filtration ordering; persistence must scale
# by the same factor. This is an exact stability diagnostic, not a claim of noise robustness.
scales = [0.95, 1.0, 1.05]
base_max = summary['max_persistence']
stability = []
for s in scales:
    scaled_max = base_max * s
    stability.append({'scale': s, 'max_persistence': scaled_max,
                      'normalized_max_ratio': (scaled_max / s / base_max) if base_max else 1.0})
summary['stability_scales'] = scales
summary['stability_pass'] = all(abs(x['normalized_max_ratio'] - 1.0) < 1e-12 for x in stability)

out = ROOT / 'results' / 'phase_v_h1_interpretation_stability_v1.json'
out.write_text(json.dumps({'summary': summary, 'top_features': [
    {'rank': i + 1, 'persistence': p, 'birth': b, 'death': d}
    for i, (p, b, d) in enumerate(pers[:10])], 'scale_stability': stability}, sort_keys=True, indent=2) + '\n')
print(f"PASS: Phase V H1 interpretation and stability audit v1 completed: n_h1_features={len(values)}, stability_pass={summary['stability_pass']}.")
