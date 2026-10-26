"""Executable examples preserve literal keys, scalar types, and nesting."""
import json
from pathlib import Path
import re
import subprocess
import unittest

import yaml

from tools.generate_docs import outputs
from tools.validate_spec import load_spec

ROOT = Path(__file__).resolve().parents[1]
BASE = 'aa65e8cd4c20518046d2ab1ce8cc428558e1e21a'
EXPECTED = {
    'external-lot': {'lot_identifier_external': {
        'lot_identifier_external.value': '00017-A',
        'lot_identifier_external.issuer': 'USDA'}},
    'protein': {'soluble_protein_%_cp': 25.0, 'degradable_protein_%_cp': 65.0},
}


class LegacyIdentifierExamples(unittest.TestCase):
    def test_source_downloads_and_definitions_remain_byte_identical(self):
        paths = ['src/hay-spec.yaml', 'docs/source/hay-spec.yaml',
                 'docs/source/hay-spec.json', 'docs/technical/index.md',
                 'notes/archive/version-history-original.txt']
        paths += [str(p.relative_to(ROOT)) for p in (ROOT / 'docs/fields').glob('*.md')]
        for path in paths:
            self.assertEqual((ROOT / path).read_bytes(), subprocess.check_output(
                ['git', 'show', f'{BASE}:{path}'], cwd=ROOT), path)

    def test_pairs_round_trip_preserving_values_and_scalar_types(self):
        notes = (ROOT / 'notes/legacy-identifier-interoperability.md').read_text()
        embedded = re.findall(r'```(yaml|json)\n(.*?)```', notes, re.S)
        self.assertEqual(len(embedded), 4)
        for index, (stem, expected) in enumerate(EXPECTED.items()):
            parsed = []
            for extension, parser in (('yaml', load_spec), ('json', json.loads)):
                text = (ROOT / f'examples/legacy-identifiers/{stem}.{extension}').read_text()
                record = parser(text)
                self.assertEqual(record, expected)
                kind, body = embedded[2 * index + (extension == 'json')]
                self.assertEqual(kind, extension)
                self.assertEqual(parser(body), record)
                parsed.append(record)
            for record in parsed:
                for result in (json.loads(json.dumps(record)),
                               load_spec(yaml.safe_dump(record)),
                               json.loads(json.dumps(load_spec(yaml.safe_dump(record))))):
                    self.assertEqual(result, expected)
                    if stem == 'external-lot':
                        value = result['lot_identifier_external']['lot_identifier_external.value']
                        self.assertIs(type(value), str)
                        self.assertEqual(value, '00017-A')
                    else:
                        self.assertTrue(all(type(v) is float for v in result.values()))

    def test_guidance_links_are_scoped_and_downloads_match_fixtures(self):
        source = (ROOT / 'src/hay-spec.yaml').read_text()
        spec = load_spec(source)
        pages = outputs(source, load_spec((ROOT / 'reference-display.yaml').read_text()))
        marked = set()
        def visit(node):
            if node.get('legacyIdentifierGuidance'):
                marked.add(node['key'])
            for child in node['children']:
                visit(child)
        for section in spec['sections']:
            data = json.loads(re.search(
                r'<script id="guide-data" type="application/json">(.*?)</script>',
                pages[f'guides/{section["id"]}.html'], re.S).group(1))
            self.assertEqual(data['root']['source'], section)
            visit(data['root'])
        self.assertEqual(marked, {
            'traceability/lot_identifier_external',
            'traceability/lot_identifier_external/lot_identifier_external.value',
            'traceability/lot_identifier_external/lot_identifier_external.issuer',
            'nutrient_analysis/soluble_protein_%_cp',
            'nutrient_analysis/degradable_protein_%_cp'})
        for stem in EXPECTED:
            for extension in ('yaml', 'json'):
                path = f'examples/legacy-identifiers/{stem}.{extension}'
                self.assertEqual(pages[path], (ROOT / path).read_text())
        self.assertEqual(pages['guidance/legacy-identifiers.md'],
                         '<!-- Generated from notes/legacy-identifier-interoperability.md. -->\n\n' +
                         (ROOT / 'notes/legacy-identifier-interoperability.md').read_text())


if __name__ == '__main__':
    unittest.main()
