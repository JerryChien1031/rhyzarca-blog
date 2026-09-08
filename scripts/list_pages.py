"""Read-only inspection of existing Blogger Pages; never prints credentials."""
from blogger_api import get_blogger_service, list_pages
from sync_to_blogger import BLOG_ID


def main():
    if not BLOG_ID:
        raise RuntimeError('BLOGGER_BLOG_ID is missing.')
    for page in list_pages(get_blogger_service(), BLOG_ID):
        print({key: page.get(key) for key in ('id', 'title', 'url', 'status')})


if __name__ == '__main__':
    main()
