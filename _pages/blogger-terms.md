---
blogger_page_id: '5316376232111127141'
blogger_page_url: https://blog.rhyzarca.com/p/blogger-terms.html
description: 自用 Blogger 同步工具的適用範圍、授權與公開發布責任、部分成功的處理方式，以及停止使用的方法。
page_key: blogger-terms
title: Rhyzarca Blogger 同步工具｜使用條款
---

# Rhyzarca Blogger 同步工具使用條款

生效日期：2026-10-22。最後更新：2026-10-22。

## 工具與適用對象

Rhyzarca Blogger 同步工具由 Jerry Chien 操作，用於把個人 GitHub Repository 的 Markdown 文章與固定頁面同步到本人有權管理的 Blogger。目前工具僅供操作者本人使用，沒有對外開放註冊、代管其他人的網誌，或提供付費發布服務。

本條款僅適用於此同步工具，不涵蓋其他 Rhyzarca 網站或 AI 助理。閱讀公開 Blog 不需要授予本工具 Google 帳戶權限。功能及資料處理方式分別見[工具介紹](https://blog.rhyzarca.com/p/blogger-tool.html)與[隱私權政策](https://blog.rhyzarca.com/p/blogger-privacy.html)。

## 授權與內容責任

操作者只能使用自己有權管理的 Google 帳戶、Blogger 網誌及 Repository，並確認文字、圖片與其他素材具有適當的發布權限。授權 Google 存取權不代表 Google 已審核文章、保證工具安全，或認可其中的觀點。

工具目前使用具有 Blogger 管理能力的 OAuth 範圍，能依來源 Markdown 建立或更新內容。操作者應保護授權檔及 GitHub Secrets，並控制能變更 Repository 或啟動 Workflow 的權限。不要透過 Issue、Commit、郵件或文章公開 Token、授權碼及其他憑證。

## 發布與更新的效果

目前符合條件的 `main` 分支變更可能觸發 GitHub Actions 同步，手動執行同步也會呼叫 Blogger API。同步程式會處理其掃描範圍內的文章與固定頁面，因此不能把一次執行理解成只會發布某一篇指定文章。

沒有 Blogger 文章身分的來源檔可能建立新文章；已有對應身分的來源則可能覆寫既有內容。固定頁面的建立與更新也會影響公開頁面。操作者應在啟動同步前審閱內容及變更範圍；需要人工核准的候選稿，應留在同步程式不會掃描的位置。

## 失敗、重試與可用性

Google 授權、API 配額、網路或 GitHub Actions 都可能使操作失敗或延遲。OAuth 的 Production 設定不保證 Token 永久有效；操作者撤銷授權後，工具也可能需要重新取得授權才能使用。

同步由多次獨立請求構成，不具備整批交易或自動回復機制。部分文章成功、其他文章失敗的情況可能發生；執行結果顯示失敗，也不代表先前的成功操作已經撤銷。如果 Blogger 已接受請求但回應遺失，直接重試還可能重複建立內容。操作者應先核對 Blogger 實際狀態、保存的文章或頁面身分，以及失敗紀錄，再決定重試或手動處理。

工具目前沒有提供持續可用、即時同步、自動備份復原或刪除所有副本的服務承諾。需要復原文章時，應依來源版本紀錄與 Blogger 的實際狀態進行個別處理。

## 停止使用與功能變更

操作者可以停用同步 Workflow、撤銷 Google 授權，並移除不再使用的本機憑證與 GitHub Secret。這些動作不會自動刪除已發布的文章、固定頁面、公開 Repository 版本或 CDN 快取。

若未來要提供其他使用者連結帳戶、變更授權範圍或加入新的資料用途，應先重新確認使用條款、隱私權政策、同意流程與存取限制，再開放相關功能。

Google、Blogger、GitHub 及其他被使用的服務仍適用各自的條款與政策。本工具的文件不會取代這些服務的要求，也不代表取得它們的背書。

## 聯絡方式

操作者：Jerry Chien。問題或更正需求請寄至 [jerrychien1031@gmail.com](mailto:jerrychien1031@gmail.com)。來信請提供必要的問題描述，不要附上 Token、Google 密碼或授權碼。