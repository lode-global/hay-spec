"""Ensure nutrient navigation never becomes a record hierarchy or rewrites source."""
import copy
import json
from pathlib import Path
import re
import subprocess
import unittest

from tools.generate_docs import outputs
from tools.traceability_guide import guide
from tools.validate_spec import load_spec

ROOT = Path(__file__).resolve().parents[1]
BASE = '8cacb2a74d50af6b43b6a126b4d693d82d922e54'


class NutrientGuide(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / 'src/hay-spec.yaml').read_text()
        cls.spec = load_spec(cls.source)
        cls.display = load_spec((ROOT / 'reference-display.yaml').read_text())
        cls.pages = outputs(cls.source, cls.display)
        cls.page = cls.pages['guides/nutrient_analysis.html']
        cls.data = json.loads(re.search(
            r'<script id="guide-data" type="application/json">(.*?)</script>',
            cls.page, re.S).group(1))

    def test_specification_downloads_and_existing_references_are_unchanged(self):
        for name in ('src/hay-spec.yaml', 'docs/source/hay-spec.yaml', 'docs/source/hay-spec.json'):
            self.assertEqual((ROOT / name).read_bytes(), subprocess.check_output(
                ['git', 'show', f'{BASE}:{name}'], cwd=ROOT))
        for name in self.pages:
            if name.startswith('fields/') or name == 'index.md':
                self.assertEqual(self.pages[name], subprocess.check_output(
                    ['git', 'show', f'{BASE}:docs/{name}'], cwd=ROOT, text=True))

    def test_visual_groups_preserve_flat_fields_and_source_order(self):
        root = self.data['root']
        section = next(s for s in self.spec['sections'] if s['id'] == 'nutrient_analysis')
        self.assertEqual(root['source'], section)
        self.assertEqual([n['title'] for n in root['children']],
                         [n['title'] for n in self.display['nutrient_groups']])
        flat = [n for group in root['children'] for n in group['children']]
        self.assertEqual([n['source'] for n in flat], section['fields'])
        self.assertEqual(len(flat), 70)
        self.assertEqual(len({n['key'] for n in flat}), 70)
        for group in root['children']:
            self.assertTrue(group['presentation'])
            self.assertIsNone(group['id'])
            self.assertIn(group['anchor'], self.pages['fields/nutrient_analysis.md'])
        for n in flat:
            self.assertEqual(n['key'], 'nutrient_analysis/' + n['id'])
            self.assertIn(n['anchor'], self.pages['fields/nutrient_analysis.md'])

    def test_literal_protein_identifiers_and_numeric_constraints_are_preserved(self):
        flat = {n['id']: n for g in self.data['root']['children'] for n in g['children']}
        for key in ('soluble_protein_%_cp', 'degradable_protein_%_cp'):
            self.assertIn(key, flat)
            self.assertEqual(load_spec(flat[key]['example']), {key: 25.0 if key.startswith('soluble') else 65.0})
        self.assertEqual(flat['moisture_content']['source']['valid_range'], {'min': 0, 'max': 100})
        self.assertNotIn('valid_range', flat['crude_protein']['source'])
        self.assertEqual(self.data['reference'], '../fields/nutrient_analysis/')
        self.assertEqual(self.page, guide(self.spec, self.display, 'nutrient_analysis'))

    def test_related_fields_and_examples_use_existing_flat_keys(self):
        flat = [n for g in self.data['root']['children'] for n in g['children']]
        keys = {n['key'] for n in flat}
        for node in flat:
            self.assertTrue(set(node['related']) <= keys)
            if node['example']:
                self.assertEqual(set(load_spec(node['example'])), {node['id']})

    def test_nutrient_payload_is_safe_when_definition_contains_html(self):
        spec = copy.deepcopy(self.spec)
        section = next(s for s in spec['sections'] if s['id'] == 'nutrient_analysis')
        section['fields'][0]['definition'] = '</script><script>alert(1)</script>'
        page = guide(spec, self.display, 'nutrient_analysis')
        self.assertNotIn('</script><script>alert(1)', page)
        self.assertNotIn('__SECTION_', page)
        self.assertNotIn('__REFERENCE__', page)
