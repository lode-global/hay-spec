"""Presentation must not alter canonical records or discard stable links."""
import copy
from pathlib import Path
import re
import unittest

from tools.generate_docs import CHILDREN, outputs, validate_display
from tools.validate_spec import load_spec

ROOT = Path(__file__).resolve().parents[1]


class ReferenceDisplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / 'src/hay-spec.yaml').read_text()
        cls.spec = load_spec(cls.source)
        cls.display = load_spec((ROOT / 'reference-display.yaml').read_text())

    def test_every_untitled_node_has_a_scoped_label(self):
        expected = set()
        def walk(node, scope):
            scope = [*scope, node.get('id', node.get('name'))]
            if 'title' not in node:
                expected.add('/'.join(scope))
            for key in CHILDREN:
                for child in node.get(key, []):
                    walk(child, scope)
        for section in self.spec['sections']:
            walk(section, [])
        self.assertEqual(expected, set(self.display['titles']))

    def test_sources_and_existing_node_anchors_are_preserved(self):
        before = outputs(self.source)
        after = outputs(self.source, self.display)
        for path in ('source/hay-spec.yaml', 'source/hay-spec.json'):
            self.assertEqual(before[path], after[path])
        for path in before:
            if path.startswith('fields/'):
                pattern = r'<a id="(node-[^"]+)"></a>'
                self.assertEqual(re.findall(pattern, before[path]),
                                 re.findall(pattern, after[path]))
                self.assertEqual(re.findall(r'Identifier: `([^`]+)`', before[path]),
                                 re.findall(r'Identifier: `([^`]+)`', after[path]))

    def test_navigation_and_literal_identifiers(self):
        pages = outputs(self.source, self.display)
        nutrient = pages['fields/nutrient_analysis.md']
        positions = []
        for group in self.display['nutrient_groups']:
            self.assertIn(f'](#nav-{group["anchor"]})', nutrient)
            anchor = f'<a id="nav-{group["anchor"]}"></a>'
            self.assertEqual(nutrient.count(anchor), 1)
            positions.append(nutrient.index(anchor))
        self.assertEqual(positions, sorted(positions))
        self.assertIn('### Soluble protein (% of CP)', nutrient)
        self.assertIn('Identifier: `soluble_protein_%_cp`', nutrient)
        self.assertIn('Identifier: `lot_identifier_external.value`',
                      pages['fields/traceability.md'])

    def test_rejects_stale_or_overriding_titles(self):
        for key in ('nutrient_analysis/nonexistent', 'nutrient_analysis'):
            with self.subTest(key=key):
                display = copy.deepcopy(self.display)
                display['titles'][key] = 'Invalid override'
                with self.assertRaises(ValueError):
                    validate_display(self.spec, display)

    def test_rejects_invalid_navigation(self):
        for change in ('duplicate', 'order', 'stale', 'first'):
            with self.subTest(change=change):
                display = copy.deepcopy(self.display)
                groups = display['nutrient_groups']
                if change == 'duplicate':
                    groups[1]['anchor'] = groups[0]['anchor']
                elif change == 'order':
                    groups[1], groups[2] = groups[2], groups[1]
                elif change == 'stale':
                    groups[0]['starts_at'] = 'nonexistent'
                else:
                    groups.pop(0)
                with self.assertRaises(ValueError):
                    validate_display(self.spec, display)
