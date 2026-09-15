import os
import frontmatter
import markdown
from bs4 import BeautifulSoup

# 將此處替換為您的 GitHub 使用者名稱與倉庫名稱
# 格式為：https://cdn.jsdelivr.net/gh/使用者名稱/倉庫名稱@main
CDN_BASE_URL = "https://cdn.jsdelivr.net/gh/jerrychien1031/rhyzarca-blog@main"

def parse_and_convert(filepath):
    """
    讀取 Markdown 檔案，解析 Frontmatter，
    將內文轉為 HTML，並替換圖片為 CDN 絕對路徑。
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"找不到檔案: {filepath}")

    # 1. 讀取並解析 Frontmatter
    with open(filepath, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    metadata = post.metadata
    content = post.content

    # 2. Markdown 轉 HTML
    # 使用 'extra' 擴充以支援表格 (tables)、定義清單、縮寫等語法
    # 使用 'sane_lists' 讓清單行為更符合預期
    # 加入 'nl2br' 確保一般換行能轉為 <br>
    html_content = markdown.markdown(content, extensions=['extra', 'sane_lists', 'nl2br'])

    # 3. 替換圖片路徑為 CDN 網址
    soup = BeautifulSoup(html_content, 'html.parser')
    for img in soup.find_all('img'):
        src = img.get('src')
        if src and src.startswith('/assets/images/'):
            # 將本地相對路徑替換為 jsDelivr CDN 絕對路徑
            img['src'] = f"{CDN_BASE_URL}{src}"

    # 將處理後的 HTML 轉回字串
    final_html = str(soup)
    return metadata, final_html

if __name__ == "__main__":
    # 簡單的本地測試
    # 指定一篇確實存在的文章來測試
    test_file = "../_posts/2026-08-17-why-rhyzarca-origin-and-value.md"
    try:
        if os.path.exists(test_file):
            print(f"正在測試解析檔案: {test_file}")
            meta, html = parse_and_convert(test_file)
            print("\n--- 取得的 Metadata ---")
            print(meta)
            print("\n--- 轉換後的 HTML (前 500 字元) ---")
            print(html[:500] + "...")
        else:
            print(f"測試檔案 {test_file} 不存在，請確認路徑。")
    except Exception as e:
        print(f"測試發生錯誤: {e}")
