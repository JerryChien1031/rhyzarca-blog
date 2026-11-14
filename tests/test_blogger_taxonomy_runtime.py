"""Regression coverage for taxonomy delivered inside actual Blogger content."""
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from blogger_taxonomy import render_category_runtime

# Execute the shipped JavaScript with a small DOM fixture. Node's real URL parser
# handles routes; this does not reimplement category lookup or redirect rules.
NODE_FIXTURE = r"""
const vm = require('node:vm');
const input = JSON.parse(require('node:fs').readFileSync(0, 'utf8'));
const url = new URL(input.url);
const redirects = [];
const location = {
  href: url.href, origin: url.origin, hostname: url.hostname,
  pathname: url.pathname, search: url.search, hash: url.hash,
  replace: value => redirects.push(value)
};
const links = (input.links || []).map(link => ({
  href: link.href, textContent: link.text,
  closest: () => link.nav ? {} : null
}));
const text = {nodeType: 3, nodeValue: input.status || ''};
const showAll = {nodeType: 1, nodeName: 'A', textContent: '顯示所有文章'};
const status = {childNodes: [text, showAll]};
const selected = {textContent: input.selected || ''};
const nav = {setAttribute: () => {}};
const document = {
  body: null, readyState: 'loading', addEventListener: () => {},
  getElementById: id => id === 'rhyzarca-nav' ? nav : null,
  querySelector: () => null,
  querySelectorAll: selector => {
    if (selector === 'a[href*="/search/label/"]') return links;
    if (selector === '.status-msg-body, .status-msg-hidden') return [status];
    if (selector === '.widget.Label li > span[dir="ltr"]') return [selected];
    return [];
  }
};
const window = {location, addEventListener: () => {}};
const context = vm.createContext({location, document, window, URL});
vm.runInContext(input.source, context);
if (input.theme) vm.runInContext('renderCategoryDetails()', context);
process.stdout.write(JSON.stringify({
  redirects, links: links.map(link => ({href: link.href, text: link.textContent})),
  status: text.nodeValue, showAll: showAll.textContent, selected: selected.textContent
}));
"""

class PublishedTaxonomyTests(unittest.TestCase):
    def execute_both(self, path, **fixture):
        inline = render_category_runtime().split('>', 1)[1].rsplit('</script>', 1)[0]
        theme = (ROOT / 'assets/js/blogger.js').read_text(encoding='utf-8')
        for is_theme, source in [(False, inline), (True, theme)]:
            with self.subTest(theme=is_theme, path=path):
                data = dict(fixture, url='https://blog.rhyzarca.com' + path,
                            source=source, theme=is_theme)
                result = subprocess.run(['node', '-e', NODE_FIXTURE],
                                        input=json.dumps(data), text=True,
                                        capture_output=True, check=True)
                yield json.loads(result.stdout)

    def test_legacy_routes_redirect_even_without_posts(self):
        suffix = '?updated-max=2026-09-02T23%3A15%3A00%2B08%3A00&max-results=20&start=4&m=1#archive'
        for alias in ['architecture', 'Architecture', 'build-log']:
            for result in self.execute_both('/search/label/' + alias + suffix):
                self.assertEqual(result['redirects'], ['/search/label/practice' + suffix])

    def test_canonical_and_unknown_routes_do_not_redirect(self):
        for path in ['/search/label/practice', '/search/label/practice/',
                     '/search/label/embodied', '/search/label/Epistemology',
                     '/search/label/%E0%A4%A', '/search/label/architecture/extra']:
            for result in self.execute_both(path):
                self.assertEqual(result['redirects'], [])

    def test_pagination_links_migrate_without_changing_the_caption(self):
        links = [
            {'href': 'https://blog.rhyzarca.com/search/label/architecture?start=4#older', 'text': '較舊的文章'},
            {'href': 'https://blog.rhyzarca.com/search/label/Architecture', 'text': 'Architecture'},
            {'href': 'https://example.com/search/label/architecture', 'text': 'architecture'},
            {'href': 'https://blog.rhyzarca.com/search/label/Epistemology', 'text': 'Epistemology'},
        ]
        for result in self.execute_both('/search/label/practice', links=links):
            self.assertEqual(result['links'][0], {'href': '/search/label/practice?start=4#older', 'text': '較舊的文章'})
            self.assertEqual(result['links'][1], {'href': '/search/label/practice', 'text': '實作探索'})
            self.assertEqual(result['links'][2:], links[2:])

    def test_native_status_and_selected_label_use_the_category_name(self):
        for result in self.execute_both('/search/label/practice',
                                        status='顯示包含「practice」標籤的文章。', selected='practice'):
            self.assertEqual(result['status'], '顯示包含「實作探索」標籤的文章。')
            self.assertEqual(result['showAll'], '顯示所有文章')
            self.assertEqual(result['selected'], '實作探索')
        for result in self.execute_both('/search/label/embodied', status='沒有符合您查詢的文章。'):
            self.assertEqual(result['status'], '沒有符合您查詢的文章。')

    def test_uses_the_existing_four_canonical_categories(self):
        html = render_category_runtime()
        payload = re.search(r'var categories = (.*);', html).group(1)
        actual = json.loads(payload)
        expected = json.loads((ROOT / '_data/blog_categories.json').read_text(encoding='utf-8'))
        self.assertEqual(actual, expected)
        self.assertEqual([v['id'] for v in actual], ['insights','practice','embodied','speculations'])
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
        source = '---\ntitle: Test\ncategories: [practice]\n---\n\n## Body\n\nKeep this content.\n'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'post.md'
            path.write_text(source, encoding='utf-8')
            metadata, html = parse_and_convert(str(path))
            self.assertEqual(path.read_text(encoding='utf-8'), source)
            self.assertEqual(metadata['categories'], ['practice'])
            self.assertIn('<h2>Body</h2>', html)
            self.assertEqual(html.count('<script data-rhyzarca-taxonomy='), 1)

if __name__ == '__main__':
    unittest.main()
