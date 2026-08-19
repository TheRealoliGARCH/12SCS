from pathlib import Path
import csv
import hashlib
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
OUT = ROOT / 'results'
MANIFEST = DATA / 'data_acquisition_provenance_manifest_v1.csv'


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    files = sorted(p for p in DATA.glob('*.csv') if p.name not in {'data_acquisition_provenance_manifest_v1.csv'})
    inventory = []
    for p in files:
        with p.open(newline='', encoding='utf-8') as f:
            rows = list(csv.reader(f))
        inventory.append({'filename': p.name, 'sha256': sha256(p), 'row_count': max(len(rows)-1, 0), 'column_count': len(rows[0]) if rows else 0})

    with MANIFEST.open(newline='', encoding='utf-8') as f:
        manifest = list(csv.DictReader(f))
    populated = [r for r in manifest if r.get('dataset_id') != 'TEMPLATE-001' and r.get('raw_filename')]
    manifest_by_file = {r['raw_filename']: r for r in populated}
    checksum_results = []
    for item in inventory:
        row = manifest_by_file.get(item['filename'])
        declared = row.get('raw_sha256', '') if row else ''
        checksum_results.append({'filename': item['filename'], 'declared': bool(declared), 'match': bool(declared) and declared == item['sha256']})

    required_dimensions = {'N','M','E','F','T','I','R','H','L','D','A','S'}
    dimension_files = [p for p in files if p.name not in {'capability_dimensions.csv','capability_recognition.csv','evidence_ledger.csv'}]
    present_dimensions = set()
    duplicate_rows = 0
    for p in dimension_files:
        with p.open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        if rows:
            for key in ('dimension','primitive','capability'):
                if key in rows[0]:
                    present_dimensions.update(r.get(key,'') for r in rows)
                    break
        if rows and 'state' in rows[0] and any(k in rows[0] for k in ('dimension','primitive','capability')):
            keyname = next(k for k in ('dimension','primitive','capability') if k in rows[0])
            seen = set()
            for r in rows:
                key = (r.get('state'), r.get(keyname))
                if key in seen: duplicate_rows += 1
                seen.add(key)

    report = {
        'audit_timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'repository_data_file_count': len(files),
        'inventory': inventory,
        'manifest': {'total_rows': len(manifest), 'populated_rows': len(populated), 'unrepresented_files': [x['filename'] for x in inventory if x['filename'] not in manifest_by_file]},
        'checksum': {'declared_count': sum(x['declared'] for x in checksum_results), 'verified_count': sum(x['match'] for x in checksum_results), 'results': checksum_results},
        'coverage': {'required_dimensions': sorted(required_dimensions), 'observed_dimension_codes': sorted(x for x in present_dimensions if x), 'dimension_schema_complete': required_dimensions.issubset(present_dimensions)},
        'duplicates': {'detected_state_dimension_duplicates': duplicate_rows},
    }
    report['freeze_decision'] = 'PASS' if report['manifest']['populated_rows'] > 0 and not report['manifest']['unrepresented_files'] and report['checksum']['declared_count'] == len(inventory) and report['checksum']['verified_count'] == len(inventory) and report['coverage']['dimension_schema_complete'] and duplicate_rows == 0 else 'BLOCKED'
    (OUT / 'data_freeze_audit_report_v1.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'freeze_decision': report['freeze_decision'], 'files': len(files), 'populated_manifest_rows': len(populated), 'checksum_verified': report['checksum']['verified_count']}, indent=2))

if __name__ == '__main__':
    main()
