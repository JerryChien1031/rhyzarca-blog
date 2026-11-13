---
blogger_permalink_slug: two-ai-projects-human-judgment
blogger_post_id: '4357768617267032194'
blogger_post_url: https://blog.rhyzarca.com/2026/11/two-ai-projects-human-judgment.html
categories:
- insights
date: 2026-11-13 09:00:00 +0800
description: 同一段課程尾聲，我參與手寫發票辨識與 AI 故事世界兩個專案。從期別認錯、RAG 套錯規定，到人物設定與重複扣費的反例，記錄人如何和 AI
  一起研究、修正與驗收。
image: /assets/images/posts/2026-11-13-two-ai-projects-human-judgment_1.svg
layout: post
tags:
- Human-AI-Collaboration
- InvoiceGuard-AI
- Life-World
- RAG
title: 發票不能亂猜，故事不能亂演：兩個 AI 專案教我的人機協作
---

![InvoiceGuard AI 報告比較與 Life World 互動路徑的雙專案概念封面](/assets/images/posts/2026-11-13-two-ai-projects-human-judgment_1.svg)

*圖一：以 InvoiceGuard AI 的簡報比較數據及 Life World 的互動旅程為元素重新設計的文章封面。數值限於簡報的小樣本測試，右側是作品意象，不是兩套系統的實際整合畫面。*

> **TL;DR**  
> 一個專案要讓 AI 看懂手寫發票，卻不能容許它亂猜數字；另一個讓 AI 寫故事、演角色，又不能讓它忘記人物設定，或多算一次生成費用。
>
> 我在輔導課程尾聲參與這兩個團隊專案，最有感的不是模型變得多強，而是**人如何發現它的錯、決定哪些事能交給它，以及怎麼讓修正留下證據**。本文記錄可回查的實作與失敗，也放入可以自己玩的 Life World 離線 HTML 作品。

---

### 一、課程快結束時，我碰上兩種完全不同的 AI 問題

近期參與失業補助輔導課程，在課程接近尾聲時，我同時投入兩個團隊專案。

其中一個是 **InvoiceGuard AI**。它面對的是台灣的手寫三聯式發票：字跡、欄位、金額、報價與審核紀錄，都有可能影響後面真正做事的人。採購希望少登打一次，財會卻不能因為 AI 說「已辨識」就直接核准。

另一個是 **Life World**。它從設定個人目標、記錄真實經歷出發，慢慢長出人物、關係、AI 故事與可以互動遊玩的作品。這裡反而希望模型有想像力：同樣一句話，急性子與謹慎的人應有不同反應；讀者選了不同的路，故事也應走向不同的結果。

一邊不准 AI 亂猜，一邊希望它能好好創作。乍看之下是相反的要求，實際做下去，卻一再遇到同一個問題：**看起來完成了，是否就代表做對了？**

我在兩個專案中的工作涉及全端整合、環境與部署、資料或模組契約、技術決策，以及部分功能的開發和驗收。這是團隊成果，不是我一個人寫出所有程式。Claude、Codex 等 AI 工具參與了實作和複查；團隊其他成員也分別投入前端、API、RAG、產品方向與美術。文章只根據有紀錄的事件談分工，不把整個團隊的工作都算到自己頭上。

---

### 二、第一次體會：JSON 長得很正確，數字還是可以錯

最先讓我印象深刻的，不是複雜的系統架構，而是一張空白的三聯式發票樣張。

2026 年 10 月 28 日，團隊以 Google Document AI 進行 OCR（光學字元辨識），再讓 Groq 上的模型整理輸出。同一份輸入第一次把「一〇八年九、十月份」回成 `202109`，隔天再次測試，又回成 `201909`。

兩次都是合法 JSON；年份與期別卻不一致。依後續系統採用的「雙月期末月」紀錄方式，這個樣張對應的值應為 `201910`。早期紀錄當時另有不同的對照寫法，不能把它和後來定義好的欄位規則混成一回事。

