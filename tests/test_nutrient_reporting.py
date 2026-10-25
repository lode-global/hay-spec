"""Compatibility with merged PR #6 and optional laboratory moisture reporting."""
import copy
import json
from pathlib import Path
import re
import subprocess
import unittest

from compatibility_helpers import restore_previous_nutrient_definitions, restore_previous_release_metadata
from tools.generate_docs import outputs
from tools.validate_spec import inspect_spec, load_spec


ROOT = Path(__file__).resolve().parents[1]
BASE = '21962fae7def1d24a1df2d218005f273afca8ae3'


class NutrientReporting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = load_spec((ROOT / 'src/hay-spec.yaml').read_text())
        cls.previous = load_spec(subprocess.check_output([
            'git', 'show', f'{BASE}:src/hay-spec.yaml'], cwd=ROOT, text=True))
        cls.fields = next(s for s in cls.spec['sections']
                          if s['id'] == 'nutrient_analysis')['fields']

    def test_exact_scope_of_compatibility_changes(self):
        current = restore_previous_release_metadata(self.spec, self.previous)
        current['sections'] = restore_previous_nutrient_definitions(
            current['sections'], self.previous['sections'])
        self.assertEqual(current, self.previous)

    def test_single_existing_dry_matter_key_retains_fuller_definition(self):
        current = [f for f in self.fields if f['id'] == 'dry_matter']
        previous = next(s for s in self.previous['sections']
                        if s['id'] == 'nutrient_analysis')['fields']
        old = [f for f in previous if f['id'] == 'dry_matter']
        self.assertEqual(len(old), 2)
        self.assertEqual(len(current), 1)
        surviving = {k: v for k, v in current[0].items() if k != 'guidance'}
        self.assertEqual(surviving, old[1])

    def test_moisture_is_optional_with_only_percentage_bounds(self):
        moisture = next(f for f in self.fields if f['id'] == 'moisture_content')
        self.assertIs(moisture['required'], False)
        self.assertNotIn('required_if', moisture)
        self.assertEqual(moisture['data_type'], 'float')
        self.assertEqual(moisture['valid_range'], {'min': 0, 'max': 100})

    def test_compatibility_normalization_does_not_hide_dry_matter_edits(self):
        changed = copy.deepcopy(self.spec['sections'])
        fields = next(s for s in changed if s['id'] == 'nutrient_analysis')['fields']
        next(f for f in fields if f['id'] == 'dry_matter')['data_type'] = 'string'
        with self.assertRaisesRegex(ValueError, 'retained dry-matter definition'):
            restore_previous_nutrient_definitions(changed, self.previous['sections'])

    def test_compatibility_normalization_rejects_duplicate_or_required_moisture(self):
        for duplicate in (True, False):
            changed = copy.deepcopy(self.spec['sections'])
            fields = next(s for s in changed if s['id'] == 'nutrient_analysis')['fields']
            moisture = next(f for f in fields if f['id'] == 'moisture_content')
            if duplicate:
                fields.append(copy.deepcopy(moisture))
            else:
                moisture['required'] = True
            with self.subTest(duplicate=duplicate), self.assertRaises(ValueError):
                restore_previous_nutrient_definitions(changed, self.previous['sections'])

    def test_legacy_and_new_record_examples_keep_numeric_types(self):
        notes = (ROOT / 'notes/nutrient-reporting-consistency.md').read_text()
        records = [load_spec(s) for s in re.findall(r'```yaml\n(.*?)```', notes, re.S)]
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]['moisture_content'] + records[0]['dry_matter'], 100)
        self.assertNotIn('moisture_content', records[1])
        self.assertIsInstance(records[1]['dry_matter'], float)
        self.assertEqual(records[0]['lab_sample_id'], '000123-A')

    def test_only_resolved_duplicate_warning_is_removed(self):
        old = inspect_spec(self.previous)
        current = inspect_spec(self.spec)
        removed = [f for f in old if f not in current]
        self.assertEqual(len(removed), 1)
        self.assertEqual(removed[0]['code'], 'duplicate_identifier')
        self.assertIn('dry_matter', removed[0]['message'])
        self.assertEqual([f for f in current if f not in old], [])

    def test_existing_protein_keys_are_not_renamed(self):
        ids = [f['id'] for f in self.fields]
        for prefix in ('soluble_protein', 'degradable_protein'):
            self.assertIn(prefix + '_%_cp', ids)
            self.assertNotIn(prefix + '_pct_cp', ids)

    def test_generated_source_keeps_legacy_record_identifiers(self):
        pages = outputs((ROOT / 'src/hay-spec.yaml').read_text())
        self.assertEqual(json.loads(pages['source/hay-spec.json']), self.spec)
        page = pages['fields/nutrient_analysis.md']
        self.assertEqual(page.count('Identifier: `dry_matter`'), 1)
        self.assertEqual(page.count('Identifier: `moisture_content`'), 1)


if __name__ == '__main__':
    unittest.main()
