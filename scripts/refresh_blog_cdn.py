"""Refresh Blogger's exact public asset URLs and verify delivered bytes.

A successful purge response is not proof of delivery. No cache-busting query
is used for verification: it must be the URL already referenced by Blogger.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
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
        return response.read()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_asset(path: str, expected: bytes, *, fetch=get_bytes, sleep=time.sleep) -> dict:
    if path not in ASSETS:
        raise ValueError('Asset is outside the authorized allowlist')
    url = CDN_BASE + path
    wanted = digest(expected)
    first = fetch(url)
    if digest(first) == wanted:
        return {'path': path, 'sha256': wanted, 'verified': True, 'purged': False}

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
            return {'path': path, 'sha256': wanted, 'verified': True, 'purged': True}
        print(f'NOT_YET_DELIVERED {path}: {received}', flush=True)
    raise RuntimeError(f'CDN delivery mismatch for {path}: expected={wanted}, received={received}')


def main() -> int:
    try:
        for path in ASSETS:
            result = verify_asset(path, (ROOT / path).read_bytes())
            print('CDN_DELIVERY_VERIFIED ' + json.dumps(result, ensure_ascii=False), flush=True)
    except Exception as exc:
        print(f'CDN_DELIVERY_FAILED {type(exc).__name__}: {exc}', flush=True)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
