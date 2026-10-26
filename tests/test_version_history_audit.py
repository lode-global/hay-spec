"""Reproduce the historical evidence without repairing tags or changing records."""
from compatibility_helpers import artifact_before_completeness, without_completeness_source
import hashlib
from pathlib import Path
import subprocess
import unittest

import yaml

from tools.generate_docs import outputs
from tools.validate_spec import load_spec

ROOT = Path(__file__).resolve().parents[1]
BASE = '31614e5d3a289499d7d7648709d457edf94f7a81'
DIGEST = 'b75a38df6a191cded357768abb126443abb0d96ec8710ea899487d5a6f78e072'


def tagged(ref):
    return subprocess.check_output(['git', 'show', f'{ref}:src/hay-spec.yaml'], cwd=ROOT)


def section(spec, identity):
    return next(s for s in spec['sections'] if s['id'] == identity)


class VersionHistoryAudit(unittest.TestCase):
    def test_canonical_spec_and_downloads_remain_byte_identical(self):
        for name in ('src/hay-spec.yaml', 'docs/source/hay-spec.yaml', 'docs/source/hay-spec.json'):
            self.assertEqual(artifact_before_completeness(name), subprocess.check_output(
                ['git', 'show', f'{BASE}:{name}'], cwd=ROOT))

    def test_archive_is_the_exact_original_subsection(self):
        original = tagged(BASE)
        start = original.index(b'      - id: version_history\n')
        end = original.index(b'      - id: document_metadata\n', start)
        archived = (ROOT / 'notes/archive/version-history-original.txt').read_bytes()
        self.assertEqual(archived, original[start:end])
        self.assertEqual(hashlib.sha256(archived).hexdigest(), DIGEST)
        self.assertEqual((ROOT / 'docs/history/archive/version-history-original.txt').read_bytes(), archived)
        self.assertIn(DIGEST, (ROOT / 'notes/version-history-reconciliation.md').read_text())

    def test_valid_old_tags_have_equal_nonmetadata_sections(self):
        old = load_spec(tagged('v0.90.0'))
        later = load_spec(tagged('v0.91.1'))
        old_sections = [s for s in old['sections'] if s['id'] != 'metadata']
        new_sections = [s for s in later['sections'] if s['id'] != 'metadata']
        self.assertEqual(len(old_sections), 10)
        self.assertEqual(old_sections, new_sections)
        for key in ('harvest_date_start', 'harvest_date_end'):
            field = next(f for f in section(old, 'harvest')['fields'] if f['id'] == key)
            self.assertEqual(field['data_type'], 'datetime')
        self.assertIn('version_history', [s['id'] for s in section(old, 'metadata')['subsections']])

    def test_refactor_tag_contains_text_but_fails_whole_document_parsing(self):
        raw = tagged('v0.91.0')
        for token in (b'fertilizer_application', b'organic_amendments', b'lab_sample_id',
                      b'enum_select_mode', b'valid_range:', b'percent_as_fed'):
            self.assertIn(token, raw)
        with self.assertRaises(yaml.YAMLError):
            load_spec(raw)
        for older, newer in (('v0.91.0', 'v0.91.1'), ('v0.91.1', 'v0.91.0')):
            result = subprocess.run(['git', 'merge-base', '--is-ancestor', older, newer], cwd=ROOT)
            self.assertEqual(result.returncode, 1)

    def test_tag_targets_and_laboratory_timeline_match_report(self):
        targets = {
            'v0.90.0': '98fce9dd1c763ab824557b036b7a4c645b71e192',
            'v0.91.0': 'b10ecc7798926355804abd226d001d77305f502c',
            'v0.91.1': '486d175740d3ecc5be583b3da601170081d14049',
            'v0.92.0': '37556a56e59f82db9618b29245614b57d4a1c5ad',
        }
        report = (ROOT / 'notes/version-history-reconciliation.md').read_text()
        for tag, target in targets.items():
            self.assertEqual(subprocess.check_output(
                ['git', 'rev-parse', tag + '^{}'], cwd=ROOT, text=True).strip(), target)
            self.assertIn(target, report)
        ids = lambda ref: {f.get('id', f.get('name')) for f in
                           section(load_spec(tagged(ref)), 'nutrient_analysis')['fields']}
        laboratory = {'lab_sample_id', 'lab_report_reference', 'lab_processing_completed_date',
                      'lab_processing_notes', 'lab_quality_code'}
        self.assertFalse(laboratory & ids('v0.91.1'))
        self.assertFalse(laboratory & ids('3a6a5b7^'))
        self.assertTrue(laboratory <= ids('3a6a5b7'))
        self.assertTrue(laboratory <= ids('v0.92.0'))

    def test_generated_audit_and_archive_are_fresh(self):
        pages = outputs((ROOT / 'src/hay-spec.yaml').read_text(),
                        load_spec((ROOT / 'reference-display.yaml').read_text()))
        for name in ('history/reconciliation.md', 'history/archive/version-history-original.txt'):
            self.assertEqual((ROOT / 'docs' / name).read_text(), pages[name])
        self.assertIn('Reconciled history', (ROOT / 'mkdocs.yml').read_text())
