"""Regression tests for new-post metadata, images and ID lifecycle."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_blog_article_contract.py"
SPEC = importlib.util.spec_from_file_location("blog_article_contract", SCRIPT)
contract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contract)


class BlogArticleContractTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.images = self.root / "assets" / "images" / "posts"
        self.images.mkdir(parents=True)
        self.stem = "2026-11-06-example-topic"
        self.image = f"/assets/images/posts/{self.stem}_1.svg"
        (self.images / f"{self.stem}_1.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" '
            'viewBox="0 0 1200 675"><rect width="1200" height="675"/></svg>',
            encoding="utf-8",
        )
        self.post = self.root / "_posts" / f"{self.stem}.md"
        self.post.parent.mkdir()
        self.good_text = (
            "---\nlayout: post\ntitle: '測試文章'\n"
            "date: 2026-11-06 09:00:00 +0800\n"
            "categories:\n  - insights\n"
            "tags:\n  - AI\n"
            "description: '短摘要'\n"
            "blogger_permalink_slug: example-topic\n"
            f"image: {self.image}\n---\n\n"
            f"![完整的封面替代文字]({self.image})\n\n"
            "*圖一：測試示意圖。*\n\n"
            "> **TL;DR**\n> 簡介。\n\n---\n\n"
            "### 一、正文\n\n以證據為本。\n"
        )
        self.post.write_text(self.good_text, encoding="utf-8")

    def errors(self):
        return contract.check_post(self.post, self.root)[0]

    def test_valid_draft_has_no_blogger_post_id(self):
        self.assertEqual([], self.errors())

    def test_missing_permalink_slug_is_error(self):
        self.post.write_text(self.good_text.replace("blogger_permalink_slug: example-topic\n", ""), encoding="utf-8")
        self.assertTrue(any("blogger_permalink_slug" in err for err in self.errors()))

    def test_missing_image_frontmatter_is_error(self):
        self.post.write_text(self.good_text.replace(f"image: {self.image}\n", ""), encoding="utf-8")
        self.assertTrue(any("image" in err for err in self.errors()))

    def test_post_id_must_not_be_guessed(self):
        self.post.write_text(
            self.good_text.replace("---\n\n", "blogger_post_id: 'TBD'\n---\n\n", 1),
            encoding="utf-8",
        )
        self.assertTrue(any("blogger_post_id" in err for err in self.errors()))

    def test_cover_must_precede_tldr(self):
        self.post.write_text(self.good_text.replace("![完整的封面替代文字]", "前言文字\n\n![完整的封面替代文字]"), encoding="utf-8")
        self.assertTrue(any("第一個內容" in err for err in self.errors()))

    def test_broken_reference_is_error(self):
        (self.images / f"{self.stem}_1.svg").unlink()
        self.assertTrue(any("不存在" in err for err in self.errors()))

    def test_legacy_is_not_retroactively_enforced(self):
        old = self.post.parent / "2026-10-22-old.md"
        old.write_text("---\nlayout: post\n---\n\n沒有圖片。", encoding="utf-8")
        self.assertEqual(([], True), contract.check_post(old, self.root))


if __name__ == "__main__":
    unittest.main()
