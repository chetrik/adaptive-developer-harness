"""Strict, local-only contracts; no remote schema resolution."""
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
VERSION = '0.2.0'
POLICY = '1.0'

class HarnessError(ValueError):
    pass

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)

def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode('utf-8')).hexdigest()

def fingerprint(value):
    return digest(canonical(value))

def validate(kind, value):
    schema = json.loads((ROOT / 'schemas' / (kind + '.schema.json')).read_text())
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda e: str(list(e.path)))
    if errors:
        # Do not echo rejected values (they might contain confidential material).
        e = errors[0]
        raise HarnessError(f'{kind}: invalid {"/".join(map(str,e.path)) or "root"} ({e.validator})')
    return value

def read_json(path):
    def pairs(items):
        out = {}
        for k, v in items:
            if k in out:
                raise HarnessError('Duplicate JSON key')
            out[k] = v
        return out
    def invalid(_):
        raise HarnessError('Non-finite JSON number')
    try:
        return json.loads(Path(path).read_text(), object_pairs_hook=pairs, parse_constant=invalid)
    except (OSError, ValueError) as exc:
        raise HarnessError('Cannot read valid JSON: ' + str(path)) from exc

def fact_value(assessment, name):
    fact = assessment['facts'][name]
    # Inference is useful for conservative selection, never proof of absence.
    if fact['basis'] in ('unknown', 'inferred') and fact['value'] is False:
        return 'unknown'
    return fact['value']

def confirmed(cap):
    return cap['value'] is True and cap['basis'] in ('observed', 'user-confirmed') and bool(cap['sources'])
