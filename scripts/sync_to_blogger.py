import os
import glob
import time
import frontmatter
from markdown_parser import parse_and_convert
from blogger_api import get_blogger_service, publish_post
from dotenv import load_dotenv

# 1. 載入位於 scripts 底下的 .env 檔案
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
BLOG_ID = os.getenv('BLOGGER_BLOG_ID')

# 2. 定義路徑：根目錄下的 _posts 資料夾
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
POSTS_DIR = os.path.join(PROJECT_ROOT, '_posts')

def update_markdown_frontmatter(filepath, post_id):
    """
    將成功發布後取得的 blogger_post_id 寫回 Markdown 檔案的 Frontmatter 中
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
    
    post.metadata['blogger_post_id'] = post_id
    
    # 寫回檔案
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))

def main():
    if not BLOG_ID:
        print("❌ 錯誤：未在 .env 檔案中找到 BLOGGER_BLOG_ID！")
        return

    print("正在連線至 Blogger API...")
    service = get_blogger_service()
    
    if not os.path.exists(POSTS_DIR):
        print(f"❌ 錯誤找不到 _posts 資料夾: {POSTS_DIR}")
        return

    md_files = glob.glob(os.path.join(POSTS_DIR, '*.md'))
    print(f"📁 找到共 {len(md_files)} 篇 Markdown 文章。")
    
    for filepath in md_files:
        filename = os.path.basename(filepath)
        print(f"\n----------------------------------------")
        print(f"正在處理檔案: {filename}")
        
        try:
            # 先讀取原始 Frontmatter 以取得 blogger_post_id
            with open(filepath, 'r', encoding='utf-8') as f:
                raw_post = frontmatter.load(f)
            blogger_post_id = raw_post.metadata.get('blogger_post_id')

            # 轉譯 HTML 與取得 Metadata
            metadata, html_content = parse_and_convert(filepath)
            title = metadata.get('title', '無標題')
            tags = metadata.get('tags', [])
            categories = metadata.get('categories', [])
            labels = list(set(tags + categories))
            
            if not blogger_post_id:
                print(f"👉 狀態：尚未發布，正在發布新文章「{title}」...")
                new_post_id = publish_post(service, BLOG_ID, title, html_content, labels)
                print(f"✅ 發布成功！Blogger 文章 ID: {new_post_id}")
                
                # 自動將 ID 寫回 Markdown 檔案
                update_markdown_frontmatter(filepath, new_post_id)
                print(f"📝 已自動將 blogger_post_id 寫回 Markdown 檔案。")
                
                time.sleep(10)
            else:
                print(f"👉 狀態：已發布過 (ID: {blogger_post_id})，正在更新內容...")
                publish_post(service, BLOG_ID, title, html_content, labels, existing_post_id=blogger_post_id)
                print(f"✅ 更新成功！")
                time.sleep(5)
                
        except Exception as e:
            print(f"❌ 同步檔案 {filename} 失敗: {e}")
            time.sleep(10)

if __name__ == '__main__':
    main()
