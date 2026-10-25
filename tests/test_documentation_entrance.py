"""Protect the new entrance without changing the specification or reference."""
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = '8e6e3a7443e100e451859e31787b89355520d7fd'


class DocumentationEntranceTests(unittest.TestCase):
    def original(self, path):
        return subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT)

    def test_source_and_downloads_are_unchanged(self):
        for path in ('src/hay-spec.yaml', 'docs/source/hay-spec.yaml',
                     'docs/source/hay-spec.json'):
            self.assertEqual((ROOT / path).read_bytes(), self.original(path), path)

    def test_overview_only_changes_relative_links(self):
        current = (ROOT / 'docs/technical/index.md').read_text()
        restored = current.replace('](../source/', '](source/').replace('](../fields/', '](fields/')
        self.assertEqual(restored, self.original('docs/index.md').decode())

    def test_home_links_every_section_and_downloads(self):
        home = (ROOT / 'docs/index.md').read_text()
        guides = [p for p in (ROOT / 'docs/guides').glob('*.html') if p.stem != 'index']
        self.assertEqual(len(guides), 11)
        for guide in guides:
            self.assertIn(f'href="guides/{guide.name}"', home)
        for suffix in ('yaml', 'json'):
            self.assertIn(f'href="source/hay-spec.{suffix}" download="hay-spec.{suffix}"', home)

    def test_guides_keep_source_downloads_and_reference_routes(self):
        for guide in (ROOT / 'docs/guides').glob('*.html'):
            content = guide.read_text()
            for suffix in ('yaml', 'json'):
                self.assertIn(f'href="../source/hay-spec.{suffix}"', content, guide.name)
            self.assertIn('href="../technical/"', content, guide.name)


if __name__ == '__main__':
    unittest.main()
