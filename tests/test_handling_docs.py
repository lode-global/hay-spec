"""Handling compatibility and lossless deterministic documentation checks."""
import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

from tools.generate_docs import outputs
from tools.validate_spec import load_spec
from compatibility_helpers import restore_previous_nutrient_definitions


ROOT = Path(__file__).resolve().parents[1]
BASE = 'f765fca13d8532d5d612c0ffc42331572bc88322'


class HandlingDocs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / 'src/hay-spec.yaml').read_text()
        cls.spec = load_spec(cls.source)
        cls.pages = outputs(cls.source)
        section = next(s for s in cls.spec['sections'] if s['id'] == 'physical_characteristics')
        cls.history = next(f for f in section['fields'] if f['id'] == 'handling_events')

    def test_existing_source_content_is_unchanged_except_additive_history(self):
        previous = load_spec(subprocess.check_output([
            'git', 'show', f'{BASE}:src/hay-spec.yaml'], cwd=ROOT, text=True))
        current = copy.deepcopy(self.spec)
        current['sections'] = restore_previous_nutrient_definitions(
            current['sections'], previous['sections'])
        for section in current['sections']:
            for field in section.get('fields', []):
                if field.get('id') == 'handling_events':
                    field.pop('guidance')
                    field.pop('components')
        self.assertEqual(current, previous)

    def test_legacy_and_annotated_examples_keep_optional_components(self):
        fields = {f['id']: f for f in self.history['components']}
        self.assertEqual(len(fields), 8)
        self.assertTrue(all(f['required'] is False for f in fields.values()))
        notes = (ROOT / 'notes/handling-history-docs.md').read_text()
        examples = [load_spec(s) for s in re.findall(r'```yaml\n(.*?)```', notes, re.S)]
        self.assertEqual(len(examples), 2)
        for record in examples:
            for event in record['handling_events']:
                for key, value in event.items():
                    self.assertIn(key, fields)
                    if fields[key]['data_type'] == 'boolean':
                        self.assertIs(type(value), bool)
                    if fields[key]['data_type'] == 'string':
                        self.assertIsInstance(value, str)
        self.assertNotIn('stage_label', examples[0]['handling_events'][0])
        self.assertIs(examples[0]['handling_events'][0]['restacked'], False)

    def test_json_transcription_preserves_all_source_values(self):
        self.assertEqual(json.loads(self.pages['source/hay-spec.json']), self.spec)
        self.assertEqual(self.pages['source/hay-spec.yaml'], self.source)

    def test_duplicate_identifiers_remain_distinct_in_documentation(self):
        # Keep exercising duplicate rendering after the actual duplicate is fixed.
        duplicate = outputs(self.source.replace('id: moisture_content\n', 'id: dry_matter\n', 1))
        page = duplicate['fields/nutrient_analysis.md']
        self.assertEqual(page.count('Identifier: `dry_matter`'), 2)
        anchors = re.findall(r'<a id="([^"]+)"', page)
        self.assertEqual(len(anchors), len(set(anchors)))
        self.assertIn('duplicate_identifier', duplicate['index.md'])

    def test_output_is_deterministic(self):
        self.assertEqual(outputs(self.source), self.pages)

    def test_every_section_identifies_unreleased_source_status(self):
        pages = [text for name, text in self.pages.items() if name.startswith('fields/')]
        self.assertEqual(len(pages), len(self.spec['sections']))
        for page in pages:
            self.assertIn('**Current-source reference, including unreleased additions.**', page)
            self.assertIn('Source version: 0.91.1; status: draft.', page)
            self.assertIn('../index.md', page)

    def test_unsupported_source_metadata_is_rejected_explicitly(self):
        for source in [
            'sections: []\n',
            'title: Test\nversion: 1.0\nstatus: draft\nsections: []\n',
            'title: Test\nversion: "1"\nstatus: draft\npublished_on: 2026-10-24\nsections: []\n',
            'title: Test\nversion: "1"\nstatus: draft\nextra: {1: value}\nsections: []\n',
        ]:
            with self.subTest(source=source), self.assertRaises(ValueError):
                outputs(source)

    def test_generation_failure_does_not_write_partial_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'spec.yaml'
            source.write_text('title: Test\nversion: "1"\nstatus: draft\n'
                              'published_on: 2026-10-24\nsections: []\n')
            result = subprocess.run([
                sys.executable, str(ROOT / 'tools/generate_docs.py'), '--source',
                str(source), '--output', str(root / 'output'),
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn('quote date-like values', result.stderr)
            self.assertNotIn('Traceback', result.stderr)
            self.assertFalse((root / 'output').exists())

    def test_check_detects_stale_output_without_rewriting_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, text in self.pages.items():
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text)
            (root / 'index.md').write_text('stale')
            result = subprocess.run([
                sys.executable, str(ROOT / 'tools/generate_docs.py'), '--source',
                str(ROOT / 'src/hay-spec.yaml'), '--output', tmp, '--check',
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn('index.md', result.stderr)
            self.assertEqual((root / 'index.md').read_text(), 'stale')

    def test_duplicate_section_names_cannot_overwrite_pages(self):
        with self.assertRaisesRegex(ValueError, 'overwrite'):
            outputs('title: Test\nversion: x\nstatus: draft\nsections:\n'
                    '  - id: same\n  - id: same\n')


if __name__ == '__main__':
    unittest.main()
