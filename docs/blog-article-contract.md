# Rhyzarca Blog｜文章結構與圖片契約

本文件是自 **2026-11-06 起新增文章**的結構規範。它固定「必要欄位與圖片位置」，**不固定文風、配色或美術類型**；舊文章不溯及既往。Commit／Push／Blogger 發布及所有權仍以根目錄 AGENTS.md、docs/codex-workflow.md 為準。

## 1. Blog ID、文章 ID、圖片不是同一件事

| 名稱 | 含義 | 何時寫入 |
| --- | --- | --- |
| BLOGGER_BLOG_ID | Blogger 整個網站的 ID，由既有同步 Workflow 的環境變數取得 | **不寫入文章**，不從其他文章複製 |
| blogger_post_id | 單篇文章的 Blogger ID；同步腳本據此更新，缺少則可能建立新文章 | **首次正式發布成功後**才從 Blogger API 回傳並自動寫回；草稿不得填假值、空值或佔位符 |
| image | 該文章的首圖本地路徑 | 新稿**必須提供**，且檔案真的存在、與正文第一張圖相同 |

實際的 scripts/sync_to_blogger.py 在首次成功發布後回寫 blogger_post_id。不得為了「欄位整齊」提前捏造 ID；已發布文章不能移除既有真實 ID，避免重新建立造成重複文章。Front Matter 的 image 用於文章來源契約，**不代表既有 Blogger 同步程式會用這個欄位設定 Blogger 特色圖片**。

## 2. 新文章最上方標準範本

未發布草稿（請以真實內容與已存在圖片取代範例）：

~~~yaml
---
layout: post
title: "從未知開始：文章的正式標題"
date: 2026-11-06 09:00:00 +0800
categories:
  - insights
  - architecture
tags:
  - Human-AI-Collaboration
  - MCP
description: "說明本文問題、核心觀點與讀者收穫的精簡摘要。"
image: /assets/images/posts/2026-11-06-example-title_1.png
---
~~~

**只有正式發布成功後**，才可能由同步器補入例如 blogger_post_id: '1234567890123456789' 的真實數字（此為示意，不可直接使用）。欄位可由 YAML 序列化程式重排，不要求固定順序；核對的是名稱、型別與值是否有效。

固定必填：layout: post；非空 title、date（含 +0800，日期與檔名前十碼一致）、categories、tags、description、image。摘要建議 120 字內。分類按文章主題設定，不強制所有文章同分類。新草稿不得有未經實際發佈的 blogger_post_id。

## 3. 位置固定，風格自由

現有正式長文的主要格式是：**Front Matter → 首圖 → 圖說 → TL;DR → 分隔線 → 正文**。

~~~markdown
![有意義的繁體中文圖片替代文字](/assets/images/posts/2026-11-06-example-title_1.png)

*圖一：封面圖所表達的主題；概念示意不冒充實測或官方架構。*

> **TL;DR**
> 本文最重要的結論與價值。

---

### 一、文章第一章
~~~

- 首圖一定是正文第一個內容元素；有非空 Alt Text、緊接的圖說；Front Matter 的 image 與此圖路徑逐字相同。
- 圖片存放於 assets/images/posts/，新文章使用與 Markdown 檔名相同的 YYYY-MM-DD-slug 前綴，加 _1（首圖）、_2、_3 等編號。可用 JPG、PNG、WebP，或安全且不含外部腳本的原創 SVG。**不可引用尚未存在的圖片。**
- 長文沿用既有多數文章的兩處敘事位置：**開頭封面**與**接近結語的收束圖**。技術文章可以在中間插入任意必要的架構圖、實測圖；不為了湊圖數添加無意義圖片。每一張圖均要 Alt Text 與圖說。
- **美術風格由 AI 依文章自由決定**：寫實、電影感、抽象、科幻、資訊圖、極簡皆可；不強制黑金、配色、構圖或固定模板。封面建議 16:9、1200×675 以上，並兼顧大小、對比與手機可讀性。
- 已有有效圖片優先沿用；格式修正不代表授權重製。新圖須有使用權並符合文章主題。沒有產圖能力時，保留 Draft 並明示缺口，不能以無效路徑充數。
- 既有 scripts/markdown_parser.py 會將 /assets/images/ 轉成 jsDelivr CDN 網址；上傳前須檢查原檔存在、實際 Markdown/Blogger HTML 可正確顯示。SVG 更需額外核對 CDN MIME 與正式平台顯示，不能只憑文字檔存在就宣稱驗證成功。

## 4. 兩道驗收：機器檢查與內容審查

新增 scripts/check_blog_article_contract.py 與 .github/workflows/blog-article-contract.yml，針對新日期文章的 PR 做**自動檢查**：Front Matter、圖片 metadata、首圖位置／圖說／Alt Text、文件存在、命名、封面比例、TL;DR、長文收束圖等。

此檢查不決定文章深度、思想風格或視覺美感；它也不等同 Blogger 真實發布。正式轉換與手機、桌面預覽依 docs/codex-workflow.md，且應使用既有 parse_and_convert()；編輯、Commit、Push、合併及正式 Blogger 同步需要分別核對授權。

## 5. 未來 AI Agent 的標準工作順序

1. 先讀 AGENTS.md、docs/codex-workflow.md、README.md **與本契約**；比對至少三篇同類文章、assets/images/posts/ 及最新發布流程。
2. 依當篇需求生成 Front Matter 和原創封面（文風、畫風自由），放到正確位置，必要時補充結語收束圖。
3. 依本契約檢查所有固定欄位，對照實際存在的圖片，執行新文章檢查程式，再用既有轉換器驗收。
4. 如果是 Draft PR，保持在獨立分支；不得誤觸 main 的 Blogger 同步。首次正式發布後才由 Blogger API 取得真實 post ID。

本契約透過 GitHub PR 檢查將「忘記欄位」變成可發現的失敗；它**不是**單靠提示詞就能保證所有平台讀到。為遵守既有 docs/codex-workflow.md §12 的「修改上位規則需全新任務驗證」，本輪不直接修改 AGENTS.md 或該文件。若未來要讓其他 Harness 原生啟動即強制載入新契約，必須先完成其規定的真實新任務驗證。
