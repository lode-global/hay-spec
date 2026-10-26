"""Reference-data guidance is presentation-only and scoped to the two fields."""
from compatibility_helpers import artifact_before_completeness, without_completeness_source
import json
from pathlib import Path
import re
import subprocess
import unittest

from tools.generate_docs import outputs
from tools.validate_spec import load_spec

ROOT = Path(__file__).resolve().parents[1]
BASE = 'a051c2b1348f844585f193280162ba54a014b01d'


class ReferenceDataGuidanceTests(unittest.TestCase):
    def test_canonical_and_technical_reference_bytes_unchanged(self):
        paths = ['src/hay-spec.yaml', 'docs/source/hay-spec.yaml',
                 'docs/source/hay-spec.json', 'docs/technical/index.md']
        paths += [str(p.relative_to(ROOT)) for p in (ROOT / 'docs/fields').glob('*.md')]
        for path in paths:
            self.assertEqual(artifact_before_completeness(path), subprocess.check_output(
                ['git', 'show', f'{BASE}:{path}'], cwd=ROOT), path)

    def test_policy_generated_and_links_scoped_without_source_mutation(self):
        source = (ROOT / 'src/hay-spec.yaml').read_text()
        spec = load_spec(source)
        pages = outputs(source, load_spec((ROOT / 'reference-display.yaml').read_text()))
        self.assertEqual(pages['guidance/reference-data.md'],
                         '<!-- Generated from notes/reference-data-policy.md. -->\n\n' +
                         (ROOT / 'notes/reference-data-policy.md').read_text())
        marked = []
        def visit(node):
            if node.get('referenceDataGuidance'):
                marked.append(node['key'])
            for child in node['children']:
                visit(child)
        for section in spec['sections']:
            page = pages[f'guides/{section["id"]}.html']
            data = json.loads(re.search(r'<script id="guide-data" type="application/json">(.*?)</script>', page, re.S).group(1))
            self.assertEqual(data['root']['source'], section)
            visit(data['root'])
        self.assertEqual(set(marked), {
            'stand/forage_variety_components/forage_variety',
            'nutrient_analysis/hay_testing_laboratory'})


if __name__ == '__main__':
    unittest.main()
