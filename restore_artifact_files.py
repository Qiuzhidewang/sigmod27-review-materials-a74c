#!/usr/bin/env python3
"""Restore compressed frozen records before offline reproduction (standard library only)."""
import gzip
import hashlib
import json
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parent


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def local_path(name):
    path = (ROOT / name).resolve()
    if path == ROOT or ROOT not in path.parents:
        raise ValueError('Invalid restoration path')
    return path


def main():
    records = json.loads((ROOT / 'PACKED_FILES.json').read_text())
    restored = 0
    for record in records:
        destination = local_path(record['path'])
        compressed = local_path(record['gzip_path'])
        if digest(compressed) != record['gzip_sha256']:
            raise ValueError('Compressed record changed: ' + record['gzip_path'])
        if destination.exists():
            if digest(destination) != record['sha256']:
                raise ValueError('Existing file differs; refusing to overwrite: ' + record['path'])
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as out:
                temporary = Path(out.name)
                size = 0
                with gzip.open(compressed, 'rb') as incoming:
                    for block in iter(lambda: incoming.read(1024 * 1024), b''):
                        size += len(block)
                        if size > record['size']:
                            raise ValueError('Expanded record exceeds its declared size')
                        out.write(block)
            if size != record['size'] or digest(temporary) != record['sha256']:
                raise ValueError('Restored record failed verification: ' + record['path'])
            temporary.replace(destination)
            temporary = None
            restored += 1
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    print(f'Verified {len(records)} compressed records; restored {restored} files. No network access used.')


if __name__ == '__main__':
    main()
