"""Storage guidance must not normalize source literals or hay records."""
import json
from pathlib import Path
import re
import subprocess
import unittest

from tools.generate_docs import outputs
from tools.validate_spec import inspect_spec, load_spec

ROOT = Path(__file__).resolve().parents[1]
BASE = 'c754bc0616d324fc17dabe59815fbde6bc8234fa'
FIELDS = {'final_storage_structure', 'final_surface_type', 'final_airflow_condition',
          'restacked_since_baling', 'visible_moisture_damage'}


class LegacyStorageEnumGuidance(unittest.TestCase):
    def test_canonical_downloads_and_technical_definitions_unchanged(self):
        paths = ['src/hay-spec.yaml', 'docs/source/hay-spec.yaml',
                 'docs/source/hay-spec.json', 'docs/technical/index.md',
                 'notes/archive/version-history-original.txt']
        paths += [str(p.relative_to(ROOT)) for p in (ROOT / 'docs/fields').glob('*.md')]
        for path in paths:
            self.assertEqual((ROOT / path).read_bytes(), subprocess.check_output(
                ['git', 'show', f'{BASE}:{path}'], cwd=ROOT), path)

    def test_guidance_marks_exactly_five_fields_and_preserves_source_projection(self):
        source = (ROOT / 'src/hay-spec.yaml').read_text()
        spec = load_spec(source)
        pages = outputs(source, load_spec((ROOT / 'reference-display.yaml').read_text()))
        marked = {}
        def visit(node):
            if node.get('legacyStorageEnumGuidance'):
                marked[node['key']] = node['source']
            for child in node['children']:
                visit(child)
        for section in spec['sections']:
            page = pages[f'guides/{section["id"]}.html']
            data = json.loads(re.search(
                r'<script id="guide-data" type="application/json">(.*?)</script>',
                page, re.S).group(1))
            self.assertEqual(data['root']['source'], section)
            visit(data['root'])
        self.assertEqual(set(marked), {f'physical_characteristics/{f}' for f in FIELDS})
        for field in marked.values():
            self.assertEqual(field['data_type'], 'enum')
            self.assertEqual(len(field['valid_values']), 1)
            self.assertIsInstance(field['valid_values'][0], str)
            self.assertIn(' | ', field['valid_values'][0])
        warnings = [f for f in inspect_spec(spec) if f['code'] == 'legacy_enum_literal']
        self.assertEqual(len(warnings), 5)
        notes = (ROOT / 'notes/legacy-storage-enums.md').read_text()
        self.assertEqual(pages['guidance/legacy-storage-enums.md'],
                         '<!-- Generated from notes/legacy-storage-enums.md. -->\n\n' + notes)
        fragment = re.search(r'```yaml\n(.*?)```', notes, re.S).group(1)
        self.assertEqual(load_spec(fragment), {'valid_values': ['true | false | unknown']})


if __name__ == '__main__':
    unittest.main()
