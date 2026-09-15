# scripts/check_blogger_auth.py
import os
import sys
from blogger_api import get_blogger_service

def main():
    print("開始檢查 Blogger API 授權狀態...")
    try:
        # 嘗試取得授權與 Service 物件
        # 這會讀取 scripts/client_secret.json 和 scripts/token.json
        service = get_blogger_service()
        
        # 進行一個最簡單、不會修改資料的 API 呼叫來驗證 Token
        # 這裡嘗試讀取使用者自己的網誌清單
        blogs = service.blogs().listByUser(userId='self').execute()
        
        if 'items' in blogs:
            print("✅ 憑證健康檢查通過：成功讀取 Blogger 網誌清單。")
            sys.exit(0) # 成功退出
        else:
            print("✅ 憑證健康檢查通過：但找不到任何網誌。")
            sys.exit(0)

    except Exception as e:
        print(f"❌ 憑證檢查失敗，可能 Token 已過期或被撤銷: {e}")
        # 如果是 401 錯誤（通常是 token invalid_grant），程式會走到這裡
        sys.exit(1) # 回傳非 0 值，讓 GitHub Actions 標記為失敗

if __name__ == '__main__':
    main()

