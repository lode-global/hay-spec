"""Lossless source projection and safe, deterministic guide generation."""
import json
from pathlib import Path
import re
import subprocess
import unittest

from tools.generate_docs import outputs
from tools.field_guides import guide
from tools.validate_spec import load_spec

ROOT = Path(__file__).resolve().parents[1]
BASE = '8ef6760ff52150a3a428eaa454256cbff748e401'


class TraceabilityGuide(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / 'src/hay-spec.yaml').read_text()
        cls.spec = load_spec(cls.source)
        cls.display = load_spec((ROOT / 'reference-display.yaml').read_text())

    def payload(self, page):
        return json.loads(re.search(r'<script id="guide-data" type="application/json">(.*?)</script>',
                                    page, re.S).group(1))

    def test_source_and_download_bytes_are_unchanged(self):
        for name in ('src/hay-spec.yaml', 'docs/source/hay-spec.yaml', 'docs/source/hay-spec.json'):
            self.assertEqual((ROOT / name).read_bytes(), subprocess.check_output(
                ['git', 'show', f'{BASE}:{name}'], cwd=ROOT))

    def test_projection_preserves_every_definition_and_literal_identifier(self):
        page = guide(self.spec, self.display)
        data = self.payload(page)
        section = next(s for s in self.spec['sections'] if s['id'] == 'traceability')
        self.assertEqual(data['root']['source'], section)
        reference = outputs(self.source)['fields/traceability.md']
        def walk(node):
            children = node['source'].get('fields', node['source'].get('components', []))
            self.assertEqual([n['source'] for n in node['children']], children)
            for child in node['children']:
                self.assertIn(child['anchor'], reference)
                walk(child)
        walk(data['root'])
        self.assertIn('traceability/lot_identifier_external/lot_identifier_external.value', page)
        self.assertEqual(page, guide(self.spec, self.display))

    def test_script_payload_cannot_be_closed_by_source_text(self):
        import copy
        spec = copy.deepcopy(self.spec)
        spec['sections'][0]['fields'][0]['definition'] = '</script><script>alert(1)</script>'
        page = guide(spec, self.display)
        data = self.payload(page)
        self.assertEqual(data['root']['children'][0]['source']['definition'],
                         '</script><script>alert(1)</script>')
        self.assertNotIn('</script><script>alert(1)', page)

    def test_generated_guide_and_reference_targets_are_present(self):
        pages = outputs(self.source, self.display)
        self.assertEqual(pages['guides/traceability.html'], guide(self.spec, self.display))
        data = self.payload(pages['guides/traceability.html'])
        keys = set()
        def walk(n):
            keys.add(n['key'])
            for child in n['children']:
                walk(child)
        walk(data['root'])
        def targets(n):
            self.assertTrue(set(n['related']) <= keys)
            for child in n['children']:
                targets(child)
        targets(data['root'])
