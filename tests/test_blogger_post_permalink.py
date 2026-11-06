"""Offline safety tests: Blogger permalink seeding and controlled identity migration."""
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from blogger_post_permalink import upsert_with_permalink

TARGET="/2026/11/human-ai-mutual-growth.html"
OLD="/2026/11/ai.html"
OLD_ID="4084431856132265811"
NEW_ID="9000000000000000001"
TITLE="從未知開始：當 AI 自行組織專業、擴充工具，與人類共同長出需求"
MARK='data-rhyzarca-post-key="human-ai-mutual-growth"'


class NotFound(Exception):
    def __init__(self):
        super().__init__("not found")
        self.resp=Mock(status=404)


def row(ident=NEW_ID, path=TARGET, title=TITLE, status="LIVE", comments="0", marked=True):
    return {"id":ident,"url":"https://blog.rhyzarca.com"+path,"title":title,
            "status":status,"replies":{"totalItems":comments},
            "content":("<div "+MARK+">sample</div>") if marked else "legacy text"}


def base(service, **extra):
    return upsert_with_permalink(
        service,"test-blog",title=TITLE,html_content="<p>sample</p>",
        labels=["insights"],slug="human-ai-mutual-growth",expected_path=TARGET,
        checkpoint=extra.pop("checkpoint",Mock()),**extra
    )


class PermalinkTests(unittest.TestCase):
    def test_new_post_seeds_ascii_title_then_changes_to_chinese(self):
        svc=Mock(); p=svc.posts.return_value
        p.getByPath.return_value.execute.side_effect=NotFound()
        p.insert.return_value.execute.return_value=row(title="human-ai-mutual-growth")
        p.update.return_value.execute.return_value=row()
        store=Mock()
        ret=base(svc,checkpoint=store)
        self.assertEqual(ret["id"],NEW_ID)
        self.assertEqual(p.insert.call_args.kwargs["body"]["title"],"human-ai-mutual-growth")
        self.assertEqual(p.update.call_args.kwargs["body"]["title"],TITLE)
        self.assertEqual(store.call_count,2)
        p.revert.assert_not_called()

    def test_existing_matching_post_keeps_same_id_and_does_not_insert(self):
        svc=Mock(); p=svc.posts.return_value
        p.get.return_value.execute.return_value=row()
        p.update.return_value.execute.return_value=row()
        store=Mock()
        base(svc,current_post_id=NEW_ID,checkpoint=store)
        p.insert.assert_not_called()
        p.getByPath.assert_not_called()
        p.revert.assert_not_called()
        store.assert_called_once_with(NEW_ID,"https://blog.rhyzarca.com"+TARGET,None)

    def test_old_wrong_permalink_without_explicit_migration_fails_closed(self):
        svc=Mock(); p=svc.posts.return_value
        p.get.return_value.execute.return_value=row(ident=OLD_ID,path=OLD,marked=False)
        with self.assertRaisesRegex(ValueError,"migration was not authorized"):
            base(svc,current_post_id=OLD_ID)
        p.insert.assert_not_called()
        p.revert.assert_not_called()

    def test_migrate_old_only_after_new_verified_and_checkpointed(self):
        svc=Mock(); p=svc.posts.return_value
        old=row(ident=OLD_ID,path=OLD,marked=False)
        p.get.return_value.execute.side_effect=[old,old,old,row(ident=OLD_ID,path=OLD,marked=False,status="DRAFT")]
        p.getByPath.return_value.execute.side_effect=NotFound()
        p.insert.return_value.execute.return_value=row(title="human-ai-mutual-growth")
        p.update.return_value.execute.return_value=row()
        store=Mock()
        base(svc,current_post_id=OLD_ID,migration_from_id=OLD_ID,
             expected_old_path=OLD,checkpoint=store)
        self.assertEqual(store.call_count,2)
        self.assertEqual(store.call_args.args[0],NEW_ID)
        self.assertEqual(store.call_args.args[2],OLD_ID)
        p.revert.assert_called_once_with(blogId="test-blog",postId=OLD_ID)
        p.insert.assert_called_once()

    def test_migration_with_comments_is_blocked_before_new_insert(self):
        svc=Mock(); p=svc.posts.return_value
        p.get.return_value.execute.return_value=row(ident=OLD_ID,path=OLD,comments="2",marked=False)
        with self.assertRaisesRegex(ValueError,"has comments"):
            base(svc,current_post_id=OLD_ID,migration_from_id=OLD_ID,expected_old_path=OLD)
        p.insert.assert_not_called()
        p.revert.assert_not_called()

    def test_migration_unknown_comment_count_is_blocked(self):
        svc=Mock();p=svc.posts.return_value
        old=row(ident=OLD_ID,path=OLD,marked=False)
        old["replies"]={}
        p.get.return_value.execute.return_value=old
        with self.assertRaisesRegex(ValueError,"Cannot confirm"):
            base(svc,current_post_id=OLD_ID,migration_from_id=OLD_ID,expected_old_path=OLD)
        p.insert.assert_not_called()

    def test_existing_target_path_with_wrong_key_is_not_adopted(self):
        svc=Mock();p=svc.posts.return_value
        p.getByPath.return_value.execute.return_value=row(marked=False)
        with self.assertRaisesRegex(ValueError,"unrelated post"):
            base(svc)
        p.insert.assert_not_called()

    def test_resume_candidate_after_lost_insert_response(self):
        svc=Mock();p=svc.posts.return_value
        p.getByPath.return_value.execute.return_value=row(title="human-ai-mutual-growth")
        p.update.return_value.execute.return_value=row()
        store=Mock()
        base(svc,checkpoint=store)
        p.insert.assert_not_called()
        self.assertEqual(store.call_count,2)

    def test_legacy_id_mismatch_cannot_migrate_unauthorized_post(self):
        svc=Mock();p=svc.posts.return_value
        p.get.return_value.execute.return_value=row(ident=OLD_ID,path=OLD)
        with self.assertRaisesRegex(ValueError,"not authorized"):
            base(svc,current_post_id=OLD_ID,migration_from_id="99999",expected_old_path=OLD)
        p.insert.assert_not_called()

    def test_unexpected_slug_is_reverted_without_retiring_original(self):
        svc=Mock();p=svc.posts.return_value
        p.getByPath.return_value.execute.side_effect=NotFound()
        p.insert.return_value.execute.return_value=row(path="/2026/11/human-ai-mutual-growth_10.html")
        with self.assertRaisesRegex(ValueError,"unexpected slug"):
            base(svc)
        p.revert.assert_called_once_with(blogId="test-blog",postId=NEW_ID)


if __name__=="__main__":
    unittest.main()
