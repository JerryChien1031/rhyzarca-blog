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
| **`insights`** | 心得記錄 | 探索 Sense-making、人機協作本質、主觀貝氏認知與價值觀建模。 |
| **`architecture`** | 實作日誌 | Rhyzarca 核心引擎、語義版本控制、確定性驗證與 CLI 工具開發。 |
| **`embodied`** | 生活體驗 | 記錄山林徒步、生理節律與真實環境感知——提醒我們智能始終根植於有邊界的肉身。 |
| **`speculations`** | 科學猜想 | 探討形式化驗證、本體論結構、意識邊界與未來的技術假說。 |

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

新增文章請於 `_posts/` 目錄下建立檔案，檔名格式遵循 `YYYY-MM-DD-title.md`。

文章結構範本如下：

```markdown
---
layout: post
title: "文章標題：核心主張與副標"
date: YYYY-MM-DD HH:MM:SS +0800
categories: [insights, architecture]
tags: [AGI, Epistemic-Ledger, Philosophy]
description: "120 字以內之文章精要（TL;DR），利於 AEO 與社群預覽。"
---

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
