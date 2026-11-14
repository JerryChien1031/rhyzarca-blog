import importlib.util
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

SPEC = importlib.util.spec_from_file_location('refresh_blog_cdn', Path(__file__).resolve().parents[1] / 'scripts/refresh_blog_cdn.py')
cdn = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cdn)


class CDNDeliveryTests(unittest.TestCase):
    path = 'assets/js/blogger.js'

    def test_current_asset_does_not_purge(self):
        fetch = Mock(return_value=b'new')
        result = cdn.verify_asset(self.path, b'new', fetch=fetch)
        self.assertTrue(result['verified'])
        self.assertFalse(result['purged'])
        fetch.assert_called_once_with(cdn.CDN_BASE + self.path)

    def test_success_requires_exact_served_bytes(self):
        fetch = Mock(side_effect=[b'old', b'{"status":"finished"}', b'new'])
        result = cdn.verify_asset(self.path, b'new', fetch=fetch)
        self.assertTrue(result['purged'])
        self.assertEqual([call.args[0] for call in fetch.call_args_list], [cdn.CDN_BASE+self.path, cdn.PURGE_BASE+self.path, cdn.CDN_BASE+self.path])

    def test_successful_purge_with_stale_bytes_fails(self):
        fetch = Mock(side_effect=[b'old', b'{"status":"finished"}'] + [b'old'] * len(cdn.DELAYS))
        with self.assertRaisesRegex(RuntimeError, 'delivery mismatch'):
            cdn.verify_asset(self.path, b'new', fetch=fetch, sleep=Mock())

    def test_pending_purge_is_verified_not_assumed_success(self):
        fetch = Mock(side_effect=[b'old', b'{"status":"pending"}', b'old', b'new'])
        sleep = Mock()
        self.assertTrue(cdn.verify_asset(self.path, b'new', fetch=fetch, sleep=sleep)['verified'])
        sleep.assert_called_once_with(10)

    def test_rejected_purge_fails(self):
        fetch = Mock(side_effect=[b'old', b'{"status":"error"}'])
        with self.assertRaisesRegex(RuntimeError, 'purge rejected'):
            cdn.verify_asset(self.path, b'new', fetch=fetch)

    def test_network_failure_is_not_swallowed(self):
        with self.assertRaises(TimeoutError):
            cdn.verify_asset(self.path, b'new', fetch=Mock(side_effect=TimeoutError()))

    def test_unknown_asset_is_rejected_before_network(self):
        fetch = Mock()
        with self.assertRaises(ValueError):
            cdn.verify_asset('outside.js', b'x', fetch=fetch)
        fetch.assert_not_called()

    def test_immutable_url_is_checked_exactly(self):
        url = cdn.CDN_BASE.replace('@main/', '@' + 'd' * 40 + '/') + self.path
        fetch = Mock(return_value=b'new')
        result = cdn.verify_asset(self.path, b'new', url=url, fetch=fetch)
        self.assertEqual(result['url'], url)
        self.assertFalse(result['purged'])
        fetch.assert_called_once_with(url)

    def test_old_immutable_version_fails_without_purge(self):
        url = cdn.CDN_BASE.replace('@main/', '@' + 'd' * 40 + '/') + self.path
        fetch = Mock(return_value=b'old')
        with self.assertRaisesRegex(RuntimeError, 'delivery mismatch for immutable'):
            cdn.verify_asset(self.path, b'new', url=url, fetch=fetch)
        fetch.assert_called_once_with(url)

    def test_unsupported_url_is_rejected_before_network(self):
        fetch = Mock()
        for url in (
            'https://example.com/' + self.path,
            cdn.CDN_BASE.replace('https:', 'http:') + self.path,
            cdn.CDN_BASE.replace('cdn.jsdelivr.net', 'user@cdn.jsdelivr.net') + self.path,
            cdn.CDN_BASE.replace('cdn.jsdelivr.net', 'cdn.jsdelivr.net:443') + self.path,
            cdn.CDN_BASE.replace('rhyzarca-blog@', 'other-repo@') + self.path,
            cdn.CDN_BASE.replace('@main/', '@unknown/') + self.path,
            cdn.CDN_BASE + self.path + '?v=1',
            cdn.CDN_BASE + self.path + '#fragment',
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                cdn.verify_asset(self.path, b'new', url=url, fetch=fetch)
        fetch.assert_not_called()


class DeployedThemeTests(unittest.TestCase):
    css_url = cdn.CDN_BASE + 'assets/css/blogger.css'
    js_url = cdn.CDN_BASE.replace('@main/', '@' + 'd' * 40 + '/') + 'assets/js/blogger.js'

    def theme(self):
        return (f'<link rel="stylesheet" href="{self.css_url}"/>'
                f'<script defer src="{self.js_url}"></script>')

    def test_discovers_actual_theme_urls_and_ignores_inline_mentions(self):
        html = self.theme() + ('<script>const example = "<script src=old>";</script>'
                               '<!-- <script src="https://example.com/assets/js/blogger.js"> -->'
                               '<link rel="preload" href="ignored.css">'
                               '<script src="https://example.com/other.js"></script>')
        self.assertEqual(cdn.deployed_asset_urls(html), {
            'assets/css/blogger.css': self.css_url,
            'assets/js/blogger.js': self.js_url,
        })

    def test_missing_or_duplicate_asset_fails(self):
        for html in ('', self.theme().replace(f'<script defer src="{self.js_url}"></script>', ''),
                     self.theme() + f'<script src="{self.js_url}"></script>'):
            with self.subTest(html=html), self.assertRaisesRegex(RuntimeError, 'Expected one'):
                cdn.deployed_asset_urls(html)

    def test_foreign_repository_source_is_rejected(self):
        with self.assertRaises(ValueError):
            cdn.deployed_asset_urls(self.theme().replace('rhyzarca-blog@', 'other-repo@'))

    def test_duplicate_attributes_cannot_hide_the_browser_source(self):
        for html in (
            self.theme().replace('<script defer', '<script src="https://example.com/other.js" defer'),
            self.theme().replace('<script defer', f'<script src="{self.js_url}" defer'),
            self.theme().replace('<link rel=', '<link href="https://example.com/other.css" rel='),
        ):
            with self.subTest(html=html), self.assertRaisesRegex(ValueError, 'Duplicate asset attribute'):
                cdn.deployed_asset_urls(html)

    def test_main_verifies_deployed_urls_with_checkout_bytes(self):
        with patch.object(cdn, 'get_bytes', side_effect=[
            self.theme().encode(),
            (cdn.ROOT / 'assets/css/blogger.css').read_bytes(),
            (cdn.ROOT / 'assets/js/blogger.js').read_bytes(),
        ]) as fetch:
            self.assertEqual(cdn.main(), 0)
        self.assertEqual([call.args[0] for call in fetch.call_args_list],
                         [cdn.BLOG_URL, self.css_url, self.js_url])

    def test_main_stops_before_asset_fetch_if_theme_is_missing_script(self):
        with patch.object(cdn, 'get_bytes', return_value=b'<html></html>') as fetch:
            self.assertEqual(cdn.main(), 1)
        fetch.assert_called_once_with(cdn.BLOG_URL)


if __name__ == '__main__':
    unittest.main()
