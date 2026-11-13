# Rhyzarca Blog｜分類範圍與判斷規則

2026-11-14 經作者確認：「系統日誌」重新定位為「實作探索」。保留四類與既有代碼，不增加第五個主分類。機器可讀對照為 `_data/blog_categories.json`。

## 四個入口
- **心得記錄（insights）**：對知識、工具、工作、社會、人機協作與個人經驗的理解、觀察、評析和反思；重點是觀點如何形成與改變。
- **實作探索（architecture）**：圍繞具體的製作、應用或改善目標，分享方案構思、可行性研究、設計製作、測試除錯，以及成果與後續改進。不限個人或團隊、軟硬體或創作流程、大型專案或小品，也不以完成或成功為門檻。
- **生活體驗（embodied）**：以親身經歷為主的生活、活動、旅行、學習、工作現場、環境與身體感受。
- **科學思辨（speculations）**：以問題、假說與思想實驗探索科學、技術、歷史或未來社會，討論前提、推論、替代解釋與待驗證之處。

## 實作探索的範圍
可行性討論、需求研究、方案比較、架構設計、團隊專案、個人小工具、學習練習、資料處理、介面或互動作品、AI 工作流程、單元與整合測試、評估實驗、除錯重構、部署維護、交接、操作教學、失敗紀錄與實作回顧，都可以收錄。每篇只談其中一個環節也成立，不要求所有文章都有程式碼或成品。

核心是「想做什麼、處理哪個問題、如何推進或驗證」。規劃尚未開始製作也能是實作探索；但只談文明可能性、引用工程術語，並不自動成為實作。

## 邊界與交集
1. 先看全文的主要目的，再看文風。第一人稱和結語反思不會把實作自動變成心得。
2. 有另一條完整內容主線時可保留次要分類，不強制所有舊文互斥，也不為增加曝光全選。
3. 團隊／個人是合作方式，規劃／原型／已部署是進度，Life World 等是專案，RAG／Agent 等是主題；它們不另立主分類。
4. 「實作探索」不宣稱驗收成功。完成程度、樣本限制、失敗與未驗證事項在正文交代。
5. 指定單一分類的作者要求優先。不得只見 MCP、AI、架構或程式就加上 architecture。
6. insights 不刪除、不改作實作的別名；embodied 暫無文章也保留其內容方向。

## 2026-11-14 既有文章審閱
下表是本次逐篇判斷，不是以標題關鍵字自動分類。保留有內容依據的重疊；未列為修改的正文與分類不擅動。

| 文章 | 原分類 | 本次分類 | 理由 |
| --- | --- | --- | --- |
| 認知總帳：為什麼 AGI 時代最稀缺的不是知識，而是認知軌跡 | Epistemology, Architecture | insights | 認知軌跡與網站理念，沒有具體製作方案。 |
| 當 AGI 無所不能，該如何提供適合你的引導與協助？—— Rhyzarca 的價值與起源 | insights, architecture | insights, architecture | 以價值觀為主，同時提出主權狀態層及帳本設計；保留觀點與方案探索的交集。 |
| 聰明 vs. 見識：當 Gemini Notebook 賦予 AI 專家資歷，選項始於認知、決策來自天賦 | insights, architecture | insights | 以認知、見識與決策的觀點為主，工具是論述案例。 |
| 視角差異與社會債務：為什麼在演算法時代，我們需要 AGI 僕人式領導的深度同理？ | insights, architecture | insights | 以同理、視角與社會成本的觀點為主，非具體製作紀錄。 |
| 當 AGI 注定成為認知巨人，而人又逐漸脫離勞動力時，未來社會需要什麼樣的智能？ | insights, architecture | speculations, insights | 未來智能與治理制度推演，同時保留價值判斷的心得入口。 |
| 神話從未架空：技術斷層、唯讀協議與「小孩開大車」的遠古工程思想實驗 | insights, epistemology | speculations, insights | 歷史假說與思想實驗，並反思認知方法；Epistemology 主題標籤仍保留。 |
| 從資訊套利到認知共善：當 AGI 接管生產力，人該如何活出不可替代的價值？ | insights, architecture | speculations, insights | 未來文明及人類價值推演，不把社會藍圖當成工程成果。 |
| BCI ╳ AGI 共治共產社會：資訊落差逐漸失效；資訊公開崛起，新的社會型態會是什麼樣的體制？ | insights, architecture | speculations | BCI 與 AGI 社會體制的假設推演，以科學思辨為主要入口。 |
| 當 AGI 成為文明的公共大腦：Rhyzarca 為何能夠存在？ | insights, architecture | insights, architecture | 包含具體四層系統方案；實作探索涵蓋規劃設計，不要求已完成產品。 |
| 數位巴別塔：當 AGI 成為文明唯一的翻譯器，Rhyzarca 如何保存人類的可理解性？ | insights, architecture | insights, architecture | 認知連續性觀點與保存、重建的架構方案並存；保留有內容依據的交集。 |
| Claude Code × OpenAI Codex：從共享契約到可恢復的自主工程工作流 | architecture | architecture | 工程設計、跨平台協作、故障恢復與限定實測。 |
| 從未知開始：當 AI 自行組織專業、擴充工具，與人類共同長出需求 | insights | insights | 人機協作方法與觀點，教學情境不是本文主體的產品實作。 |
| 從行政痛點到互動世界：當 AI 的想像力遇上真實需求 | insights | architecture | 兩個團隊專案從需求、研究、試錯到成果；屬實作探索。 |

## 相容性與發布
`architecture` 是歷史技術代碼，公開名稱為「實作探索」，不改成新的 slug。`build-log`／`Architecture`、`life-and-trails` 等舊入口保留別名，不新增分類。`Epistemology`／`epistemology` 原分類歸入經審閱的正式入口；原有主題 tags 不刪除。

本次只改八篇文章的 categories；Blogger ID、標題、日期、slug、tags、正文、圖檔與作品連結不變。因 Jekyll 原設定把 categories 放進文章 URL，從實際變更前建置取得既有 URL，再以每篇 permalink 固定原路徑，避免舊連結失效。Blogger 更新既有 Post，不建立新文章。

GitHub、Blogger 導覽、404 分類入口、標籤文字及分類說明同步使用四類定義。分類頁由 `_data/blog_categories.json` 產生；Blogger 腳本內的對照由測試比對，防止兩邊名稱再分歧。原始發文 Workflow 的同步範圍不變。
