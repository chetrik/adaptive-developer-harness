#!/usr/bin/env python3
"""Validate installed harness integrity. Does not certify the application's security."""
import hashlib
import json
from pathlib import Path
import sys


def check(root):
    errors = []
    home = root / '.adaptive-harness'
    manifest_path = home / 'manifest.json'
    if home.is_symlink() or manifest_path.is_symlink():
        return ['Unsafe manifest path']
    try:
        manifest = json.loads(manifest_path.read_text())
        if manifest['schema_version'] not in ('1.0','2.0') or not manifest['files']:
            return ['Invalid manifest']
        for name, expected in manifest['files'].items():
            rel = Path(name)
            if rel.is_absolute() or '..' in rel.parts or not rel.parts:
                errors.append('Unsafe path')
                continue
            path = root
            for part in rel.parts:
                path = path / part
                if path.is_symlink():
                    errors.append('Symlink: ' + name)
                    break
            else:
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    errors.append('Missing or changed: ' + name)
        for name in manifest['files']:
            if name not in manifest['provenance']:
                errors.append('Missing provenance: ' + name)
        if not (home / 'LICENSE').is_file():
            errors.append('Missing license')
    except (OSError, ValueError, KeyError, TypeError):
        errors.append('Cannot read valid manifest')
    return errors

if __name__ == '__main__':
    errors = check(Path(__file__).resolve().parents[1])
    for error in errors:
        print(error)
    print('Harness integrity: ' + ('FAIL' if errors else 'PASS'))
    print('Application tests, native Skill discovery and security review: NOT VERIFIED by this checker.')
    sys.exit(1 if errors else 0)
