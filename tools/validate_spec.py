"""Validate specification structure, not hay records or scientific plausibility."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re
import sys

import yaml


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f'duplicate YAML key: {key!r}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def load_spec(text):
    return yaml.load(text, Loader=UniqueKeyLoader)


def inspect_spec(spec):
    findings = []

    def report(code, path, message, severity='error'):
        findings.append(dict(code=code, path=path, message=message, severity=severity))

    def collection(items, path):
        if not isinstance(items, list):
            report('collection_type', path, 'Expected a list of field definitions.')
            return
        identities = []
        for i, node in enumerate(items):
            here = f'{path}/{i}'
            if not isinstance(node, dict):
                report('field_type', here, 'Expected a field mapping.')
                continue
            identity = node.get('id', node.get('name'))
            if not isinstance(identity, str) or not identity:
                report('missing_id', here, 'Expected a nonempty id or legacy name.')
            else:
                identities.append(identity)
                if not re.fullmatch(r'[a-z][a-z0-9]*(?:_[a-z0-9]+)*', identity):
                    report('legacy_identifier', here, identity, 'warning')
            if 'id' in node and 'name' in node and node['id'] != node['name']:
                report('alias_mismatch', here, 'id and name must match.')
            if 'required' in node and type(node['required']) is not bool:
                report('required_type', here, 'required must be a boolean.')
            values = node.get('valid_values')
            if isinstance(values, list):
                tokens = []
                for v in values:
                    if not isinstance(v, (str, bool, int, float)) or v is None:
                        report('enum_value_type', here, 'Enum entries must be scalar values.')
                        continue
                    tokens.append((type(v).__name__, str(v)))
                    if isinstance(v, str) and ('`' in v or '|' in v):
                        report('legacy_enum_literal', here, v, 'warning')
                if len(tokens) != len(set(tokens)):
                    report('duplicate_enum', here, 'Duplicate enum entries.')
            bounds = node.get('valid_range')
            if bounds is not None:
                if not isinstance(bounds, dict) or not bounds or set(bounds) - {'min', 'max'}:
                    report('range_shape', here, 'Expected min and/or max bounds.')
                elif any(type(v) not in (int, float) or not math.isfinite(v)
                         for v in bounds.values()):
                    report('range_number', here, 'Bounds must be finite numbers, not booleans.')
                elif 'min' in bounds and 'max' in bounds and bounds['min'] > bounds['max']:
                    report('range_order', here, 'min exceeds max.')
                if node.get('data_type') not in ('int', 'float'):
                    report('range_type', here, 'Numeric bounds require int or float data_type.')
            for key in ('fields', 'components', 'groups', 'subsections'):
                if key in node:
                    collection(node[key], f'{here}/{key}')
        for identity, count in Counter(identities).items():
            if count > 1:
                report('duplicate_identifier', path, f'{identity}: {count} definitions', 'warning')

    if not isinstance(spec, dict) or 'sections' not in spec:
        report('root', '/', 'Expected a specification mapping containing sections.')
    else:
        collection(spec['sections'], '/sections')
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('spec', type=Path)
    parser.add_argument('--baseline', type=Path)
    args = parser.parse_args()
    try:
        findings = inspect_spec(load_spec(args.spec.read_text()))
        baseline = json.loads(args.baseline.read_text()) if args.baseline else []
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f'Specification validation failed: {exc}', file=sys.stderr)
        return 1
    errors = [f for f in findings if f['severity'] == 'error']
    warnings = [f for f in findings if f['severity'] == 'warning']
    new = [f for f in warnings if f not in baseline]
    stale = [f for f in baseline if f not in warnings]
    print(json.dumps(findings, indent=2))
    if args.baseline and stale:
        print('Baseline contains resolved or moved warnings; review and update it.', file=sys.stderr)
    print(f'{len(errors)} errors; {len(warnings)} legacy warnings; '
          f'{len(new)} unacknowledged warnings.')
    return int(bool(errors or (args.baseline and (new or stale))))


if __name__ == '__main__':
    sys.exit(main())
