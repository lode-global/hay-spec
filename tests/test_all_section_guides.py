"""All-section guide coverage and immutable canonical/record structures."""
from compatibility_helpers import artifact_before_completeness, without_completeness_source
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

from tools.generate_docs import outputs
from tools.field_guides import guide_index
from tools.validate_spec import load_spec

ROOT = Path(__file__).resolve().parents[1]
BASE = '35cd997a6b8e387902f224a12f3e71921a99f7be'
CHILDREN = ('fields', 'components', 'groups', 'subsections')


class AllSectionGuides(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / 'src/hay-spec.yaml').read_text()
        cls.spec = load_spec(cls.source)
        cls.pages = outputs(cls.source, load_spec((ROOT / 'reference-display.yaml').read_text()))
        cls.data = {}
        for section in cls.spec['sections']:
            page = cls.pages[f'guides/{section["id"]}.html']
            cls.data[section['id']] = json.loads(re.search(
                r'<script id="guide-data" type="application/json">(.*?)</script>', page, re.S).group(1))

    def test_canonical_sources_and_full_references_unchanged(self):
        for name in ('src/hay-spec.yaml', 'docs/source/hay-spec.yaml', 'docs/source/hay-spec.json'):
            self.assertEqual(artifact_before_completeness(name), subprocess.check_output(
                ['git', 'show', f'{BASE}:{name}'], cwd=ROOT))
        for name in self.pages:
            if name.startswith('fields/') or name == 'technical/index.md':
                text = artifact_before_completeness('docs/' + name).decode()
                self.assertEqual(text.replace("](../source/", "](source/").replace("](../fields/", "](fields/"), subprocess.check_output(
                    ['git', 'show', f'{BASE}:docs/{"index.md" if name == "technical/index.md" else name}'], cwd=ROOT, text=True))

    def test_every_canonical_node_has_exact_source_scope_order_and_reference(self):
        for i, section in enumerate(self.spec['sections']):
            source_nodes = []
            def walk_source(node, scope, anchor):
                key = '/'.join([*scope, node.get('id', node.get('name'))])
                source_nodes.append((key, anchor, node))
                for collection in CHILDREN:
                    for j, child in enumerate(node.get(collection, [])):
                        walk_source(child, key.split('/'), f'{anchor}-{collection}-{j}')
            walk_source(section, [], f'node-sections-{i}')
            actual = []
            def walk_guide(node):
                if not node.get('presentation'):
                    actual.append((node['key'], node['anchor'], node['source']))
                for child in node['children']:
                    walk_guide(child)
            walk_guide(self.data[section['id']]['root'])
            self.assertEqual(actual, source_nodes, section['id'])
            self.assertEqual(len({key for key, _, _ in actual}), len(actual))
            for _, anchor, _ in actual:
                self.assertIn(f'id="{anchor}"', self.pages[f'fields/{section["id"]}.md'])

    def test_overview_and_site_navigation_cover_every_section(self):
        overview = self.pages['guides/index.html']
        navigation = load_spec((ROOT / 'mkdocs.yml').read_text())['nav']
        guides = next(n['Browse sections'] for n in navigation if 'Browse sections' in n)
        targets = [target for item in guides for target in item.values()]
        self.assertEqual(targets, ['guides/index.html'] +
                         [f'guides/{s["id"]}.html' for s in self.spec['sections']])
        for section in self.spec['sections']:
            self.assertIn(f'href="{section["id"]}.html"', overview)

    def test_component_lists_metadata_and_legacy_literals_are_preserved(self):
        stand = self.data['stand']['root']['source']['fields']
        mixture = next(n for n in stand if n['id'] == 'forage_variety_components')
        self.assertEqual((mixture['data_type'], mixture['item_type']), ('list', 'component'))
        physical = self.data['physical_characteristics']['root']['source']['fields']
        legacy = next(n for n in physical if n['id'] == 'final_storage_structure')
        self.assertEqual(len(legacy['valid_values']), 1)
        self.assertIn('|', legacy['valid_values'][0])
        history = next(n for n in physical if n['id'] == 'handling_events')
        self.assertIsInstance(load_spec(history['examples'][0])['handling_events'], list)
        metadata = self.data['metadata']['root']
        self.assertTrue(all(n['documentary'] for n in metadata['children']))
        self.assertTrue(any(n['source'].get('items') for n in metadata['children']))

    def test_presentation_examples_and_related_links_resolve_within_scope(self):
        for section, data in self.data.items():
            nodes = []
            def walk(node):
                nodes.append(node)
                for child in node['children']:
                    walk(child)
            walk(data['root'])
            keys = {node['key'] for node in nodes}
            for node in nodes:
                self.assertTrue(set(node['related']) <= keys, (section, node['id']))
                if node['example']:
                    self.assertEqual(set(load_spec(node['example'])),
                                     {'source_fields', 'source_fields_completeness'}
                                     if node['id'] == 'source_fields_completeness' else {node['id']})
            page = self.pages[f'guides/{section}.html']
            self.assertNotIn('__SECTION_', page)
            self.assertNotIn('__GUIDE_', page)

    def test_freshness_check_reports_unexpected_guide_without_deleting_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            for name, content in self.pages.items():
                path = out / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
            extra = out / 'guides/retired.html'
            extra.write_text('retired guide')
            result = subprocess.run([sys.executable, 'tools/generate_docs.py', '--check',
                                     '--output', tmp], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn('guides/retired.html', result.stderr)
            self.assertEqual(extra.read_text(), 'retired guide')

    def test_overview_escapes_source_markup(self):
        import copy
        spec = copy.deepcopy(self.spec)
        spec['sections'][0]['title'] = '<img src=x onerror=alert(1)>'
        spec['sections'][0]['description'] = '<script>alert(1)</script>'
        page = guide_index(spec)
        self.assertIn('&lt;img src=x onerror=alert(1)&gt;', page)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', page)
        self.assertNotIn('<img src=x', page)
        self.assertNotIn('<script>alert(1)', page)
