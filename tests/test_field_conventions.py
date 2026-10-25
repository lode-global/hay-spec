"""Adversarial structure checks and compatibility with the merged PR #4."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.validate_spec import inspect_spec, load_baseline, load_spec
from compatibility_helpers import restore_previous_nutrient_definitions


ROOT = Path(__file__).resolve().parents[1]
BASE = '7fb9083d0234e7d8ca8a5d8bd63867e23468331e'


class FieldConventions(unittest.TestCase):
    def field_spec(self, **field):
        return {'sections': [{'id': 'sample', 'fields': [field]}]}

    def codes(self, spec):
        return {f['code'] for f in inspect_spec(spec)}

    def test_duplicate_yaml_keys_are_not_silently_overwritten(self):
        with self.assertRaisesRegex(ValueError, 'duplicate YAML key'):
            load_spec('sections: []\nsections: []\n')

    def test_unhashable_yaml_mapping_keys_report_a_validation_error(self):
        with self.assertRaisesRegex(ValueError, 'mapping keys'):
            load_spec('? [a, b]\n: value\n')

    def test_malformed_baselines_are_rejected(self):
        for baseline in [None, {}, 'warnings', [None], [{'code': 'partial'}]]:
            with self.subTest(baseline=baseline), self.assertRaises(ValueError):
                load_baseline(json.dumps(baseline))
        finding = dict(code='x', path='/', message='example', severity='warning')
        with self.assertRaisesRegex(ValueError, 'duplicate entries'):
            load_baseline(json.dumps([finding, finding]))

    def test_malformed_values_and_explicit_null_ranges_fail(self):
        for value in [None, {}, 123, False]:
            with self.subTest(value=value):
                self.assertIn('values_shape', self.codes(
                    self.field_spec(id='value', valid_values=value)))
        self.assertIn('range_shape', self.codes(self.field_spec(
            id='value', data_type='float', valid_range=None)))
        self.assertIn('enum_value_number', self.codes(self.field_spec(
            id='value', valid_values=[float('nan')])))

    def test_large_integer_bounds_do_not_overflow(self):
        self.assertEqual(inspect_spec(self.field_spec(
            id='value', data_type='int', valid_range={'min': 0, 'max': 10 ** 400})), [])

    def test_mismatched_aliases_fail(self):
        self.assertIn('alias_mismatch', self.codes(
            self.field_spec(id='weight', name='mass')))

    def test_name_only_legacy_fields_still_work(self):
        self.assertEqual(inspect_spec(self.field_spec(name='weight')), [])

    def test_typical_prose_ranges_do_not_become_constraints(self):
        spec = self.field_spec(id='weight', data_type='float',
                               valid_values='Typically 10 to 20; other values occur.')
        self.assertEqual(inspect_spec(spec), [])

    def test_enum_values_keep_boolean_number_and_string_distinct(self):
        self.assertEqual(inspect_spec(self.field_spec(
            id='status', valid_values=[True, 1, 'true', False, 0, 'false'])), [])

    def test_duplicate_and_formatted_enum_values_are_detected(self):
        codes = self.codes(self.field_spec(id='status', valid_values=['a', 'a', '`b`']))
        self.assertIn('duplicate_enum', codes)
        self.assertIn('legacy_enum_literal', codes)

    def test_invalid_numeric_constraints_fail(self):
        for bounds, kind, expected in [
            ({'min': 3, 'max': 2}, 'float', 'range_order'),
            ({'min': True}, 'int', 'range_number'),
            ({'max': float('inf')}, 'float', 'range_number'),
            ({'min': 0}, 'string', 'range_type'),
            ({'minimum': 0}, 'float', 'range_shape'),
        ]:
            with self.subTest(bounds=bounds):
                self.assertIn(expected, self.codes(self.field_spec(
                    id='value', data_type=kind, valid_range=bounds)))

    def test_required_false_is_valid_but_string_false_is_not(self):
        self.assertEqual(inspect_spec(self.field_spec(id='value', required=False)), [])
        self.assertIn('required_type', self.codes(
            self.field_spec(id='value', required='false')))

    def test_identity_scope_does_not_flatten_components(self):
        spec = {'sections': [{'id': 'example', 'fields': [
            {'id': 'first', 'components': [{'id': 'value'}]},
            {'id': 'second', 'components': [{'id': 'value'}]},
        ]}]}
        self.assertEqual(inspect_spec(spec), [])
        spec['sections'][0]['fields'].append(copy.deepcopy(spec['sections'][0]['fields'][0]))
        self.assertIn('duplicate_identifier', self.codes(spec))

    def test_all_existing_section_content_is_preserved(self):
        current = load_spec((ROOT / 'src/hay-spec.yaml').read_text())
        previous = load_spec(subprocess.check_output(
            ['git', 'show', f'{BASE}:src/hay-spec.yaml'], cwd=ROOT, text=True))
        # The handling replacement only adds optional components and guidance.
        normalized = restore_previous_nutrient_definitions(
            current['sections'], previous['sections'])
        for section in normalized:
            for field in section.get('fields', []):
                if field.get('id') == 'handling_events':
                    field.pop('components', None)
                    field.pop('guidance', None)
        self.assertEqual(normalized, previous['sections'])
        self.assertEqual(current['version'], previous['version'])
        self.assertEqual(current['published_on'], previous['published_on'])

    def test_legacy_findings_are_explicit_and_exact(self):
        current = load_spec((ROOT / 'src/hay-spec.yaml').read_text())
        baseline = json.loads((ROOT / 'tests/legacy-spec-warnings.json').read_text())
        self.assertEqual(inspect_spec(current), baseline)
        self.assertEqual(len(baseline), 9)
        current['sections'][0]['fields'].append({'id': 'new%identifier'})
        self.assertNotEqual(inspect_spec(current), baseline)

    def test_cli_rejects_new_stale_and_error_baselines(self):
        cases = [
            (self.field_spec(id='new%identifier'), []),
            (self.field_spec(id='valid'), [{'code': 'stale'}]),
            (self.field_spec(id='weight', name='mass'), None),
        ]
        for spec, baseline in cases:
            with self.subTest(spec=spec), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp)
                # JSON is a valid YAML subset and preserves scalar types here.
                (path / 'spec.yaml').write_text(json.dumps(spec))
                (path / 'baseline.json').write_text(json.dumps(
                    inspect_spec(spec) if baseline is None else baseline))
                result = subprocess.run([
                    sys.executable, str(ROOT / 'tools/validate_spec.py'),
                    str(path / 'spec.yaml'), '--baseline', str(path / 'baseline.json'),
                ], capture_output=True, text=True)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
