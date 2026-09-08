import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import re
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
from googleapiclient.errors import HttpError

# 設定我們需要的權限：管理 Blogger
SCOPES = ['https://www.googleapis.com/auth/blogger']

def get_blogger_service(client_secret_file='client_secret.json', token_file='token.json'):
    """
    取得授權並建立 Blogger API 的通訊客戶端 (Service Object)。
    """
    creds = None

    token_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), token_file)
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds:
        raise RuntimeError('Existing Blogger OAuth token required; no interactive login.')
    if not creds.valid:
        if not creds.refresh_token:
            raise RuntimeError('Blogger token cannot be refreshed.')
        creds.refresh(Request())
        with open(token_file, 'w', encoding='utf-8') as token:
            token.write(creds.to_json())

    return build('blogger', 'v3', credentials=creds)

def publish_post(service, blog_id, title, html_content, labels=None, existing_post_id=None):
    """
    將文章發布或更新到 Blogger。
    如果提供了 existing_post_id，則執行覆蓋更新 (Update)；否則執行新增 (Insert)。
    """
    post_data = {
        'title': title,
        'content': html_content,
        'labels': labels or []
    }

    try:
        if existing_post_id:
            # 執行更新
            request = service.posts().update(blogId=blog_id, postId=existing_post_id, body=post_data)
        else:
            # 執行新增
            request = service.posts().insert(blogId=blog_id, body=post_data)

        response = request.execute()
        return response.get('id')

    except Exception as e:
        print(f"API 呼叫失敗: {e}")
        raise

def list_pages(service, blog_id):
    # Current v3 discovery supports pagination and uppercase status enums.
    pages = {}
    token = None
    while True:
        response = service.pages().list(
            blogId=blog_id, fetchBodies=True, view='ADMIN',
            status=['LIVE', 'DRAFT', 'SOFT_TRASHED'], maxResults=100,
            **({'pageToken': token} if token else {})
        ).execute()
        for page in response.get('items', []):
            pages[str(page['id'])] = page
        token = response.get('nextPageToken')
        if not token:
            return list(pages.values())


def get_page(service, blog_id, page_id):
    return service.pages().get(blogId=blog_id, pageId=str(page_id)).execute()


def insert_page(service, blog_id, title, content):
    # Never retry insert automatically: a lost response may have created it.
    return service.pages().insert(
        blogId=blog_id, isDraft=False, body={'title': title, 'content': content}
    ).execute()


def update_page(service, blog_id, page_id, title, content):
    return service.pages().update(
        blogId=blog_id, pageId=str(page_id), publish=True,
        body={'title': title, 'content': content}
    ).execute()


def page_keys(page):
    soup = BeautifulSoup(page.get('content', ''), 'html.parser')
    return {el['data-rhyzarca-page-key'] for el in
            soup.select('[data-rhyzarca-page-key]')}


def resolve_page(service, blog_id, metadata):
    key = metadata['page_key']
    pages = list_pages(service, blog_id)
    saved_id = str(metadata.get('blogger_page_id') or '')
    if saved_id and not any(str(p['id']) == saved_id for p in pages):
        try:
            pages.append(get_page(service, blog_id, saved_id))
        except HttpError as exc:
            if exc.resp.status != 404:
                raise
    paths = {f'/p/{key}.html'}
    if metadata.get('blogger_page_url'):
        paths.add(urlsplit(metadata['blogger_page_url']).path)
    matches = [p for p in pages if str(p['id']) == saved_id or
               urlsplit(p.get('url', '')).path in paths or key in page_keys(p)]
    if not matches:
        matches = [p for p in pages if p.get('title') in (metadata['title'], key)]
    if len(matches) > 1:
        raise ValueError(f'Ambiguous Page identity for {key}; refusing overwrite or insert.')
    if matches:
        page = matches[0]
        if page_keys(page) - {key}:
            raise ValueError(f'Conflicting managed Page key for {key}.')
        if page.get('status', 'LIVE') not in ('LIVE', 'DRAFT'):
            raise ValueError(f'Existing Page {key} is not LIVE; refusing duplicate creation.')
        return page
    if saved_id or metadata.get('blogger_page_url'):
        raise ValueError(f'Saved Page identity for {key} missing; refusing replacement.')
    return None


def upsert_page(service, blog_id, metadata, html_content, checkpoint):
    key = metadata.get('page_key', '')
    if not re.fullmatch(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)*', key):
        raise ValueError('page_key must be a stable lowercase ASCII slug.')
    content = f'<div data-rhyzarca-page-key="{key}">\n{html_content}\n</div>'
    page = resolve_page(service, blog_id, metadata)
    if page is None:
        # No documented slug field: seed with ASCII title, then rename.
        page = insert_page(service, blog_id, key, content)
        checkpoint(page)
    page = update_page(service, blog_id, page['id'], metadata['title'], content)
    checkpoint(page)
    if urlsplit(page['url']).path != f'/p/{key}.html':
        raise ValueError(f"Unexpected Blogger URL: {page['url']}; identity saved, no reinsertion.")
    return page
