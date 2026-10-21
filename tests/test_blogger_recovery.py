import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import frontmatter
from google.auth.exceptions import RefreshError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import blogger_api as api
import check_blogger_auth as health
import sync_to_blogger as sync


class AuthorizationRecoveryTests(unittest.TestCase):
    def test_health_forces_refresh_without_persisting_credentials(self):
        service = Mock()
        service.blogs.return_value.listByUser.return_value.execute.return_value = {'items': [{}]}
        with patch.object(health, 'get_blogger_service', return_value=service) as connect:
            self.assertEqual(health.main(), 0)
        connect.assert_called_once_with(force_refresh=True, persist_token=False)
        service.blogs.return_value.listByUser.assert_called_once_with(userId='self')
        service.posts.assert_not_called()
        service.pages.assert_not_called()

    def test_valid_access_token_does_not_hide_revoked_refresh_token(self):
        credentials = Mock(valid=True, refresh_token='test-only')
        credentials.refresh.side_effect = RefreshError(
            'sensitive-response', {'error': 'invalid_grant', 'private': 'must-not-appear'})
        with patch.object(api.os.path, 'exists', return_value=True), \
                patch.object(api.Credentials, 'from_authorized_user_file', return_value=credentials), \
                patch.object(api, 'build') as build:
            with self.assertRaises(api.BloggerAuthorizationError) as caught:
                api.get_blogger_service(force_refresh=True, persist_token=False)
        credentials.refresh.assert_called_once()
        build.assert_not_called()
        message = str(caught.exception)
        self.assertIn('invalid_grant', message)
        self.assertIn('BLOGGER_TOKEN', message)
        self.assertIn('Testing', message)
        self.assertNotIn('sensitive-response', message)
        self.assertNotIn('must-not-appear', message)

    def test_health_refresh_leaves_token_file_unchanged(self):
        with tempfile.TemporaryDirectory() as folder:
            token = Path(folder) / 'token.json'
            token.write_text('preserve-existing-credential', encoding='utf-8')
            before = token.read_bytes()
            credentials = Mock(valid=True, refresh_token='test-only')
            with patch.object(api.Credentials, 'from_authorized_user_file', return_value=credentials), \
                    patch.object(api, 'build', return_value=Mock()):
                api.get_blogger_service(token_file=str(token), force_refresh=True, persist_token=False)
            credentials.refresh.assert_called_once()
            credentials.to_json.assert_not_called()
            self.assertEqual(token.read_bytes(), before)

    def test_failed_refresh_does_not_overwrite_existing_token(self):
        with tempfile.TemporaryDirectory() as folder:
            token = Path(folder) / 'token.json'
            token.write_text('preserve-existing-credential', encoding='utf-8')
            before = token.read_bytes()
            credentials = Mock(valid=False, refresh_token='test-only')
            credentials.refresh.side_effect = RefreshError('private', {'error': 'invalid_grant'})
            with patch.object(api.Credentials, 'from_authorized_user_file', return_value=credentials):
                with self.assertRaises(api.BloggerAuthorizationError):
                    api.get_blogger_service(token_file=str(token))
            self.assertEqual(token.read_bytes(), before)

    def test_other_refresh_failure_does_not_claim_token_was_revoked(self):
        credentials = Mock(valid=False, refresh_token='test-only')
        credentials.refresh.side_effect = RefreshError('private', {'error': 'temporarily_unavailable'})
        with patch.object(api.os.path, 'exists', return_value=True), \
                patch.object(api.Credentials, 'from_authorized_user_file', return_value=credentials):
            with self.assertRaises(api.BloggerAuthorizationError) as caught:
                api.get_blogger_service()
        self.assertNotIn('invalid_grant', str(caught.exception))
        self.assertNotIn('revoked', str(caught.exception))

    def test_health_reports_failure_without_raw_exception_data(self):
        error_output = io.StringIO()
        with patch.object(health, 'get_blogger_service', side_effect=RuntimeError('credential-value')), \
                contextlib.redirect_stderr(error_output):
            self.assertEqual(health.main(), 1)
        self.assertIn('RuntimeError', error_output.getvalue())
        self.assertNotIn('credential-value', error_output.getvalue())


class SyncFailureReportingTests(unittest.TestCase):
    def test_partial_failure_continues_and_only_saves_successful_identity(self):
        with tempfile.TemporaryDirectory() as folder:
            failed = Path(folder) / 'failed.md'
            successful = Path(folder) / 'successful.md'
            for post in (failed, successful):
                post.write_text('---\ntitle: Candidate\n---\nContent', encoding='utf-8')
            failed_before = failed.read_bytes()
            with patch.object(sync, 'POSTS_DIR', folder), \
                    patch.object(sync.glob, 'glob', return_value=[str(failed), str(successful)]), \
                    patch.object(sync, 'publish_post', side_effect=[RuntimeError('private'), 'saved-id']) as publish, \
                    patch.object(sync.time, 'sleep'):
                failures = sync.sync_posts(Mock())
            self.assertEqual(failures, [('failed.md', 'RuntimeError')])
            self.assertEqual(publish.call_count, 2)
            self.assertEqual(failed.read_bytes(), failed_before)
            self.assertEqual(frontmatter.load(successful)['blogger_post_id'], 'saved-id')

    def test_main_reports_both_post_and_page_failures_and_exits_nonzero(self):
        error_output = io.StringIO()
        with patch.object(sync, 'BLOG_ID', 'test-blog'), \
                patch.object(sync, 'get_blogger_service', return_value=Mock()), \
                patch.object(sync, 'sync_posts', return_value=[('failed.md', 'RuntimeError')]), \
                patch.object(sync, 'sync_pages', side_effect=ValueError('private')), \
                contextlib.redirect_stderr(error_output):
            self.assertEqual(sync.main(), 1)
        self.assertIn('failed.md: RuntimeError', error_output.getvalue())
        self.assertIn('_pages: ValueError', error_output.getvalue())
        self.assertNotIn('private', error_output.getvalue())

    def test_main_returns_zero_only_when_both_syncs_succeed(self):
        with patch.object(sync, 'BLOG_ID', 'test-blog'), \
                patch.object(sync, 'get_blogger_service', return_value=Mock()), \
                patch.object(sync, 'sync_posts', return_value=[]), \
                patch.object(sync, 'sync_pages') as pages:
            self.assertEqual(sync.main(), 0)
        pages.assert_called_once()

    def test_auth_failure_prevents_all_publication(self):
        with patch.object(sync, 'BLOG_ID', 'test-blog'), \
                patch.object(sync, 'get_blogger_service', side_effect=api.BloggerAuthorizationError('renew token')), \
                patch.object(sync, 'sync_posts') as posts, \
                patch.object(sync, 'sync_pages') as pages:
            self.assertEqual(sync.main(), 1)
        posts.assert_not_called()
        pages.assert_not_called()

    def test_missing_posts_directory_is_reported_as_failure(self):
        with patch.object(sync.os.path, 'exists', return_value=False):
            self.assertEqual(sync.sync_posts(Mock()), [('_posts', 'FileNotFoundError')])


if __name__ == '__main__':
    unittest.main()
