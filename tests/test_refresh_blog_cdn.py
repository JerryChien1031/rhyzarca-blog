import importlib.util
import unittest
from pathlib import Path
from unittest.mock import Mock

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


if __name__ == '__main__':
    unittest.main()
