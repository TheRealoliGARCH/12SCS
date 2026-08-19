import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / 'results'
SUMMARY = RESULTS / 'perturbation_sensitivity_v1.csv'
METADATA = RESULTS / 'perturbation_sensitivity_v1_metadata.csv'
EXPECTED_SCENARIOS = 5000
EXPECTED_SEED = '12000'
EXPECTED_SCALE = '0.1'


def read_rows(path):
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def fail(message):
    raise AssertionError(message)


summary_rows = read_rows(SUMMARY)
metadata_rows = read_rows(METADATA)

if not summary_rows:
    fail('summary file is empty')
if not metadata_rows:
    fail('metadata file is empty')

metadata_key = next((k for k in ('parameter', 'key', 'metric') if k in metadata_rows[0]), None)
if metadata_key is None or 'value' not in metadata_rows[0]:
    fail(f"unexpected metadata schema: {list(metadata_rows[0])}")
metadata = {r[metadata_key]: r['value'] for r in metadata_rows}

if metadata.get('seed') != EXPECTED_SEED:
    fail(f"seed mismatch: {metadata.get('seed')}")
if metadata.get('scenarios') != str(EXPECTED_SCENARIOS):
    fail(f"scenario mismatch: {metadata.get('scenarios')}")
if metadata.get('scale') != EXPECTED_SCALE:
    fail(f"scale mismatch: {metadata.get('scale')}")

summary_metric_key = next((k for k in ('metric', 'category') if k in summary_rows[0]), None)
if summary_metric_key is None or 'count' not in summary_rows[0]:
    fail(f"unexpected summary schema: {list(summary_rows[0])}")

for metric in ('closest_pair', 'most_central', 'most_peripheral'):
    rows = [r for r in summary_rows if r[summary_metric_key] == metric]
    if not rows:
        fail(f'missing summary category: {metric}')
    if sum(int(r['count']) for r in rows) != EXPECTED_SCENARIOS:
        fail(f'{metric} counts do not sum to {EXPECTED_SCENARIOS}')

item_key = 'item' if 'item' in summary_rows[0] else 'category'
closest = {r[item_key] for r in summary_rows if r[summary_metric_key] == 'closest_pair'}
allowed_closest = {'United Kingdom -- France', 'United States -- China'}
if not closest or not closest.issubset(allowed_closest):
    fail(f'unexpected closest-pair categories: {sorted(closest)}')

peripheral = [r for r in summary_rows if r[summary_metric_key] == 'most_peripheral']
if len(peripheral) != 1:
    fail(f'expected one peripheral category, found {len(peripheral)}')
if peripheral[0][item_key] != 'North Korea':
    fail(f"unexpected peripheral state: {peripheral[0][item_key]}")
if int(peripheral[0]['count']) != EXPECTED_SCENARIOS:
    fail('North Korea is not peripheral in every scenario')

print('PASS: perturbation sensitivity v1 metadata and stability invariants verified.')
