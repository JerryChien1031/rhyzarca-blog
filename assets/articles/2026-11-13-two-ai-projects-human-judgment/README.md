# Life World 離線作品｜Rhyzarca Blog 單篇專屬資產

對應文章：`_posts/2026-11-13-two-ai-projects-human-judgment.md`  
資產目錄：`assets/articles/2026-11-13-two-ai-projects-human-judgment/`

本目錄是本次雙專案 Blog 文章的**獨立作品展示庫**，不是 Life World 正式產品的部署。四份 HTML 都來自使用者在本次對話提供的原始離線匯出檔，**原始內容逐位元組保留**；每份 HTML 內含必要資料、樣式、JavaScript 與嚴格的 CSP，沒有另外載入線上 API、憑證或私人環境。

| GitHub 檔名 | 原始作品 | Git Blob SHA（原檔核對） | 觀察定位 |
| --- | --- | --- | --- |
| `sea-town-route.html` | `海角小鎮一日遊（互動遊戲）.html` | `a76d079b315b8115261089ae4b1d847df96cd48c` | 行程選擇與同行者反應，並非「海線小鎮一日行」合成版圖檔 |
| `modern-hongmen-banquet.html` | `現代鴻門宴：會館裡的最後合約（互動版）.html` | `9a0236e9b912ca298c93908f8ff613d14e8e33aa` | 逐段閱讀、人物反應、真心話與結尾卡 |
| `bakery-empty-fortress.html` | `空城計：巷口麵包店的最後清晨（互動版）.html` | `d68c9a4c366109d20f4affe6988a54ca6a8ccf78` | 互動故事作品，角色與劇情均屬虛構 |
| `spring-under-ice-scroll.html` | `冰下之春（捲動劇情）.html` | `b820737a71e3c3ddac264e03995d7b79101f6fe0` | 捲動敘事作品，含完整離線播放器 |

## 發布與嵌入方式

- Blogger 本文使用 HTTPS `iframe` 連到 GitHub Pages 靜態頁面，避免將含 JavaScript 的完整 HTML 直接貼進 Blogger Markdown／編輯器；`sandbox="allow-scripts allow-downloads"` 限制嵌入權限。
- 預期獨立試玩網址為 `https://jerrychien1031.github.io/rhyzarca-blog/assets/articles/2026-11-13-two-ai-projects-human-judgment/<filename>.html`。
- **Draft PR 只驗證來源與靜態檔案，GitHub Pages 只有進入正式部署後才能驗證實際公開 URL。** Blogger 是否保留 iframe、是否允許嵌入、瀏覽器是否正常執行仍需以正式網站手機與桌面操作確認；不能以 Markdown 轉譯 PASS 代替。
- 若 GitHub Pages URL 不可用，請以 GitHub 原始碼頁下載離線檔，不要把 Raw GitHub 文字服務 URL 當可直接執行的互動頁。
- 若未來更新作品，先保留原始檔的雜湊與原始版本；任何修改 CSP、JavaScript、劇情資料、個人設定都應另建版本並重新測試，不可直接覆蓋原作而宣稱位元組一致。
- 本次作品輸出屬提供的創作與合成樣張，不等同目前正式版 Life World 所有功能、作品或結局都已完成雲端驗收。

## 本文圖像資產

文章封面及報告重繪圖存放於既有的 `assets/images/posts/` 標準位置，以同樣文章 stem 加 `_1.svg` 至 `_4.svg` 命名，符合既有 Blog 圖片契約。InvoiceGuard 部分僅使用**報告比較與來源查核示意**，不展示真實或合成發票照片。
