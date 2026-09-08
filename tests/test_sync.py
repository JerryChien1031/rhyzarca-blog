import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
import frontmatter
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import blogger_api as api
import sync_to_blogger as sync
from markdown_parser import parse_and_convert

META = {'page_key': 'about', 'title': 'About Jerry'}
PAGE = {'id': '123', 'url': 'https://blog.rhyzarca.com/p/about.html',
        'title': 'Old title', 'status': 'LIVE'}


class PagesTests(unittest.TestCase):
    def test_list_follows_pagination_and_includes_drafts(self):
        service = Mock()
        service.pages.return_value.list.return_value.execute.side_effect = [
            {'items': [PAGE], 'nextPageToken': 'next'},
            {'items': [dict(PAGE, id='456', status='DRAFT')]}
        ]
        self.assertEqual(len(api.list_pages(service, 'blog')), 2)
        self.assertEqual(service.pages.return_value.list.call_args.kwargs['pageToken'], 'next')

    def test_real_discovery_accepts_requests(self):
        from googleapiclient.discovery import build
        service = build('blogger', 'v3', developerKey='unused')
        with patch('googleapiclient.http.HttpRequest.execute', return_value={'items': []}):
            self.assertEqual(api.list_pages(service, 'blog'), [])
            api.insert_page(service, 'blog', 'about', 'body')
            api.update_page(service, 'blog', '123', 'Title', 'body')

    def test_empty_id_resolves_url(self):
        with patch.object(api, 'list_pages', return_value=[PAGE]):
            self.assertEqual(api.resolve_page(None, 'blog', META), PAGE)

    def test_key_survives_title_and_url_change(self):
        page = dict(PAGE, url='https://example.com/p/old.html',
                    content='<div data-rhyzarca-page-key="about"></div>')
        with patch.object(api, 'list_pages', return_value=[page]):
            self.assertEqual(api.resolve_page(None, 'blog', META), page)

    def test_ambiguous_identity_fails_closed(self):
        with patch.object(api, 'list_pages', return_value=[PAGE, dict(PAGE, id='456')]):
            with self.assertRaises(ValueError):
                api.resolve_page(None, 'blog', META)

    def test_draft_and_conflicting_key_fail_closed(self):
        for page in (dict(PAGE, status='SOFT_TRASHED'),
                     dict(PAGE, content='<div data-rhyzarca-page-key="other"></div>')):
            with patch.object(api, 'list_pages', return_value=[page]):
                with self.assertRaises(ValueError):
                    api.resolve_page(None, 'blog', META)

    def test_saved_identity_missing_does_not_insert(self):
        with patch.object(api, 'list_pages', return_value=[]):
            with self.assertRaises(ValueError):
                api.resolve_page(None, 'blog', dict(META, blogger_page_url=PAGE['url']))

    def test_list_failure_does_not_insert(self):
        with patch.object(api, 'list_pages', side_effect=RuntimeError), patch.object(api, 'insert_page') as insert:
            with self.assertRaises(RuntimeError):
                api.upsert_page(None, 'blog', META, 'body', Mock())
            insert.assert_not_called()

    def test_insert_checkpoint_then_rename_and_rerun(self):
        checkpoint = Mock()
        with patch.object(api, 'list_pages', side_effect=[[], [PAGE]]), patch.object(api, 'insert_page', return_value=PAGE) as insert, patch.object(api, 'update_page', return_value=PAGE) as update:
            api.upsert_page(None, 'blog', META, 'body', checkpoint)
            api.upsert_page(None, 'blog', META, 'body', checkpoint)
            insert.assert_called_once()
            self.assertEqual(insert.call_args.args[2], 'about')
            self.assertEqual(update.call_count, 2)
            self.assertEqual(checkpoint.call_count, 3)

    def test_rename_failure_keeps_checkpoint(self):
        checkpoint = Mock()
        with patch.object(api, 'list_pages', return_value=[]), patch.object(api, 'insert_page', return_value=PAGE), patch.object(api, 'update_page', side_effect=RuntimeError):
            with self.assertRaises(RuntimeError):
                api.upsert_page(None, 'blog', META, 'body', checkpoint)
            checkpoint.assert_called_once_with(PAGE)

    def test_unexpected_slug_is_saved_and_fails(self):
        page = dict(PAGE, url='https://blog.rhyzarca.com/p/about_2.html')
        checkpoint = Mock()
        with patch.object(api, 'list_pages', return_value=[]), patch.object(api, 'insert_page', return_value=page), patch.object(api, 'update_page', return_value=page):
            with self.assertRaises(ValueError):
                api.upsert_page(None, 'blog', META, 'body', checkpoint)
            checkpoint.assert_called_with(page)

    def test_sync_pages_writes_real_identity_twice(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / 'about.md'
            file.write_text('---\ntitle: About Jerry\npage_key: about\n---\n# Jerry Chien', encoding='utf-8')
            with patch.object(sync, 'PAGES_DIR', folder), patch.object(api, 'list_pages', side_effect=[[], [PAGE]]), patch.object(api, 'insert_page', return_value=PAGE) as insert, patch.object(api, 'update_page', return_value=PAGE):
                sync.sync_pages(None)
                first = file.read_bytes()
                sync.sync_pages(None)
                self.assertEqual(first, file.read_bytes())
                insert.assert_called_once()
                meta = frontmatter.load(file).metadata
                self.assertEqual(meta['blogger_page_id'], PAGE['id'])
                self.assertEqual(meta['blogger_page_url'], PAGE['url'])

    def test_posts_api_contract_unchanged(self):
        service = Mock()
        service.posts.return_value.insert.return_value.execute.return_value = {'id': '42'}
        service.posts.return_value.update.return_value.execute.return_value = {'id': '42'}
        self.assertEqual(api.publish_post(service, 'blog', 'Title', 'body', ['tag']), '42')
        self.assertEqual(api.publish_post(service, 'blog', 'Title', 'body', ['tag'], '42'), '42')
        service.pages.assert_not_called()
        service.posts.return_value.update.assert_called_once_with(blogId='blog', postId='42', body={'title':'Title','content':'body','labels':['tag']})

    def test_posts_sync_insert_update_and_parser(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / 'post.md'
            file.write_text('---\ntitle: Post\ntags: [one]\ncategories: [two]\n---\n![image](/assets/images/example.jpg)', encoding='utf-8')
            with patch.object(sync, 'POSTS_DIR', folder), patch.object(sync, 'publish_post', return_value='42') as publish, patch.object(sync.time, 'sleep'):
                sync.sync_posts(None)
                sync.sync_posts(None)
                self.assertEqual(publish.call_args.kwargs['existing_post_id'], '42')
                self.assertIn('cdn.jsdelivr.net', publish.call_args.args[3])

    def test_about_and_workflow(self):
        root = Path(__file__).resolve().parents[1]
        meta, html = parse_and_convert(root / '_pages/about.md')
        self.assertEqual(meta['page_key'], 'about')
        self.assertIn('<h1>Jerry Chien</h1>', html)
        workflow = yaml.load((root / '.github/workflows/sync.yml').read_text(encoding='utf-8'), Loader=yaml.BaseLoader)
        self.assertIn('_pages/**', workflow['on']['push']['paths'])
        self.assertEqual(workflow['concurrency']['cancel-in-progress'], 'false')
        self.assertIn('[skip ci]', str(workflow))


if __name__ == '__main__':
    unittest.main()
