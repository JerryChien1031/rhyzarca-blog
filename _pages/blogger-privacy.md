---
blogger_page_id: '6380017173854469309'
blogger_page_url: https://blog.rhyzarca.com/p/blogger-privacy.html
description: 說明自用 Blogger 同步工具存取的 Google 資料、用途、憑證與內容保存方式，以及撤銷授權與刪除資料的差異。
page_key: blogger-privacy
title: Rhyzarca Blogger 同步工具｜隱私權政策
---

# Rhyzarca Blogger 同步工具隱私權政策

生效日期：2026-10-22。最後更新：2026-10-22。

## 適用範圍與操作者

本政策說明 Jerry Chien 操作的 Rhyzarca Blogger 同步工具如何處理資料。工具將個人 GitHub Repository 的 Markdown 文章與固定頁面同步到本人有權管理的 Blogger，目前僅供操作者本人使用，沒有對外開放帳戶註冊或接受其他使用者的 Google 授權。

本政策適用於這個同步工具及其授權、健康檢查與發布流程，不涵蓋其他 Rhyzarca 網站、AI 助理或第三方服務。工具功能概覽請見[工具介紹](https://blog.rhyzarca.com/p/blogger-tool.html)。

## 存取哪些資料，為什麼需要

工具使用 Google OAuth 授權，讓操作者在 Google 官方頁面同意存取 Blogger。工具不收取 Google 帳戶密碼。目前請求的權限範圍為 `https://www.googleapis.com/auth/blogger`，具有管理 Blogger 的能力，用於建立及更新文章與固定頁面。程式目前沒有刪除內容的功能，但授權本身不限於唯讀存取。

| 資料類型 | 來源與用途 | 保存方式 |
| --- | --- | --- |
| OAuth 存取權杖、更新權杖及相關授權設定 | Google 授權回應；代表操作者呼叫 Blogger API，並在必要時更新存取權杖 | 操作者的本機授權檔；供自動化使用的副本保存在 GitHub Actions Secrets，執行期間還原到 Runner 的授權檔 |
| 已授權帳戶的網誌清單與識別資訊 | Blogger API；健康檢查確認授權可用，並核對目標網誌 | 檢查期間處理；部分識別資訊可能出現在執行紀錄，不作為建立讀者名冊之用 |
| Blogger 固定頁面的標題、內容、狀態、識別碼及網址 | Blogger API；比對既有頁面，判斷應更新的目標 | 比對時在執行記憶體處理；管理中的頁面識別碼與實際網址會保存到來源 Markdown |
| 文章及頁面的標題、HTML 內容、標籤與分類 | Repository 中的 Markdown；向 Blogger 建立或更新內容 | Repository、Blogger，以及對應的版本紀錄 |
| API 回傳的文章或頁面識別碼、網址及執行結果 | Blogger API；保存同步身分、排查失敗及避免錯誤重建 | 來源 Markdown 與執行紀錄；紀錄也可能包含檔名、標題及錯誤訊息 |
| 公開圖片及靜態資產 | Repository；支援文章與頁面的顯示 | GitHub、公開 CDN 及其快取 |

授權範圍不包含 Gmail、Google Drive 或聯絡人權限，工具目前也不提供讀取這些服務的功能。這不代表 Blogger 內容一定不含個人資料；操作者仍須自行檢查準備發布的文字及圖片。

## 資料如何使用與分享

Google 授權資料及 API 回應用於完成操作者要求的 Blogger 同步、識別目標頁面、檢查授權和排查執行問題。依本政策，工具不將這些資料出售、用於廣告投放、建立廣告輪廓或信用評估，也不將 Google API 資料與憑證送入 AI 模型作為本工具功能的一部分。

本工具對從 Google API 取得資訊的使用與轉移，將遵守 [Google API Services User Data Policy](https://developers.google.com/terms/api-services-user-data-policy)，包括其中的有限使用（Limited Use）要求。操作者或經其明確授權的維護者，只能為本人要求的操作、必要的故障排查、安全維護或適用法律要求接觸相關資料，不能另作未揭露用途。

執行這些功能會涉及下列服務：

- **Google／Blogger**：處理 Google 登入與授權、更新 Token，並接收文章或頁面的讀取及發布請求。
- **GitHub／GitHub Actions**：保存 Repository 與版本紀錄、儲存供自動化使用的授權 Secret，並在 Runner 執行同步。執行紀錄依 Repository 的可見性及 GitHub 設定保存，不應視為私人資料保管區。
- **jsDelivr**：提供公開 Repository 中的圖片與靜態資產。工具不以 CDN 傳送 Google 授權憑證或私人 API 回應；讀者瀏覽公開資產時，仍會直接與 CDN 服務互動。

上述服務各自依其政策處理收到的資料。公開文章與圖片是操作者選擇對外發布的內容；這與私下保存的 OAuth 憑證不同。將私人資料寫進公開文章、Git 版本或執行紀錄後，不能僅靠撤銷 Google 授權收回副本。

## 儲存、安全與保存期間

本機授權檔及 GitHub Actions Secrets 由操作者管理。自動化執行時，Workflow 從 Secrets 還原授權檔及必要設定，並配置在執行結束時清理這些檔案的步驟。這是目前的處理方式，不代表所有本機副本、平台備份或意外中斷的環境都已經被證明完全清除。

憑證不應提交到公開 Repository，也不應加入文章、圖片或除錯輸出。若發現洩漏，操作者需要撤銷或輪替授權，並檢查曾保存或暴露資料的位置；單純刪除目前版本的檔案，不等同於移除 Git 歷史或既有副本。

工具目前沒有為所有資料設定統一的自動刪除期限。本機授權檔與 Secret 會保存至操作者刪除或更換；更換 Secret 不會自動刪除本機的舊授權檔。執行紀錄由 GitHub 的保存設定管理。文章、固定頁面及公開資產則依操作者的發布、刪除與版本管理操作保存，第三方快取或備份的移除時間由相應服務決定。

## 撤銷授權、停止使用與刪除資料

操作者可以在 [Google 帳戶的第三方連結管理頁面](https://myaccount.google.com/connections) 撤銷本工具的存取權，並停用 GitHub Actions 同步入口，阻止後續工作流程觸發的同步。撤銷授權不會自動刪除本機授權檔、GitHub Secret、已發布文章或保存於 Git 的身分紀錄。

若要停止使用並清理資料，需要依目的分別處理：移除不再需要的本機授權檔與 GitHub Secret；在 Blogger 管理已發布的文章或固定頁面；在 Repository 管理來源檔、圖片與版本紀錄。公開版本或第三方快取可能仍有副本，工具目前沒有能一次刪除所有副本的功能。

## 政策變更與聯絡方式

如未來擴大使用對象、Google 權限範圍或資料用途，操作者應先更新本政策及相關說明，並在需要時重新取得同意，不沿用本次自用授權去處理未揭露的用途。

對本工具的資料處理或刪除有疑問，可聯絡 Jerry Chien：[jerrychien1031@gmail.com](mailto:jerrychien1031@gmail.com)。來信請描述需求，不要附上 Token、Google 密碼或授權碼。

相關文件：[工具介紹](https://blog.rhyzarca.com/p/blogger-tool.html)、[使用條款](https://blog.rhyzarca.com/p/blogger-terms.html)。