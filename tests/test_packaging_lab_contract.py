"""Focused regression checks for the packaging/provenance proposal."""
from pathlib import Path
import subprocess
import unittest
import re

import yaml


ROOT = Path(__file__).resolve().parents[1]


class PackagingLabContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = yaml.safe_load((ROOT / 'src/hay-spec.yaml').read_text())
        released = subprocess.check_output(
            ['git', 'show', 'v0.91.1:src/hay-spec.yaml'], cwd=ROOT, text=True)
        cls.released = yaml.safe_load(released)
        cls.sections = {s['id']: s for s in cls.spec['sections']}
        cls.pack = {f['id']: f for f in cls.sections['packaging']['fields']}
        cls.lab = {f['id']: f for f in cls.sections['nutrient_analysis']['fields']}

    def test_released_packaging_identifiers_and_enums_are_preserved(self):
        old = next(s for s in self.released['sections'] if s['id'] == 'packaging')
        for field in old['fields']:
            key = field['name']
            with self.subTest(field=key):
                self.assertEqual(self.pack[key]['name'], key)
                self.assertEqual(self.pack[key]['data_type'], field['data_type'])
                self.assertEqual(self.pack[key]['valid_values'], field['valid_values'])

    def test_packaging_identifiers_are_unique(self):
        ids = [f['id'] for f in self.sections['packaging']['fields']]
        self.assertEqual(len(ids), len(set(ids)))

    def test_supported_units_and_round_axis(self):
        self.assertEqual(self.pack['bale_weight_units']['valid_values'],
                         ['kilograms', 'pounds'])
        self.assertEqual(set(self.pack['bale_dimension_units']['valid_values']),
                         {'inches', 'centimeters', 'feet', 'meters'})
        self.assertEqual(self.pack['bale_dimension_axis']['data_type'], 'float')
        self.assertNotIn('valid_range', self.pack['bale_dimension_axis'])

    def test_provenance_does_not_make_historical_tests_invalid(self):
        for key in ['lab_sample_id', 'lab_report_reference',
                    'lab_processing_completed_date', 'lab_processing_notes',
                    'lab_quality_code']:
            with self.subTest(field=key):
                self.assertIn(key, self.lab)
                self.assertFalse(self.lab[key].get('required', False))
                self.assertNotIn('required_if', self.lab[key])
                self.assertNotIn('#NAME?', self.lab[key]['definition'])

    def test_other_sections_and_existing_lab_fields_are_unchanged(self):
        for old in self.released['sections']:
            if old['id'] not in {'packaging', 'nutrient_analysis'}:
                self.assertEqual(old, self.sections[old['id']])
            if old['id'] == 'nutrient_analysis':
                new_fields = self.sections[old['id']]['fields']
                old_ids = {f['id'] for f in old['fields']}
                self.assertEqual([f for f in new_fields if f['id'] in old_ids],
                                 old['fields'])

    def test_release_metadata_is_not_bumped(self):
        self.assertEqual(self.spec['version'], '0.91.1')
        self.assertEqual(self.spec['published_on'], '2025-08-31')

    def test_documented_examples_match_declared_fields_and_enums(self):
        notes = (ROOT / 'notes/packaging-lab-provenance.md').read_text()
        examples = re.findall(r'```yaml\n(.*?)```', notes, re.S)
        self.assertEqual(len(examples), 3)
        fields = {**self.pack, **self.lab}
        fields.update({f['id']: f for f in self.sections['harvest']['fields']})
        for example in examples:
            record = yaml.safe_load(example)
            for key, value in record.items():
                with self.subTest(field=key):
                    field = fields[key]
                    if isinstance(field.get('valid_values'), list):
                        self.assertIn(value, field['valid_values'])
                    if key.startswith('bale_dimension_') and key != 'bale_dimension_units':
                        self.assertGreater(value, 0)
                        self.assertIn('bale_dimension_units', record)
            if 'average_bale_weight' in record:
                self.assertIn('bale_weight_units', record)
            if 'lab_sample_id' in record:
                self.assertIsInstance(record['lab_sample_id'], str)
                self.assertTrue(record['lab_sample_id'].startswith('000'))


if __name__ == '__main__':
    unittest.main()
