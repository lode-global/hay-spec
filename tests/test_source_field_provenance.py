"""Guard the optional addition and all pre-existing source definitions."""
import copy
from pathlib import Path
import re
import subprocess
import unittest

from tools.validate_spec import load_spec

ROOT = Path(__file__).resolve().parents[1]
BASE = '52377fae34c61cd6382a7fcdd7c952ad17a7a207'


class SourceFieldProvenance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = load_spec((ROOT / 'src/hay-spec.yaml').read_text())
        cls.previous = load_spec(subprocess.check_output(
            ['git', 'show', f'{BASE}:src/hay-spec.yaml'], cwd=ROOT, text=True))
        trace = next(s for s in cls.spec['sections'] if s['id'] == 'traceability')
        cls.field = next(f for f in trace['fields'] if f['id'] == 'source_fields')

    def test_only_new_collection_and_publication_notice_change(self):
        current = copy.deepcopy(self.spec)
        trace = next(s for s in current['sections'] if s['id'] == 'traceability')
        self.assertEqual(trace['fields'].pop(), self.field)
        current['publication_status'] = self.previous['publication_status']
        metadata = next(s for s in current['sections'] if s['id'] == 'metadata')
        previous = next(s for s in self.previous['sections'] if s['id'] == 'metadata')
        for item, old in zip(metadata['subsections'], previous['subsections']):
            if item['id'] == 'document_metadata':
                text = item['items'][0].replace(
                    'Publication: Unreleased additions since v0.92.0', 'Publication: Published')
                self.assertEqual(text, old['items'][0])
                item['items'][0] = text
        self.assertEqual(current, self.previous)

    def test_optional_collection_and_string_components(self):
        self.assertEqual(self.field['data_type'], 'object[]')
        self.assertIs(self.field['required'], False)
        self.assertNotIn('required_if', self.field)
        components = {c['id']: c for c in self.field['components']}
        self.assertEqual(set(components),
                         {'field_name', 'field_identifier', 'field_identifier_scope'})
        for component in components.values():
            self.assertEqual(component['data_type'], 'string')
            self.assertIs(component['required'], False)
            self.assertNotIn('required_if', component)

    def test_examples_cover_legacy_single_multiple_and_empty(self):
        notes = (ROOT / 'notes/source-field-provenance.md').read_text()
        examples = [load_spec(x) for x in re.findall(r'```yaml\n(.*?)```', notes, re.S)]
        self.assertEqual(len(examples), 4)
        self.assertNotIn('source_fields', examples[0])
        self.assertEqual(len(examples[1]['source_fields']), 1)
        self.assertEqual(len(examples[2]['source_fields']), 2)
        self.assertEqual(examples[3]['source_fields'], [])
        for record in examples:
            for entry in record.get('source_fields', []):
                self.assertTrue(entry.get('field_name') or entry.get('field_identifier'))
                self.assertTrue(all(isinstance(value, str) and value.strip()
                                    for value in entry.values()))
        entries = examples[2]['source_fields']
        self.assertEqual(entries[0]['field_identifier'], '001-A')
        self.assertEqual(entries[0]['field_identifier'], entries[1]['field_identifier'])
        self.assertNotEqual(entries[0]['field_identifier_scope'], entries[1]['field_identifier_scope'])
