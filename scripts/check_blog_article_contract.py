#!/usr/bin/env python3
"""Validate the Rhyzarca Blog *new-post* contract; read-only, no publishing.

The canonical publishing converter remains scripts/markdown_parser.py.
This checker intentionally ignores pre-2026-11-06 historical posts.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

import yaml
from PIL import Image

REPO = Path(__file__).resolve().parents[1]
START_DATE = "2026-11-06"
REQUIRED = ("layout", "title", "date", "categories", "tags", "description", "image")
IMAGE_RE = re.compile(r"!\[(?P<alt>[^\]\n]*)\]\((?P<url>[^)\s]+)\)")
LOCAL_PREFIX = "/assets/images/posts/"
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".svg"}


def image_file(path: str, repo: Path) -> Path | None:
    if not path.startswith(LOCAL_PREFIX) or "?" in path or "#" in path or "\\" in path:
        return None
    relative = Path(path.lstrip("/"))
    if ".." in relative.parts:
        return None
    target = (repo / relative).resolve()
    try:
        target.relative_to(repo.resolve())
    except ValueError:
        return None
    return target


def check_picture(path: Path, *, cover: bool) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"圖片檔案不存在：{path}"]
    if path.suffix.lower() not in IMAGE_EXTS:
        return [f"圖片格式不支援：{path}"]
    if path.stat().st_size > 200 * 1024:
        errors.append(f"圖片大於 200 KiB：{path.name}；請壓縮或說明必要性")
    try:
        if path.suffix.lower() == ".svg":
            root = ET.parse(path).getroot()
            if root.tag != "{http://www.w3.org/2000/svg}svg":
                errors.append("SVG 的根節點不是正式 SVG")
            w = float(root.attrib.get("width", "0"))
            h = float(root.attrib.get("height", "0"))
            for element in root.iter():
                local_tag = element.tag.rsplit("}", 1)[-1]
                if local_tag in {"script", "foreignObject"}:
                    errors.append(f"SVG 包含不允許的 {local_tag} 元素：{path.name}")
                for key, value in element.attrib.items():
                    attr = key.rsplit("}", 1)[-1].lower()
                    if attr in {"href", "src"} and re.match(r"(?i)^(?:https?:|data:|javascript:)", value):
                        errors.append(f"SVG 含外部資源：{path.name}")
        else:
            with Image.open(path) as picture:
                w, h = picture.size
                picture.verify()
    except Exception as exc:
        return [f"無法讀取或驗證圖片 {path.name}：{type(exc).__name__}"]
    if cover and (w < 1200 or h < 675 or abs(w / h - 16 / 9) > 0.025):
        errors.append(f"封面須為至少 1200x675、16:9；目前 {path.name} 為 {w:g}x{h:g}")
    return errors


def check_post(path: Path, repo: Path = REPO) -> tuple[list[str], bool]:
    """Return (errors, is_legacy). Does not modify files."""
    errors: list[str] = []
    if not path.is_file():
        return [f"文章不存在：{path}"], False
    if path.name[:10] < START_DATE:
        return [], True
    source = path.read_text(encoding="utf-8-sig")
    matched = re.match(r"\A---\s*\n(?P<front>.*?)\n---\s*\n(?P<body>.*)\Z", source, re.S)
    if matched is None:
        return ["缺少有效 YAML Front Matter（須以 --- 包住）"], False
    try:
        meta = yaml.safe_load(matched["front"])
    except yaml.YAMLError as exc:
        return [f"YAML 解析失敗：{str(exc).splitlines()[0]}"], False
    if not isinstance(meta, dict):
        return ["Front Matter 必須是 YAML mapping"], False
    body = matched["body"]
    for field in REQUIRED:
        value = meta.get(field)
        if value is None or value == "" or value == []:
            errors.append(f"缺少必要欄位／值：{field}")
    if meta.get("layout") != "post":
        errors.append("layout 必須為 post")
    if not isinstance(meta.get("title"), str) or not meta.get("title", "").strip():
        errors.append("title 必須是非空字串")
    if not isinstance(meta.get("description"), str) or not meta.get("description", "").strip():
        errors.append("description 必須是非空字串")
    if isinstance(meta.get("description"), str) and len(meta["description"]) > 180:
        errors.append("description 過長；請濃縮至 180 字元內（建議約 120 個中文字）")
    for field in ("categories", "tags"):
        if not isinstance(meta.get(field), list) or not all(
            isinstance(v, str) and v.strip() for v in meta[field]
        ):
            errors.append(f"{field} 必須是非空字串列表")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}-.+\.md", path.name):
        errors.append("檔名須為 YYYY-MM-DD-slug.md")
    raw_date = re.search(r"(?m)^date:\s*(.*?)\s*$", matched["front"])
    if not raw_date or not raw_date.group(1).startswith(path.name[:10]) or "+0800" not in raw_date.group(1):
        errors.append("date 必須與檔名日期一致並標記 +0800")
    if "blogger_blog_id" in meta or "BLOGGER_BLOG_ID" in meta:
        errors.append("整站 Blogger Blog ID 不得寫在文章 Front Matter")
    if "blogger_post_id" in meta:
        post_id = meta["blogger_post_id"]
        if not isinstance(post_id, str) or not re.fullmatch(r"\d{8,25}", post_id):
            errors.append("blogger_post_id 必須是已發佈文章的真實數字字串；草稿請省略")
    image_value = meta.get("image")
    if not isinstance(image_value, str) or not image_value.strip():
        image_value = ""
    pictures = list(IMAGE_RE.finditer(body))
    if not pictures:
        errors.append("本文沒有 Markdown 圖片；新文章需要首圖")
        return errors, False
    content_start = body.lstrip()
    if not content_start.startswith(pictures[0].group(0)):
        errors.append("正文第一個內容項目必須是封面圖片（在 TL;DR 之前）")
    cover_src = pictures[0].group("url")
    if image_value != cover_src:
        errors.append("Front Matter 的 image 必須與正文第一張圖片路徑完全一致")
    if not body.find("> **TL;DR**") >= 0:
        errors.append("缺少 TL;DR")
    else:
        cover_end = pictures[0].end()
        tldr_pos = body.index("> **TL;DR**")
        if tldr_pos < cover_end:
            errors.append("TL;DR 必須出現在封面與圖說之後")
        elif tldr_pos - cover_end > 650:
            errors.append("封面後應緊接圖說與 TL;DR，不要插入長段正文")
    stem = path.stem
    for index, image in enumerate(pictures):
        alt = image.group("alt").strip()
        src = image.group("url")
        if not alt:
            errors.append(f"第 {index+1} 張圖缺少 Alt Text")
        target = image_file(src, repo)
        if target is None:
            errors.append(f"第 {index+1} 張圖必須是合法的 {LOCAL_PREFIX} 路徑：{src}")
            continue
        if not re.fullmatch(re.escape(stem) + r"_\d+\.(?:png|jpg|jpeg|webp|svg)", target.name, re.I):
            errors.append(f"第 {index+1} 張圖未符合本文檔名 _N 編號：{target.name}")
        if index == 0 and not re.search(r"_1\.(?:png|jpg|jpeg|webp|svg)$", target.name, re.I):
            errors.append("第一張封面應以 _1 代表")
        errors.extend(check_picture(target, cover=index == 0))
        after = body[image.end():].lstrip("\r\n ")
        first_line = after.split("\n", 1)[0].strip()
        if not (first_line.startswith("*圖") and first_line.endswith("*")):
            errors.append(f"第 {index+1} 張圖後缺少以 *圖...* 表達的圖說")
    if len(body) > 5000 and len(pictures) < 2:
        errors.append("長文需有接近結語的收束圖（第二張或更多）")
    if len(body) > 5000 and len(pictures) >= 2 and pictures[-1].start() < len(body) * .5:
        errors.append("長文的最後一張圖應放在正文後半段、接近結語")
    return errors, False


def check_conversion(path: Path, expected_count: int) -> list[str]:
    """Use the repository's *actual* Markdown → Blogger converter."""
    sys.path.insert(0, str(REPO / "scripts"))
    from markdown_parser import parse_and_convert
    from bs4 import BeautifulSoup
    try:
        metadata, html = parse_and_convert(str(path))
        soup = BeautifulSoup(html, "html.parser")
        if len(soup.find_all("img")) != expected_count:
            return [f"Blogger HTML 圖片數量不符：預期 {expected_count} 張"]
        for img in soup.find_all("img"):
            if not img.get("src", "").startswith(
                "https://cdn.jsdelivr.net/gh/jerrychien1031/rhyzarca-blog@main/assets/images/"
            ):
                return [f"Blogger HTML 圖片尚未轉為正確 CDN 路徑：{img.get('src')}"]
        if not metadata.get("title"):
            return ["Blogger 轉換後缺少文章標題"]
    except Exception as exc:
        return [f"既有正式 Markdown 轉換失敗：{type(exc).__name__}: {exc}"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("posts", nargs="+", type=Path)
    parser.add_argument("--verify-conversion", action="store_true")
    args = parser.parse_args()
    total = 0
    for arg in args.posts:
        path = arg if arg.is_absolute() else REPO / arg
        errors, legacy = check_post(path)
        if legacy:
            print(f"LEGACY SKIP {arg}（歷史文章不溯及）")
            continue
        if args.verify_conversion and not errors:
            body = path.read_text(encoding="utf-8-sig")
            errors.extend(check_conversion(path, len(IMAGE_RE.findall(body))))
        if errors:
            total += len(errors)
            print(f"FAIL {arg}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {arg}")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
