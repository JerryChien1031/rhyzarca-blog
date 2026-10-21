---
blogger_page_id: '5648847046636893072'
blogger_page_url: https://blog.rhyzarca.com/p/blogger-tool.html
description: 將個人 GitHub Repository 的 Markdown 文章與固定頁面同步到本人管理的 Blogger，說明用途、授權與資料處理方式。
page_key: blogger-tool
title: Rhyzarca Blogger 同步工具
---

# Rhyzarca Blogger 同步工具

最後更新：2026-10-22。

Rhyzarca Blogger 同步工具是 Jerry Chien 自用的文章發布工具，用來把個人 GitHub Repository 中的 Markdown 文章與固定頁面，轉換成 HTML 後同步到本人有權管理的 Blogger。它讓文章原始檔、圖片與版本紀錄能保存在 GitHub，再由 Blogger 提供公開閱讀頁面。

這個工具目前只供操作者本人使用，沒有對外開放註冊，也不接受其他讀者連結 Google 帳戶。這份介紹及相關政策僅說明 Blogger 同步工具，不代表其他 Rhyzarca 網站、AI 助理或日後服務的資料處理方式。

## 工具如何運作

操作者先在 Google 官方授權頁面登入，授予工具存取 Blogger 的權限。工具取得授權憑證後，能在本機或 GitHub Actions 執行，不必每次同步都重新登入。Google 密碼由 Google 處理，工具不要求操作者把密碼填入 Repository 或同步腳本。

同步時，工具讀取指定 Repository 的 Markdown 內容，產生文章標題、HTML、標籤與分類，再向指定 Blogger 網誌建立或更新文章。固定頁面則會先比對已有的 Page 身分，避免在找不到或無法確定對應頁面時直接覆寫其他內容。成功回應所提供的文章或頁面識別碼，以及固定頁面的實際網址，會寫回來源檔案，供下次同步使用。

目前 GitHub Actions 設定會在 `main` 分支上符合條件的文章、固定頁面、程式或資產變更後啟動同步，也提供手動執行入口。因此，合併或 Push 這些變更可能直接建立或修改公開內容，不等同於只儲存草稿。

## 為什麼需要 Google 授權

目前程式請求的 OAuth 範圍為 `https://www.googleapis.com/auth/blogger`，用於建立及更新 Blogger 文章與固定頁面。這是具有管理能力的授權，範圍大於單純讀取公開文章；工具目前沒有實作刪除 Blogger 內容的功能，但這不會縮小 Google 授權本身的權限範圍。

健康檢查會讀取已授權帳戶可管理的網誌清單。固定頁面同步會讀取頁面的標題、內容、狀態、識別碼及網址，辨識應更新的目標。授權憑證的保存、資料用途與撤銷方式，請見[隱私權政策](https://blog.rhyzarca.com/p/blogger-privacy.html)。

## 公開內容與私人憑證

文章、固定頁面及公開圖片原本就是準備對外發布的內容，可能出現在公開 GitHub Repository、Blogger 與圖片 CDN。Google 授權憑證則保存於操作者的本機授權檔或 GitHub Actions Secrets，不應放進公開原始碼、文章或圖片目錄。

撤銷 Google 授權會阻止工具繼續取得對應的存取權限，但不會自動刪除已發布的文章，也不會清除本機授權檔、GitHub Secret、Git 版本紀錄或 CDN 快取。停止使用時，需分別處理授權、工作流程與已保存的資料。

## 使用前應了解的限制

同步包含多個獨立的 API 操作，不是能整批回復的單一交易。一篇文章失敗時，其他文章仍可能已經成功；網路中斷也可能發生在 Blogger 已接受操作、但工具尚未收到回應的時候。操作者應先核對 Blogger 的實際結果，再決定重試或手動修正。

Google 授權可能因撤銷、到期或其他服務政策失效。OAuth 的 Production 狀態也不代表 Token 永遠有效，或代表 Google 已審核、認可這個工具。

## 政策、原始碼與聯絡方式

- [隱私權政策](https://blog.rhyzarca.com/p/blogger-privacy.html)：存取資料、使用目的、儲存、分享及刪除方式。
- [使用條款](https://blog.rhyzarca.com/p/blogger-terms.html)：適用對象、發布責任、失敗處理與停止使用。
- [公開原始碼](https://github.com/JerryChien1031/rhyzarca-blog)。
- [Rhyzarca Blog](https://blog.rhyzarca.com/)。
- 操作者與聯絡窗口：Jerry Chien，電子郵件 [jerrychien1031@gmail.com](mailto:jerrychien1031@gmail.com)。