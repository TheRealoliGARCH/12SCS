"""Generate SHA-256 hashes for the certified 12SCCM v2 package.

Usage from repository root:
    python reproducibility/HASH_MANIFEST.py
"""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "reproducibility" / "INPUT_MANIFEST.csv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    rows = []
    with MANIFEST.open("r", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            path = ROOT / row["path"]
            if not path.is_file():
                raise FileNotFoundError(path)
            rows.append((row["path"], row["role"], sha256(path), path.stat().st_size))

    print("path,role,sha256,size_bytes")
    for path, role, digest, size in rows:
        print(f'"{path}","{role}",{digest},{size}')


if __name__ == "__main__":
    main()
