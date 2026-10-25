"""Release preparation updates metadata, never scientific field definitions."""
import json
from pathlib import Path
import subprocess
import unittest

from compatibility_helpers import restore_previous_release_metadata
from tools.validate_spec import load_spec


ROOT = Path(__file__).resolve().parents[1]
BASE = '543255038bc07e9b565c036a2214d6ebff3c1406'


class ReleasePreparation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = load_spec((ROOT / 'src/hay-spec.yaml').read_text())
        cls.previous = load_spec(subprocess.check_output([
            'git', 'show', f'{BASE}:src/hay-spec.yaml'], cwd=ROOT, text=True))
        cls.metadata = {s['id']: s for section in cls.spec['sections']
                        if section['id'] == 'metadata' for s in section['subsections']}

    def test_no_field_changes_beyond_release_metadata(self):
        self.assertEqual(restore_previous_release_metadata(self.spec, self.previous), self.previous)

    def test_candidate_metadata_does_not_claim_publication(self):
        self.assertEqual(self.spec['version'], '0.92.0')
        self.assertEqual(self.spec['status'], 'draft')
        self.assertEqual(self.spec['prepared_on'], '2026-10-24')
        self.assertEqual(self.spec['publication_status'], 'unreleased')
        self.assertIsNone(self.spec['published_on'])

    def test_history_preserves_prior_entries_and_labels_candidate(self):
        previous = next(s for section in self.previous['sections']
                        if section['id'] == 'metadata' for s in section['subsections']
                        if s['id'] == 'version_history')
        history = self.metadata['version_history']['items']
        self.assertEqual(history[1:], previous['items'])
        self.assertIn('v0.92.0 (unreleased;', history[0])

    def test_human_metadata_matches_without_nonexistent_schema_link(self):
        text = '\n'.join(self.metadata['document_metadata']['items'])
        self.assertIn('Version: 0.92.0', text)
        self.assertIn('Published on: Not yet published', text)
        self.assertIn('Planned tag: v0.92.0 (not created)', text)
        self.assertNotIn('/schema.yaml', text)
        self.assertNotIn('/releases/tag/v0.92.0', text)

    def test_generated_transcription_carries_unpublished_metadata(self):
        generated = json.loads((ROOT / 'docs/source/hay-spec.json').read_text())
        self.assertEqual(generated, self.spec)
        self.assertIsNone(generated['published_on'])

    def test_readme_and_notes_distinguish_candidate_from_published_release(self):
        readme = (ROOT / 'README.md').read_text()
        notes = (ROOT / 'releases/v0.92.0.md').read_text()
        self.assertIn('v0.92.0 (unreleased', readme)
        self.assertIn('**Latest published:** [v0.91.1]', readme)
        self.assertIn('Draft release notes — unreleased', notes)
        self.assertIn('same sample/basis', notes)


if __name__ == '__main__':
    unittest.main()
