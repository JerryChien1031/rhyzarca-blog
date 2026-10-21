# scripts/check_blogger_auth.py
import os
import sys
from blogger_api import BloggerAuthorizationError, get_blogger_service

def main():
    print("開始檢查 Blogger API 授權狀態...")
    try:
        # 即使 Access Token 尚有效，也要確認 Refresh Token 能繼續使用。
        # 僅在記憶體刷新；健康檢查不覆寫既有憑證。
        service = get_blogger_service(force_refresh=True, persist_token=False)
        
        # 進行一個最簡單、不會修改資料的 API 呼叫來驗證 Token
        # 這裡嘗試讀取使用者自己的網誌清單
        blogs = service.blogs().listByUser(userId='self').execute()
        
        if 'items' in blogs:
            print("✅ 憑證健康檢查通過：成功讀取 Blogger 網誌清單。")
            return 0
        else:
            print("✅ 憑證健康檢查通過：但找不到任何網誌。")
            return 0

    except BloggerAuthorizationError as exc:
        print(f"❌ 憑證檢查失敗: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        # 原始 OAuth/API 例外可能含敏感資料，僅回報例外類型。
        print(f"❌ 憑證檢查失敗 ({type(exc).__name__})。請檢查網路、帳號及 Blogger 存取權。",
              file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())

