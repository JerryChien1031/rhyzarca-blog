"""Regression coverage for taxonomy delivered inside actual Blogger content."""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from blogger_taxonomy import render_category_runtime

class PublishedTaxonomyTests(unittest.TestCase):
    def test_uses_the_existing_four_canonical_categories(self):
        html = render_category_runtime()
        payload = re.search(r'var categories = (.*);', html).group(1)
        actual = json.loads(payload)
        expected = json.loads((ROOT / '_data/blog_categories.json').read_text(encoding='utf-8'))
        self.assertEqual(actual, expected)
        self.assertEqual([v['id'] for v in actual], ['insights','architecture','embodied','speculations'])
        self.assertEqual(actual[1]['name'], '實作探索')

    def test_runtime_has_no_external_asset_or_cache_dependency(self):
        html = render_category_runtime()
        self.assertNotIn('src=', html)
        self.assertNotIn('fetch(', html)
        self.assertNotIn('cdn.jsdelivr', html)
        self.assertIn('MutationObserver', html)
        self.assertIn('__rhyzarcaPublishedTaxonomy === version', html)

    def test_script_boundary_is_safe(self):
        html = render_category_runtime([{'name':'</script><script>alert(1)</script>'}])
        self.assertEqual(html.count('</script>'), 1)
        self.assertNotIn('<script>alert', html)
        self.assertIn(r'\u003c/script\u003e', html)

    def test_version_changes_with_definition_not_randomly(self):
        one = render_category_runtime([{'name':'one'}])
        two = render_category_runtime([{'name':'two'}])
        version = lambda value: re.search(r'data-rhyzarca-taxonomy="([a-f0-9]+)"', value).group(1)
        self.assertEqual(one, render_category_runtime([{'name':'one'}]))
        self.assertNotEqual(version(one), version(two))

    def test_official_converter_includes_runtime_and_preserves_source(self):
        from markdown_parser import parse_and_convert
        source = '---\ntitle: Test\ncategories: [architecture]\n---\n\n## Body\n\nKeep this content.\n'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'post.md'
            path.write_text(source, encoding='utf-8')
            metadata, html = parse_and_convert(str(path))
            self.assertEqual(path.read_text(encoding='utf-8'), source)
            self.assertEqual(metadata['categories'], ['architecture'])
            self.assertIn('<h2>Body</h2>', html)
            self.assertEqual(html.count('<script data-rhyzarca-taxonomy='), 1)

if __name__ == '__main__':
    unittest.main()
