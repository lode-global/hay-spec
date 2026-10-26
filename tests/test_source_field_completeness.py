"""Guard the single optional addition and documented record semantics."""
from pathlib import Path
import re
import subprocess
import unittest

from compatibility_helpers import without_completeness_source
from tools.validate_spec import load_spec

ROOT = Path(__file__).resolve().parents[1]
BASE = '95349b957f58e0d5e09e9fc7d6d886bc2f60e727'


class SourceFieldCompleteness(unittest.TestCase):
    def test_only_new_field_is_added_with_no_existing_byte_changes(self):
        source = (ROOT / 'src/hay-spec.yaml').read_text()
        old = subprocess.check_output(['git', 'show', f'{BASE}:src/hay-spec.yaml'], cwd=ROOT)
        self.assertEqual(without_completeness_source(source).encode(), old)
        current = load_spec(source)
        previous = load_spec(old)
        trace = current['sections'][0]
        added = trace['fields'].pop()
        self.assertEqual(added['id'], 'source_fields_completeness')
        self.assertEqual(added['data_type'], 'enum')
        self.assertIs(added['required'], False)
        self.assertEqual(added['valid_values'], ['complete', 'partial'])
        self.assertNotIn('default', added)
        self.assertNotIn('required_if', added)
        self.assertEqual(current, previous)

    def test_documented_fragments_cover_assertions_omission_and_conflict(self):
        notes = (ROOT / 'notes/source-field-completeness.md').read_text()
        examples = [load_spec(s) for s in re.findall(r'```yaml\n(.*?)```', notes, re.S)]
        self.assertEqual(len(examples), 5)
        self.assertNotIn('source_fields_completeness', examples[0])
        self.assertEqual([len(e['source_fields']) for e in examples], [1, 1, 2, 1, 0])
        self.assertEqual([e.get('source_fields_completeness') for e in examples],
                         [None, 'complete', 'complete', 'partial', 'complete'])
        self.assertEqual(examples[2]['source_fields'][0]['field_identifier'], '001-A')
        self.assertIn('not a conforming example', notes)
        self.assertIn('not\nhay records', notes)



if __name__ == '__main__':
    unittest.main()