這個例子讓我重新理解「AI 已經辨識成功」究竟是什麼意思。

**能輸出規定格式，只證明它知道怎麼交卷；不代表答案正確。**

團隊後來的作法，是把工作拆開：讓模型先辨識票面文字，年、月、金額及期別的換算交由程式處理；缺少依據或出現衝突時，保留人工確認。11 月 5 日之後，API 主要發票擷取路徑又改為 Gemini 直接讀取影像，不能再把早期 Document AI → Groq 實驗當成最新實作。

不論模型怎麼換，有一件事沒變：採購人員必須能核對 AI 原始值、修正值，財會也必須有自己的審核權限。這些不是多做幾個按鈕，而是讓錯誤不會一路進入正式流程。

[早期發票辨識與期別反例](https://github.com/Donato517/InvoiceGuard-AI-API/blob/69c74ce08c53960c5fa5533d7c2978aa80f54f31/docs/TEST_REPORT.md#L928) · [現行期別換算規則](https://github.com/Donato517/InvoiceGuard-AI-API/blob/69c74ce08c53960c5fa5533d7c2978aa80f54f31/app/utils/invoice_format.py#L133) · [切換 Gemini 影像路徑的提交](https://github.com/Donato517/InvoiceGuard-AI-API/commit/61d98fa)

---

### 三、從簡報上的 94.3%，學會問「到底測了什麼？」

報告裡有一張很清楚的比較圖：原始影像的 Zero-shot（不提供示例）辨識，欄位命中率為 74.3%；經過裁切校正、搭配 Few-shot（少量示例）等不同組合後，最高一組達到 94.3%。

如果只看最後那個數字，很容易覺得「準確率已經接近 95%」。但那張簡報底下還有一句更重要的提醒：**這組比較來自五張發票、共 70 個欄位。**

![InvoiceGuard AI 簡報中四組欄位命中率的比較圖表重繪](/assets/images/posts/2026-11-13-two-ai-projects-human-judgment_2.svg)

*圖二：依 InvoiceGuard AI 專案簡報第 13 頁重繪的四組比較。74.3%、88.6%、92.9%、94.3% 各有不同輸入條件；樣本僅五張發票、70 個欄位，不能外推為正式系統整體辨識率。*

而且，這裡不只改了一件事：影像裁切校正與 Few-shot 條件也不同，不能把提高的 20 個百分點全部說成某一種技巧的功勞。

專案的另一份測試資料有 100 筆黃金集索引，但其中只有三張有人工逐欄標註。**100 筆索引和 100 張都經過人工標準答案核對，是完全不同的證據。**

這些數字提醒我：做 AI 系統時，除了問模型有多厲害，更要問測試的分母是什麼、誰提供正確答案、條件改了幾項，以及錯誤能否被攔下。

我後來愈來愈在意的不是「報告寫了多少 passed」，而是這些通過結果，究竟可以支持哪一句話。

[專案黃金集與標註狀態](https://github.com/Donato517/InvoiceGuard-AI-API/blob/69c74ce08c53960c5fa5533d7c2978aa80f54f31/docs/GOLDEN_SET.md#L5)

---

### 四、明明已經換成 B，畫面還留著 A；有引用的回答，也可能用錯規則

另一段開發經歷更接近一般使用者的日常。

採購人員上傳 A 發票，接著改選 B。B 的預覽明明已經顯示在畫面上，A 之前那個慢半拍的回覆卻突然抵達，將 A 的辨識欄位蓋到 B 上面。

這不是模型認字準不準的問題，而是兩個非同步工作碰在一起。**畫面上的檔案和旁邊的欄位，如果不是同一張發票，再漂亮的辨識結果也沒有用。**

第一次修正用選檔版本號擋掉舊資料。使用者接著要求 Codex 從不同情境複查，卻又發現：舊的登入轉址可能先發生、手機重拍前舊工作尚未作廢、延遲的讀檔也可能蓋過後選的檔案。Claude 再依這些反例修補，把「現在仍然是同一份檔案嗎？」放到真正改動畫面之前檢查。

這是我喜歡的協作方式：**不是叫兩個 AI 都說一次沒問題，而是讓其中一個故意找出另一個可能沒想到的情境。**

[前台換檔競態與跨 Agent 複查](https://github.com/Donato517/InvoiceGuard-AI/blob/d8874e5c14495da2e773a26c7cf5323de4a20ddf/docs/REVIEW_FIX_LOG.md#L370)

接著，輪到企業知識庫問答出問題。

RAG（檢索增強生成）會先從公司授權的法規、流程文件找資料，再讓模型整理回答。報告裡甚至有「點擊引用編號，回到來源原文」的操作畫面。但一次真正的操作題測試中，AI 把「發票開錯」的處理方式，套用到「發票遺失」上。

它有引用，也不代表用的是正確的規則。對不熟悉規定的新進同仁而言，這種錯誤可能比直接說「我不知道」更危險。

![依 InvoiceGuard AI RAG 來源追溯報告重繪的答題與原文查核示意](/assets/images/posts/2026-11-13-two-ai-projects-human-judgment_3.svg)

*圖三：依專案簡報的「RAG 回答點開來源」畫面，以及實際操作題失敗紀錄重繪。這是辨識「有引用」與「引用適用」的差別，不是任何發票法規的操作指引。*

團隊重新整理了 OCR 辨識出的條文項次與索引，讓問答分兩輪完成：先產生答案草稿，再比對來源與適用情境；缺乏依據時應明確說資料不足，不必硬給結論。

這裡我看到的不是單純的模型優化，而是產品責任：**真正需要幫助的人，不能因為 AI 很有自信，就被帶往錯誤的下一步。**

[實際 RAG 誤答與來源修正紀錄](https://github.com/Donato517/InvoiceGuard-AI-ADMIN/blob/f67b5a6066f2c4d27b265a4f638b52ad6baefb83/docs/TEST_REPORT.md#L1382) · [新手問答的開發與限制](https://github.com/Donato517/InvoiceGuard-AI-ADMIN/blob/f67b5a6066f2c4d27b265a4f638b52ad6baefb83/docs/RAG_DEVELOPMENT.md#L218)

---

### 五、換到 Life World：故事能寫出來，不代表 AI 真的認識人物

做完這些需要嚴格判斷的功能，我又回到另一個團隊專案——Life World。

最早的產品想法很生活化：設定一個目標、記下每天真正做過的事，再由使用者確認這次努力要算多少貢獻。後來人物和關係進入系統，故事開始不只是描述個人生活，還能把不同人物放進同一個虛構情境裡。

但我們很快發現一個容易被忽略的問題：畫面上已經選了某個人物，**不代表生成模型真的收到了那個人物的正式設定**。

早期創作入口主要依賴舊角色卡，和後來整合的正式人物資料之間還有落差。這個問題在首篇作品生成之前的唯讀盤點中就被找出來，當時的結論是 `NOT READY`。

接著團隊處理人物的正式來源、版本鎖定及輸入範圍。例如：作品一開始就選定某個人物設定版本，後來這個人物即使又修改了設定，也不能讓正在生成的作品突然「變了一個人」。

另一條界線更值得注意：**真人的經歷、使用者對人的主觀印象、模型推論和虛構情節，不能混成同一種事實。** AI 可以讓虛構人物演出，但不代表有權把真人的私人設定交給其他角色，或讓作品裡編造的事件反過來變成真實經歷紀錄。

[人物設定接入的實際提交](https://github.com/asixtw/life-world/commit/5cb5015a174ad821dea17abfc36236f4e33fd1b4) · [人物來源、版本與驗收紀錄](https://github.com/asixtw/life-world/blob/725e0e714c4bac847fea054bd63459ccfd69d4e7/docs/ACCEPTANCE.md#L218)

---

### 六、故事已經寫完，我卻覺得它不好看

Life World 後來可以讓模型分段續寫、保存章節，再匯出為單一 HTML。程式測試可以確認欄位、版本、格式沒有壞；可是第一次認真讀完作品，仍會發現人物說話太像、某些情節太快解決，甚至有角色提前回應還沒發生的事。

這些問題不是多跑幾個單元測試就能直接回答。**文章能產生，和讀者會不會想讀下去，是兩件不同的事。**

於是開始調整提示：讓角色以自己的說話節奏、動作和價值取捨做反應；把已發生的事帶進後續章節，避免改寫前文；我讀過樣本後，也提出以觀眾熟悉的名場面為藍本，讓開場先有衝突、讓人物留下一個值得追看的問題。接下來又把這些做法改寫成適用不同題材的共通規則，而不是只為某一篇故事寫死台詞。

這也是團隊協作中我很在意的一件事：Claude、Codex 可以協助追程式、生成與測試；**但「這個人物不像他自己」「這故事沒有讓我想看下一段」仍需要有人親自讀、指出差異。**

有些改善在特定樣本上看得到，有些跨章時間矛盾仍存在。文章不應用「品質顯著提升」掩蓋這些還沒解決的問題。

[提示詞 v5～v8 的修正與人工閱讀紀錄](https://github.com/asixtw/life-world/blob/725e0e714c4bac847fea054bd63459ccfd69d4e7/docs/ACCEPTANCE.md#L293)

#### 不只閱讀，也能真的做一次選擇

從文字作品往前一步，Life World 也做出了互動閱讀、行程選擇與捲動劇情的離線 HTML。這些不是文章裡的概念圖，而是**可以在瀏覽器實際操作的獨立檔案**；所有展示檔都放在本篇專屬的 GitHub 資產資料夾，沒有要求讀者登入產品服務。

先試《海角小鎮一日遊》。從車站出發，時間有限，同行者對每個選擇的反應不同，途中還能回頭看自己走過的路。

<iframe title="Life World《海角小鎮一日遊》離線互動遊戲示範" src="https://jerrychien1031.github.io/rhyzarca-blog/assets/articles/2026-11-13-two-ai-projects-human-judgment/sea-town-route.html" width="100%" height="610" loading="lazy" referrerpolicy="no-referrer" sandbox="allow-scripts allow-downloads" style="border:1px solid #d2ddd7;border-radius:14px;max-width:100%;background:#fbfaf6;"></iframe>

*互動作品一：《海角小鎮一日遊》。這是提供的離線 HTML 作品，與文中合成版「海線小鎮一日行」操作截圖、受控真實模型試跑並非同一份驗收樣本。若內嵌視窗無法操作，可使用下方獨立連結。*

[獨立開啟行程互動遊戲](https://jerrychien1031.github.io/rhyzarca-blog/assets/articles/2026-11-13-two-ai-projects-human-judgment/sea-town-route.html) · [查看 HTML 原始檔並下載離線使用](https://github.com/JerryChien1031/rhyzarca-blog/blob/main/assets/articles/2026-11-13-two-ai-projects-human-judgment/sea-town-route.html)

另一件作品是《現代鴻門宴：會館裡的最後合約》。它改寫古典情節的角色衝突，讀者可以逐段揭開台詞，切換人物視角，讀完後再看看角色真正藏著什麼。

<iframe title="Life World《現代鴻門宴：會館裡的最後合約》互動閱讀示範" src="https://jerrychien1031.github.io/rhyzarca-blog/assets/articles/2026-11-13-two-ai-projects-human-judgment/modern-hongmen-banquet.html" width="100%" height="570" loading="lazy" referrerpolicy="no-referrer" sandbox="allow-scripts allow-downloads" style="border:1px solid #d2ddd7;border-radius:14px;max-width:100%;background:#fbfaf6;"></iframe>

*互動作品二：《現代鴻門宴》。這份 HTML 是已提供的作品匯出檔，內容與人物均為虛構演出，並非真人事件紀錄。*

[獨立閱讀《現代鴻門宴》](https://jerrychien1031.github.io/rhyzarca-blog/assets/articles/2026-11-13-two-ai-projects-human-judgment/modern-hongmen-banquet.html) · [查看 HTML 原始檔](https://github.com/JerryChien1031/rhyzarca-blog/blob/main/assets/articles/2026-11-13-two-ai-projects-human-judgment/modern-hongmen-banquet.html)

另外兩份同樣已納入這篇文章的展示檔案：[《空城計：巷口麵包店的最後清晨》互動版](https://jerrychien1031.github.io/rhyzarca-blog/assets/articles/2026-11-13-two-ai-projects-human-judgment/bakery-empty-fortress.html)與[《冰下之春》捲動劇情](https://jerrychien1031.github.io/rhyzarca-blog/assets/articles/2026-11-13-two-ai-projects-human-judgment/spring-under-ice-scroll.html)。它們可以獨立開啟，亦能從 GitHub 下載 HTML 離線閱讀。

這些作品讓人看得見 AI 的創作空間；但它們同時提醒我，互動功能可以測試，故事本身的好不好看仍值得持續討論。

---

### 七、按了兩次「再試一次」，為什麼可能多付一次錢？

Life World 還有一個比故事台詞更棘手的問題。

生成故事與遊戲需要呼叫模型，而模型呼叫有成本。假設同一個請求因網路斷線而重送，系統若沒有辨認出「這是剛剛那次工作」，可能又生成一次、又記一次費用。

回合制互動遊戲在一連串獨立複查中，正是遇到這種情境。

第一次發現的是：模型結果已完成結算，但作品尚未存好時，另一個請求可能讓同一角色再生成一次。接著又發現回應丟失後重送，可能直接替下一個角色開工；後來兩個請求同時抵達，也可能讓遊戲進度從 2/3 意外推到 3/3。

這些問題並不會因為「遊戲看起來能玩」就自動消失。

團隊在 SQLite 與隔離 PostgreSQL 上反覆做假模型測試，讓兩次請求在特定時間點碰撞，確認原本要復用的執行回執、作品版本與費用紀錄都沒有被改錯。第五輪在兩套資料庫各通過 23 個指定案例，離線播放器另有 26 項測試通過；同輪全套測試仍記錄 1,142 通過、7 失敗、12 錯誤、35 跳過，後面幾類和既有基線逐項對照，不能省略後直接寫成「全套都通過」。

我在這裡感受到，人類與 AI 的角色並不是「AI 寫程式，人只要按接受」。

使用者要先明確說出不可破壞的承諾，例如「同一個請求重送，不應再生成或多扣費」。Claude 可以實作修正，Codex 透過另一輪反例找出邊界，最後還要用真實執行紀錄證明結果。完成後，才由人決定能不能提交指定分支。

**AI 能幫忙找到許多測試情境，但哪個承諾不能被破壞，始終需要有人說清楚。**

[Life World 五輪獨立複查](https://github.com/asixtw/life-world/blob/725e0e714c4bac847fea054bd63459ccfd69d4e7/docs/INTERACTIVE_GAME_REVIEW_20261112.md#L246) · [第五輪提交與修正](https://github.com/asixtw/life-world/commit/725e0e714c4bac847fea054bd63459ccfd69d4e7)

---

### 八、不是兩份功能清單，而是兩種責任邊界

把兩個專案放在一起，我發現很多問題只是換了外表。

**表一：兩個 AI 專案裡，哪些地方看似不同，其實需要同一種判斷？**

| InvoiceGuard AI | Life World | 我學到的事 |
| --- | --- | --- |
| JSON 格式對，發票期別仍錯 | 選了人物，模型卻不一定拿到對的設定 | 有資料，不代表資料用對 |
| RAG 附上來源，卻可能套錯規定 | 劇情完整，仍可能前後矛盾、人物失去個性 | 有產出，不代表符合使用目的 |
| A 的延遲辨識不能覆蓋 B | 同一個生成請求不能多走一輪 | 中斷與重送，也要維持一致 |
| 採購確認、財會核准 | 作者決定人物界線、採納故事 | AI 可以提出草稿，重要選擇仍需有人把關 |

我也更能理解團隊合作的價值。有人知道第一線使用者真正會卡在哪裡，有人關心人物設定和遊戲節奏，也有人從後端、資料庫與部署角度找出另一種錯誤。Claude 和 Codex 的分工不必固定成誰永遠主寫、誰永遠審查；重點是每一次交接，都要說清楚要做什麼、用什麼版本、哪些不能碰，以及回來拿什麼證明。

在 InvoiceGuard AI，部署環境與機密隔離讓不同成員不必接觸正式金鑰也能開發；前台透過 API 存取資料，管理端和 API 各有明確責任。在 Life World，正式環境、E2E 與功能分支也必須分開，否則一項測試成功，很容易被誤會成所有人已經能用到那個版本。

這些工程決策看起來不如 AI 的畫面炫目，卻決定一個團隊能不能安心地繼續開發。

尤其不能把所有漂亮的測試數字都當成產品完成率：**規劃文件、Git 合併、隔離測試、真實模型呼叫、正式部署，是不同層次的證據。** 我們兩個專案都還有待補的完整流程、不同角色、裝置相容性與長期品質評估，不能因為 Demo 已能操作就宣稱正式營運已驗證。

---

### 九、課程結束前，我真正帶走的是什麼？

如果只用技術清單回顧這段時間，大概會列出 FastAPI、PostgreSQL、Document AI、Gemini、RAG、Cloud Run、Vercel、GitHub Actions、Claude 和 Codex。

但這些名字很快就會換。模型、工具、部署服務，一年後或許有更好的選擇。

我反而想記住幾個比較不容易過時的問題：

當 AI 認出了字，誰知道那是不是正確的發票期別？當它找到法條，誰確認它沒有套錯情境？當它替角色寫完故事，誰能判斷人物是否仍是原來的樣子？當一次生成發生重送，誰來確認費用、進度和結果沒有重複計算？

這些問題沒有一個能只靠「把 Prompt 寫得更長」解決。

AI 幫我研究、產生程式、找出可能的反例；我和團隊成員帶回真實的工作情境、使用回饋、取捨與驗收條件。當答案不對，重新查來源；當設計不適合，重新選方向；當測試失敗，留下可以再跑一次的紀錄。

這讓我想起 Rhyzarca 之前寫過的[〈從未知開始：當 AI 自行組織專業、擴充工具，與人類共同長出需求〉](https://blog.rhyzarca.com/2026/11/human-ai-mutual-growth.html)。那篇文章從模糊需求談人機協作；而這次，兩個團隊專案給了我更具體的例子：人的參與並不是多餘的審批，而是讓 AI 的探索不會脫離現實的關鍵。

![InvoiceGuard AI 與 Life World 在真實資料與虛構創作中各自需要的人類確認界線](/assets/images/posts/2026-11-13-two-ai-projects-human-judgment_4.svg)

*圖四：兩個專案走向不同：發票資訊必須可核對，虛構故事可以盡情發揮，但仍須遵守人物設定、已發生的情節與生成成本等規則。這是本文觀點整理的概念圖。*

我也逐漸明白，Rhyzarca 一再談的「保留知識與決策理由」，不是為了替 AI 收集更多漂亮筆記，而是讓下次換了模型、換了團隊成員，我們仍能找回：**當時為什麼這樣做？哪些試過卻失敗？什麼結果真的驗過？**

這也呼應了[〈數位巴別塔：當 AI 成為文明唯一的翻譯器〉](https://blog.rhyzarca.com/2026/09/agi-rhyzarca_0615099013.html)裡更深一層的擔憂：資料留住了，如果沒有人能回頭理解那些決定，知識仍可能一點一點失去意義。

這兩個作品當然還不是終點。我也沒有因為做了兩個 AI 專案，就突然掌握所有問題的答案。

不過，至少現在遇到新的需求時，我會更願意先問一句：

**這次，我們該讓 AI 自由探索到哪裡？又該在哪一步，停下來把事情看清楚？**

---

### 🔗 開發來源與延伸閱讀

**InvoiceGuard AI：** [早期發票辨識與測試報告](https://github.com/Donato517/InvoiceGuard-AI-API/blob/69c74ce08c53960c5fa5533d7c2978aa80f54f31/docs/TEST_REPORT.md) · [前台換檔與複查紀錄](https://github.com/Donato517/InvoiceGuard-AI/blob/d8874e5c14495da2e773a26c7cf5323de4a20ddf/docs/REVIEW_FIX_LOG.md) · [RAG 問答與來源測試](https://github.com/Donato517/InvoiceGuard-AI-ADMIN/blob/f67b5a6066f2c4d27b265a4f638b52ad6baefb83/docs/TEST_REPORT.md)

**Life World：** [人物與作品驗收紀錄](https://github.com/asixtw/life-world/blob/725e0e714c4bac847fea054bd63459ccfd69d4e7/docs/ACCEPTANCE.md) · [互動遊戲第五輪獨立複查](https://github.com/asixtw/life-world/blob/725e0e714c4bac847fea054bd63459ccfd69d4e7/docs/INTERACTIVE_GAME_REVIEW_20261112.md) · [對應功能分支提交](https://github.com/asixtw/life-world/commit/725e0e714c4bac847fea054bd63459ccfd69d4e7)

**Rhyzarca 思想脈絡：** [〈從未知開始：人機協作與雙向成長〉](https://blog.rhyzarca.com/2026/11/human-ai-mutual-growth.html) · [〈Claude Code × OpenAI Codex：共享契約與自主工程工作流〉（GitHub 原文）](https://github.com/JerryChien1031/rhyzarca-blog/blob/main/_posts/2026-10-22-claude-codex-harness-engineering-auto-workflow.md)

---

### 🏛️ Epistemic Ledger Entry: #0011（候選分錄）

- **Timestamp:** 2026-11-13T09:00:00+08:00
- **Claim:** 在 AI 參與的真實開發中，允許模型創作或擷取資訊的範圍可因業務不同而改變，但使用者仍須能區分來源、推論、操作副作用與最終驗收。人機協作的價值不只是提高產出速度，更包括辨識錯誤、界定權責，以及讓後續開發者可以重建已確認的理由。
- **Epistemic State:** 個案心得與工程觀察（Case-Based Insight）；並非普遍成效的因果證明。
- **Evidence Scope:** InvoiceGuard AI 依 2026-10-21 至 11-13 的指定 Git、PR 與測試資料；原始簡報四組 70 欄小樣本不代表正式整體辨識率。Life World 的人物、故事與重送問題依功能分支、指定本機／E2E 測試及交接紀錄；本文公開的四份 HTML 為提供的離線作品，與不同日期的真實模型試跑不得混為一件。未重跑兩案完整測試，亦未查驗目前所有正式部署與實際使用量。
- **Dependencies:** 真實授權與責任分工；版本化人物／發票資料；可重新執行的測試與回執；人工確認；跨 Agent 清晰交接；資料安全與作品公開權限。
- **Revision Trigger:** 若後續有更廣泛、獨立且具代表性的辨識黃金集，或公開作品與正式流量完成端到端驗收，應更新成效敘述；若實際部署、授權或內容來源與現有紀錄不同，應保留歷史並修訂當前結論。
- **Next Question:** 當 AI 不只協助寫程式，還能研究、安排與執行，我們要如何讓人的選擇、AI 的實作與獨立驗證形成既不妨礙創造、又能避免錯誤擴散的日常工作方式？