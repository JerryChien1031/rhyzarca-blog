import json
import re
import unittest
from pathlib import Path
import frontmatter

ROOT = Path(__file__).resolve().parents[1]
class TaxonomyTests(unittest.TestCase):
    def setUp(self):
        self.categories=json.loads((ROOT/'_data/blog_categories.json').read_text())
        self.ids={c['id'] for c in self.categories}
    def test_four_categories_and_names(self):
        self.assertEqual(self.ids,{'insights','practice','embodied','speculations'})
        self.assertEqual(next(c['name'] for c in self.categories if c['id']=='practice'),'實作探索')
    def test_all_posts_use_canonical_categories(self):
        for path in (ROOT/'_posts').glob('*.md'):
            with self.subTest(path=path.name):
                categories=frontmatter.load(path)['categories']
                self.assertTrue(categories)
                self.assertEqual(len(categories),len(set(categories)))
                self.assertTrue(set(categories)<=self.ids)
    def test_blogger_snapshot_matches_source(self):
        js=(ROOT/'assets/js/blogger.js').read_text()
        match=re.search(r'var RHYZARCA_CATEGORIES = (.*);',js)
        self.assertIsNotNone(match)
        self.assertEqual(json.loads(match[1]),self.categories)
        self.assertNotIn('系統日誌',js)
        self.assertIn('實作探索 (Practice)',js)
    def test_category_page_uses_canonical_source_and_aliases(self):
        text=(ROOT/'categories.md').read_text()
        self.assertIn('site.data.blog_categories',text)
        self.assertIn('site.categories[category.id]',text)
        self.assertIn('category.aliases',text)
        self.assertNotIn('site.categories.build-log',text)
    def test_examples_follow_author_assigned_categories(self):
        expected={
            '2026-11-13-two-ai-projects-human-judgment.md':['practice'],
            '2026-11-06-from-unknown-to-human-ai-mutual-growth.md':['insights'],
            '2026-10-22-claude-codex-harness-engineering-auto-workflow.md':['practice'],
            '2026-09-15-digital-babel-rhyzarca-sovereign-continuity.md':['insights'],
        }
        for name,categories in expected.items():
            self.assertEqual(frontmatter.load(ROOT/'_posts'/name)['categories'],categories)
    def test_definition_includes_planning_tests_and_failure(self):
        doc=(ROOT/'docs/blog-taxonomy.md').read_text()
        for term in ['可行性','單元','失敗','個人','團隊','不以完成或成功為門檻']:
            self.assertIn(term,doc)
        contract=(ROOT/'docs/blog-article-contract.md').read_text()
        self.assertIn('不限完成或成功',contract)
        self.assertNotIn('`architecture` 是已實作的系統工程',contract)
    def test_category_aliases_do_not_capture_topic_tags(self):
        tags=set()
        for path in (ROOT/'_posts').glob('*.md'):
            tags.update(frontmatter.load(path).get('tags',[]))
        aliases={alias for category in self.categories for alias in category['aliases']}
        self.assertFalse(tags & aliases)
        self.assertNotIn('Epistemology',aliases)

if __name__=='__main__': unittest.main()
