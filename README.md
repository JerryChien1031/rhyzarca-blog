# Rhyzarca Blog (`blog.rhyzarca.com`)[cite: 1]

> **The Sovereign Epistemic State Layer in the AGI Era**  
> 當 AGI 無所不能，決策與引導的根本價值不在於模型多聰明，而在於對使用者**環境約束**、**價值觀取捨**與**歷時性認知軌跡**的主權對齊。

---

## 🧭 專案願景與核心哲學 (Core Philosophy)

在多模型並存、算力邊際成本趨近於零的時代，任何頂級 AGI 都能在幾秒內給出邏輯嚴密的「統計平均最優解」。然而，忽視具體個人現實的通用建議，往往只是精緻的幻覺。

本部落格是 **Rhyzarca Sovereign Writing OS** 的官方思想實驗場與公開演化日誌。我們主張：

* **自持圖書館 vs. 換代的管家**：各類頂級 LLM 與 AI Agent 只是來來去去的「管家」；Rhyzarca 是一座由個人自持、跨模型調閱的「主權狀態層」。
* **個人化決策的三大支柱**：
  1. **環境約束（Context & Reality）**：物理邊界、生理精力極限、財務跑道與時間水位。
  2. **價值觀與取捨（Values & Trade-offs）**：在目標衝突時，你願意義無反顧放棄什麼。
  3. **歷時性認知軌跡（Cognitive Trajectory）**：基於特定時點（Point-in-time）誠實鑄造的判斷與修正史。
* **互補品經濟學**：推論算力越廉價，記錄真實靈魂軌跡的「個人認知帳本」就越稀缺且無可取代。

---

## 📚 內容軸線 (Taxonomy & Focus Areas)

本站所有文章均嚴格圍繞四條交織的思維軸線展開：

| 類別 (Category) | 核心範疇 | 說明與探討方向 |
| :--- | :--- | :--- |
| **`insights`** | 心得記錄 | 對知識、工具、工作與人機協作的觀察、評析和反思；分享觀點如何形成與改變。 |
| **`practice`** | 實作探索 | 從構想、試驗到成果，分享把問題做出解法的過程。涵蓋可行性研究、設計製作、測試除錯、維護與實作回顧；不限個人或團隊，也不以完成或成功為門檻。 |
| **`embodied`** | 生活體驗 | 以親身經歷為主，記錄生活、活動、旅行、學習、工作現場、環境與身體感受。 |
| **`speculations`** | 科學思辨 | 以問題、假說與思想實驗探索科學、技術、歷史與未來社會的可能性，釐清前提、推論與待驗證之處。 |

---

## 🏛️ 認識論公約 (Epistemic Protocol)

本站實踐 Rhyzarca 的 **「永不刪除，只加註記（Append-Only）」** 核心原則：

1. **真實記錄時點狀態**：每篇核心論述均附帶當時的信念強度（Conviction）與前提假設（Dependencies）。
2. **公開修正，不抹煞歷史**：若未來的認知改觀，一律在原文下方追加**修訂分錄（Epistemic Revision Entry）**，保留思維演進的完整軌跡。

---

## 🛠️ 本地開發與建置 (Local Development)

本專案基於 Jekyll 靜態網站產生器建置，並透過 GitHub Pages 自動部署。

### 1. 環境需求
* Ruby (>= 3.1.0)
* Bundler
* Git

### 2. 本地啟動步驟
```bash
# 複製儲存庫
git clone [https://github.com/jerrychien1031/rhyzarca-blog.git](https://github.com/jerrychien1031/rhyzarca-blog.git)
cd rhyzarca-blog

# 安裝相依套件
bundle install

# 啟動本地開發伺服器
bundle exec jekyll serve --livereload
```
瀏覽器開啟 `http://localhost:4000` 即可預覽。

---

## ✍️ 文章發布規範 (Writing Guidelines)

**新文章必讀：[Blog 文章結構與圖片契約](docs/blog-article-contract.md)**。2026-11-06 起的新文章必須包含標準 Front Matter（含 `image` 首圖路徑），在正文最前面放置實際存在的首圖與圖說，再接 TL;DR。圖片的**位置、來源與命名固定；風格不固定**。長文另建議在靠近結語處加入收束圖。Draft **不可編造 `blogger_post_id`**；正式發布成功後，既有 Blogger 同步流程才會回寫真實文章 ID。獨立 PR 的 GitHub Actions 檢查缺漏，不能取代最終顯示與發布驗收。

新增文章請於 `_posts/` 目錄下建立檔案，檔名格式遵循 `YYYY-MM-DD-title.md`。

文章分類依正文的**主要目的**決定，完整定義與逐篇對照見 [分類範圍與判斷規則](docs/blog-taxonomy.md)。`practice` 對外顯示「實作探索」：具體目標的可行性討論、設計、個人小品、團隊合作、單元測試、除錯、教學及未完成或失敗的嘗試皆可收錄；不要求已有成品。心得與觀點保留 `insights`。不得只因提到 AI、架構或程式就歸為實作，也不因第一人稱或尚在規劃而排除。先定主要入口，另一分類須有完整內容支撐；不用為合作方式、完成階段或專案名稱增加主分類。實作探索的正式分類代碼為 `practice`；`architecture`、`Architecture`、`build-log` 僅保留為舊網址別名，不另開第五類。

**重要：** GitHub 的檔名不會決定 Blogger 公開永久連結。新文章必須在 Front Matter 指定 `blogger_permalink_slug`；同步程式先以此英文名稱建立 Blogger 文章，再更新正式中文標題，並驗證真實 URL。已發布文章的舊網址不可靠重命名 Markdown 修復；需要明確授權、保存舊 ID 的遷移流程。

文章結構範本如下：

```markdown
---
layout: post
title: "文章標題：核心主張與副標"
date: YYYY-MM-DD HH:MM:SS +0800
categories: [insights]
tags: [AGI, Epistemic-Ledger, Philosophy]
description: "120 字以內之文章精要（TL;DR），利於 AEO 與社群預覽。"
blogger_permalink_slug: human-ai-mutual-growth
image: /assets/images/posts/YYYY-MM-DD-title_1.png
---

![根據文章主題撰寫的首圖替代文字](/assets/images/posts/YYYY-MM-DD-title_1.png)

*圖一：依文章主題設計的封面圖說。*

> **TL;DR**  
> 本文核心結論與摘要（BLUF 原則，先給出結論）。

---

### 一、 核心問題與背景

正文內容...

---

### 🏛️ Epistemic Ledger Entry: #序號
* **Timestamp**: `YYYY-MM-DDTHH:MM:SS+08:00`
* **Claim**: 核心論斷描述
* **Epistemic State**: `High Conviction` | `Tentative Hypothesis` | `Under Revision`
* **Dependencies**: 支撐該論斷的關鍵理論或外部前設
```

---

## 📂 目錄結構 (Project Structure)

```text
.
├── CNAME                  # 自訂網域設定 (blog.rhyzarca.com)
├── README.md              # 專案說明與認識論宣言
├── _config.yml            # Jekyll 全域設定檔
├── _layouts/              # 頁面模板 (post.html, default.html)
├── _posts/                # 歷時性文章分錄 (Markdown)
├── assets/
│   └── css/
│       └── custom.css     # 自訂樣式表 (排版與主題優化)
├── categories.md          # 分類彙整導覽頁
└── index.html             # 部落格首頁
```

---

## 📜 授權與宣言 (License)

* **文字內容與思維分錄**：採用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 授權。
* **原始碼與架構腳本**：採用 [MIT License](LICENSE) 開源發布。
