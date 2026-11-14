"""Verify the exact asset URLs deployed in Blogger's public theme.

A successful purge response is not proof of delivery. Discover the real theme
URLs first, then compare their served bytes with this checkout. Immutable
commit URLs avoid branch-origin caches; an old pinned version must still fail.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BLOG_URL = 'https://blog.rhyzarca.com/'
CDN_BASE = 'https://cdn.jsdelivr.net/gh/jerrychien1031/rhyzarca-blog@main/'
PURGE_BASE = 'https://purge.jsdelivr.net/gh/jerrychien1031/rhyzarca-blog@main/'
ASSETS = ('assets/css/blogger.css', 'assets/js/blogger.js')
DELAYS = (0, 10, 25, 45)


def get_bytes(url: str) -> bytes:
    request = Request(url, headers={'Accept-Encoding': 'identity',
                                   'User-Agent': 'Rhyzarca-CDN-Delivery-Check/1.0'})
    with urlopen(request, timeout=25) as response:
        if response.status != 200:
            raise RuntimeError(f'Unexpected HTTP status: {response.status}')
        if response.geturl() != url:
            raise RuntimeError(f'Unexpected redirect while checking {url}')
        return response.read()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def asset_revision(path: str, url: str) -> str:
    if path not in ASSETS:
        raise ValueError('Asset is outside the authorized allowlist')
    parsed = urlsplit(url)
    match = re.fullmatch(
        r'/gh/jerrychien1031/rhyzarca-blog@(main|[0-9a-f]{40})/' + re.escape(path),
        parsed.path,
    )
    if (parsed.scheme != 'https' or parsed.netloc != 'cdn.jsdelivr.net'
            or parsed.query or parsed.fragment or not match):
        raise ValueError(f'Unsupported deployed asset URL: {url}')
    return match.group(1)


def deployed_asset_urls(html: str) -> dict[str, str]:
    found = {path: [] for path in ASSETS}

    class ThemeAssets(HTMLParser):
        def handle_starttag(self, tag, attrs):
            names = [name for name, _ in attrs]
            relevant = ('src',) if tag == 'script' else ('href', 'rel') if tag == 'link' else ()
            if any(names.count(name) > 1 for name in relevant):
                raise ValueError(f'Duplicate asset attribute in {tag}')
            attrs = dict(attrs)
            if tag == 'script':
                path, url = 'assets/js/blogger.js', attrs.get('src', '')
            elif tag == 'link' and 'stylesheet' in attrs.get('rel', '').lower().split():
                path, url = 'assets/css/blogger.css', attrs.get('href', '')
            else:
                return
            if urlsplit(url).path.endswith('/' + path):
                asset_revision(path, url)
                found[path].append(url)

    ThemeAssets().feed(html)
    for path, urls in found.items():
        if len(urls) != 1:
            raise RuntimeError(f'Expected one deployed URL for {path}, found {len(urls)}')
    return {path: urls[0] for path, urls in found.items()}


def verify_asset(path: str, expected: bytes, *, url: str | None = None,
                 fetch=get_bytes, sleep=time.sleep) -> dict:
    url = url if url is not None else CDN_BASE + path
    revision = asset_revision(path, url)
    wanted = digest(expected)
    first = fetch(url)
    if digest(first) == wanted:
        return {'path': path, 'url': url, 'sha256': wanted, 'verified': True, 'purged': False}

    if revision != 'main':
        raise RuntimeError(f'CDN delivery mismatch for immutable {url}: '
                           f'expected={wanted}, received={digest(first)}; '
                           'update the Blogger theme to the intended commit')

    print(f'STALE {path}: expected={wanted} received={digest(first)}', flush=True)
    purge = json.loads(fetch(PURGE_BASE + path))
    if purge.get('status') not in ('finished', 'pending'):
        raise RuntimeError(f'CDN purge rejected for {path}')
    print(f'PURGE_REQUESTED {path}: {purge.get("status")}', flush=True)
    received = digest(first)
    for delay in DELAYS:
        if delay:
            sleep(delay)
        received = digest(fetch(url))
        if received == wanted:
            return {'path': path, 'url': url, 'sha256': wanted, 'verified': True, 'purged': True}
        print(f'NOT_YET_DELIVERED {path}: {received}', flush=True)
    raise RuntimeError(f'CDN delivery mismatch for {path}: expected={wanted}, received={received}')


def main() -> int:
    try:
        urls = deployed_asset_urls(get_bytes(BLOG_URL).decode('utf-8'))
        for path in ASSETS:
            result = verify_asset(path, (ROOT / path).read_bytes(), url=urls[path], fetch=get_bytes)
            print('CDN_DELIVERY_VERIFIED ' + json.dumps(result, ensure_ascii=False), flush=True)
    except Exception as exc:
        print(f'CDN_DELIVERY_FAILED {type(exc).__name__}: {exc}', flush=True)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
