"""Coverage and bookmark preservation for the single Field Guide entrance."""
import json
from pathlib import Path
import re
import subprocess
import unittest

from tools.generate_docs import outputs
from tools.validate_spec import load_spec

ROOT = Path(__file__).resolve().parents[1]
BASE = 'b7b87f8ac8bb3f77d95668a6b970ae3a76d459bd'


class SingleReadingExperience(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / 'src/hay-spec.yaml').read_text()
        cls.spec = load_spec(cls.source)
        cls.pages = outputs(cls.source, load_spec((ROOT / 'reference-display.yaml').read_text()))

    def test_source_downloads_archive_and_legacy_references_unchanged(self):
        paths = ['src/hay-spec.yaml', 'docs/source/hay-spec.yaml',
                 'docs/source/hay-spec.json', 'docs/technical/index.md',
                 'notes/archive/version-history-original.txt']
        paths += [str(p.relative_to(ROOT)) for p in (ROOT / 'docs/fields').glob('*.md')]
        for path in paths:
            self.assertEqual((ROOT / path).read_bytes(), subprocess.check_output(
                ['git', 'show', f'{BASE}:{path}'], cwd=ROOT), path)

    def test_about_page_preserves_entire_overview_except_guide_links(self):
        overview = self.pages['technical/index.md']
        for section in self.spec['sections']:
            overview = overview.replace(f'(../fields/{section["id"]}.md)',
                                        f'(../guides/{section["id"]}.html)')
        self.assertEqual(self.pages['guidance/specification.md'], overview)

    def test_every_source_node_has_complete_data_and_a_legacy_anchor_route(self):
        script = self.pages['assets/javascripts/reader-navigation.js']
        routes = json.loads(re.search(r'const routes = (.*);', script).group(1))
        count = 0
        for i, section in enumerate(self.spec['sections']):
            page = self.pages[f'guides/{section["id"]}.html']
            data = json.loads(re.search(
                r'<script id="guide-data" type="application/json">(.*?)</script>', page, re.S).group(1))
            self.assertEqual(data['root']['source'], section)
            route = routes[f'fields/{section["id"]}/']
            expected = {}
            def visit(node):
                if not node.get('presentation'):
                    expected[node['anchor']] = node['key']
                    self.assertEqual(node['source']['id'] if 'id' in node['source'] else node['source']['name'], node['id'])
                for child in node['children']:
                    visit(child)
            visit(data['root'])
            self.assertEqual(route['anchors'], expected)
            self.assertEqual(route['guide'], f'guides/{section["id"]}.html')
            self.assertIn('JSON.stringify(node.source, null, 2)', page)
            self.assertNotIn('Read this definition in the full reference', page)
            for anchor in expected:
                self.assertIn(f'id="{anchor}"', self.pages[f'fields/{section["id"]}.md'])
            count += len(expected)
        self.assertGreater(count, 200)


if __name__ == '__main__':
    unittest.main()
