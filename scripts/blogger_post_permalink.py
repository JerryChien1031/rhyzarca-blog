"""Safe, versioned permalink publishing for Blogger Posts.

Blogger v3 has no documented customPermalink input. As this repository already
does for Pages, seed a *new* Post with an ASCII title, checkpoint its real ID,
then update the public-facing Chinese title and verify the returned URL.

An already-published post at another URL cannot be renamed this way: migration
creates a replacement Post, verifies it, checkpoints its ID, and only then
reverts the old Post to a restorable draft. Never delete the legacy Post.
"""
import re
from urllib.parse import urlsplit

_SLUG = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")
_PATH = re.compile(r"/20\d\d/(?:0[1-9]|1[0-2])/[a-z][a-z0-9-]*\.html\Z")


def require_slug(slug):
    if not isinstance(slug, str) or not _SLUG.fullmatch(slug) or len(slug) > 38:
        raise ValueError("blogger_permalink_slug must be ASCII lowercase kebab-case (max 38 chars)")
    return slug


def url_path(post):
    return urlsplit(str(post.get("url") or "")).path


def fetch_post(posts, blog_id, post_id):
    return posts.get(blogId=blog_id, postId=str(post_id), view="ADMIN").execute()


def find_matching_new_post(posts, blog_id, expected_path, marker):
    try:
        post = posts.getByPath(blogId=blog_id, path=expected_path, view="ADMIN").execute()
    except Exception as exc:
        if getattr(getattr(exc, "resp", None), "status", None) == 404:
            return None
        raise
    if marker not in str(post.get("content") or ""):
        raise ValueError("Blogger target permalink already belongs to an unrelated post; refusing takeover")
    return post


def assert_url(post, expected_path, expected_id=None):
    if not post.get("id"):
        raise ValueError("Blogger response missing real Post ID")
    if expected_id is not None and str(post["id"]) != str(expected_id):
        raise ValueError("Unexpected Blogger Post identity changed during update")
    actual = url_path(post)
    if actual != expected_path:
        raise ValueError(
            f"Unexpected Blogger permalink {actual or '(missing)'}; expected {expected_path}. "
            "Do not declare success or create another copy.")
    if str(post.get("status") or "LIVE") not in ("LIVE", ""):
        raise ValueError("Blogger Post is not LIVE")
    return post


def check_legacy_for_migration(posts, blog_id, old_id, expected_old_path, expected_title):
    old = fetch_post(posts, blog_id, old_id)
    if str(old.get("id")) != str(old_id):
        raise ValueError("Legacy Blogger Post identity mismatch")
    if url_path(old) != expected_old_path:
        raise ValueError("Legacy URL no longer matches the explicit migration precondition")
    if str(old.get("title") or "") != expected_title:
        raise ValueError("Legacy post title mismatch; refusing to migrate another article")
    status = old.get("status")
    if status not in ("LIVE", "DRAFT"):
        raise ValueError("Legacy Post must be LIVE or previously reverted to DRAFT")
    comments = (old.get("replies") or {}).get("totalItems")
    if comments is None:
        raise ValueError("Cannot confirm whether legacy Post has comments; refusing migration")
    if int(comments):
        raise ValueError("Legacy Post has comments; use reviewed Blogger UI migration instead")
    return old


def retire_legacy(posts, blog_id, legacy_id, old_path, title):
    if not legacy_id:
        return
    old = check_legacy_for_migration(posts, blog_id, legacy_id, old_path, title)
    if old["status"] == "LIVE":
        posts.revert(blogId=blog_id, postId=str(legacy_id)).execute()
        status = fetch_post(posts, blog_id, legacy_id).get("status")
        if status != "DRAFT":
            raise ValueError("Legacy Post revert not confirmed; migration incomplete")


def upsert_with_permalink(
        service, blog_id, *, title, html_content, labels,
        slug, expected_path, current_post_id=None,
        migration_from_id=None, expected_old_path=None, checkpoint):
    """Return the verified LIVE post; checkpoint(new id/url/legacy id) *before* retiring old."""
    require_slug(slug)
    if not _PATH.fullmatch(expected_path) or not expected_path.endswith("/" + slug + ".html"):
        raise ValueError("Expected Blogger URL does not match date/slug")
    if migration_from_id is not None and (not str(migration_from_id).isdigit()
                                          or not expected_old_path
                                          or not _PATH.fullmatch(expected_old_path)):
        raise ValueError("Legacy migration requires exact numeric Post ID and old path")
    posts = service.posts()
    legacy_id = str(migration_from_id) if migration_from_id else None
    if current_post_id:
        current = fetch_post(posts, blog_id, current_post_id)
        if url_path(current) == expected_path:
            # Existing target: update the same published post, do not change its permalink.
            marked_html = '<div data-rhyzarca-post-key="%s">\n%s\n</div>' % (slug, html_content)
            updated = posts.update(
                blogId=blog_id, postId=str(current_post_id),
                body={"title": title, "content": marked_html, "labels": labels}
            ).execute()
            assert_url(updated, expected_path, current_post_id)
            checkpoint(str(updated["id"]), updated["url"], legacy_id)
            if legacy_id and legacy_id != str(updated["id"]):
                retire_legacy(posts, blog_id, legacy_id, expected_old_path, title)
            return updated

        # Only specifically whitelisted existing source may be migrated.
        if legacy_id != str(current_post_id):
            raise ValueError("Existing Blogger Post has a different permalink; migration was not authorized")
        check_legacy_for_migration(posts, blog_id, legacy_id, expected_old_path, title)

    marker = 'data-rhyzarca-post-key="%s"' % slug
    marked_html = '<div %s>\n%s\n</div>' % (marker, html_content)
    candidate = find_matching_new_post(posts, blog_id, expected_path, marker)

    if candidate is None:
        # Blogger creates the slug from the initial ASCII title. This Post is
        # new, so its ID necessarily differs from the old published Post ID.
        candidate = posts.insert(
            blogId=blog_id,
            body={"title": slug, "content": marked_html, "labels": labels}
        ).execute()
        if not candidate.get("id"):
            raise ValueError("New Blogger Post lacks ID; inspect remote state before retry")
        if url_path(candidate) != expected_path:
            # Preserve legacy LIVE. Do not adopt or repeatedly create wrong URLs.
            posts.revert(blogId=blog_id, postId=str(candidate["id"])).execute()
            raise ValueError("Blogger produced an unexpected slug; candidate reverted to draft")
        checkpoint(str(candidate["id"]), candidate["url"], legacy_id)
    else:
        assert_url(candidate, expected_path)
        checkpoint(str(candidate["id"]), candidate["url"], legacy_id)

    updated = posts.update(
        blogId=blog_id, postId=str(candidate["id"]),
        body={"title": title, "content": marked_html, "labels": labels}
    ).execute()
    assert_url(updated, expected_path, candidate["id"])
    checkpoint(str(updated["id"]), updated["url"], legacy_id)
    if legacy_id and legacy_id != str(updated["id"]):
        retire_legacy(posts, blog_id, legacy_id, expected_old_path, title)
    return updated
