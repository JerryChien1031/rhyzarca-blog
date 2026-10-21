# Git Working Tree Ownership & Commit Integrity Policy

本規範為硬性安全規則，高於一般任務便利性。

## 1. 基本不變量

Agent 只能提交「本次任務由 Agent 自己產生，且屬於明確授權範圍」的變更。

任何在任務開始前已存在於 working tree、index 或 untracked files 中的內容，
預設均屬於使用者或其他工作流程。

除非使用者明確授權，Agent 不得：

- 修改這些既有變更
- staged 這些既有變更
- commit 這些既有變更
- reset / restore / checkout 這些既有變更
- stash 這些既有變更
- 刪除這些既有變更
- 用自己的版本覆蓋這些既有變更

無法確認變更所有權時，一律視為「不是 Agent 的」。

## 2. 任務開始前必須建立 Working Tree Baseline

任何會修改檔案的任務開始前，必須先執行至少：

git rev-parse HEAD
git status --porcelain=v1 -uall
git diff --name-status
git diff --cached --name-status

並記錄：

BASE_HEAD
PREEXISTING_MODIFIED_FILES
PREEXISTING_STAGED_FILES
PREEXISTING_UNTRACKED_FILES

這個 baseline 必須在第一次 Write / Edit / apply_patch 前完成。

如果沒有 baseline，
Agent 不得在任務結束時執行 git commit，
因為已無法證明哪些變更屬於自己。

## 3. Pre-existing Dirty Files 視為受保護資產

任務開始時已 modified / staged / untracked 的檔案，
全部標示為：

PREEXISTING_DIRTY

預設：

READ ONLY
DO NOT STAGE
DO NOT COMMIT

如果任務不需要修改它：
完全不得碰觸。

如果任務確實需要修改同一檔案：
不得直接整檔 stage。

必須停止並：

A. 使用隔離 worktree 處理；
或
B. 明確取得使用者同意；
或
C. 能可靠做到 hunk-level ownership isolation。

無法隔離時不得 commit 該檔案。

## 4. 每項任務必須建立 Commit Allowlist

在開始修改前，Agent 必須列出本次預期允許修改的檔案，例如：

TASK_ALLOWLIST:
- _pages/about.md
- scripts/blogger_api.py
- scripts/sync_to_blogger.py
- assets/js/blogger.js
- assets/css/blogger.css
- .github/workflows/sync.yml

此清單之外的檔案不得自動納入 commit。

若實作過程發現必須修改額外檔案，
必須先進行 scope amendment：

- 說明為什麼需要
- 將檔案加入 TASK_ALLOWLIST
- 確認該檔案不是 PREEXISTING_DIRTY

完成後才能修改。

不得先修改、最後才合理化。

## 5. 禁止 Broad Staging

Agent 禁止使用：

git add .
git add -A
git add --all
git add *
git commit -a
git commit -am

以及任何等效的「把整個 working tree 一次納入」操作。

也不得因為某資料夾看起來屬於任務，就直接：

git add scripts/
git add assets/
git add _posts/

除非該資料夾中的每一個 staged path
都已逐一存在 TASK_ALLOWLIST 中。

正常 staging 必須使用明確路徑：

git add -- path/to/file1 path/to/file2

## 6. Staging 不代表可以 Commit

完成 git add 後，Agent 必須執行：

git diff --cached --name-status
git diff --cached

並逐一審查 staged diff。

不只是確認檔名，
必須確認每一個 staged hunk 都屬於本次任務。

任何以下情況必須停止 commit：

- staged path 不在 TASK_ALLOWLIST
- staged path 屬於 PREEXISTING_DIRTY
- staged hunk 無法確認來源
- staged 內容與任務無直接關係
- 出現使用者原本未提交的工作
- 出現其他 Agent 的工作
- 出現臨時檔、log、token、secret
- 出現「順手整理」但未經授權的修改

## 7. 同一檔案存在混合所有權時

若某檔案同時包含：

USER_HUNK
+
AGENT_HUNK

Agent 不得：

git add <whole-file>

優先策略：

1. 不 commit 該檔案；
2. 使用獨立 worktree；
3. 使用精確 patch / hunk staging；
4. 必要時要求使用者裁定。

絕對禁止因為 Agent 也修改過該檔案，
就宣稱整個檔案都屬於 Agent。

## 8. Commit 前硬閘門

commit 前必須產生：

BASE_HEAD
TASK_ALLOWLIST
PREEXISTING_DIRTY
AGENT_MODIFIED
STAGED_FILES

並確認：

STAGED_FILES ⊆ TASK_ALLOWLIST

且：

STAGED_FILES ∩ PREEXISTING_DIRTY = ∅

除非對交集項目已有明確 hunk isolation 授權。

只要條件不成立：

FAIL CLOSED
不得 commit。

## 9. Commit 後驗證

commit 後必須執行：

git show --stat --oneline HEAD
git show --name-status HEAD

並再次確認：

- commit 只包含本次任務
- 沒有使用者既有變更
- 沒有未授權檔案
- 沒有 Secrets
- 沒有 unrelated cleanup

若發現越界，
不得 push。

## 10. Push 為獨立權限

git commit 與 git push 為不同權限。

即使 commit 成功，
沒有明確 push 授權仍不得 push。

## 11. 禁止「順便整理」

以下理由不構成修改授權：

- 順便更新 README
- 順便整理格式
- 順便補測試
- 順便更新 requirements
- 順便清 .gitignore
- 順便修 lint
- 順便重構
- 這樣比較完整
- 這是最佳實務

如果確實為任務必要條件，
必須先聲明 scope expansion，
再納入 TASK_ALLOWLIST。

## 12. 任務完成回報必須附 Commit Receipt

每次 Agent 建立 commit，都必須回報：

Task:
Base HEAD:
Pre-existing dirty files:
Authorized files:
Files actually modified:
Files staged:
Files committed:
Protected files deliberately excluded:
Commit SHA:
Push status:

如果無法提供這份 receipt，
視為 commit provenance 不完整。
## 13. rhyzarca-blog 執行前必讀入口

開始本專案任務時，除上述 Git 政策，必須完整閱讀 [Codex 執行與驗收規則](docs/codex-workflow.md)，再依當次授權執行。不要只讀連結標題或自行推定內容；此補充不得削弱前述所有權、staging、Commit 與 Push 規範。

執行時尤其遵守：

- 先核對 Repository、既有程式、工作樹 baseline 與精確檔案 allowlist。
- 「依既有格式」不代表改換文體；技術文章保留技術論述，不套用思想或生活文章風格。
- 沿用既有有效圖片；格式修正不授權重製圖片，使用者禁止產圖時立即遵守。
- 原始素材、原有未提交變更及公開安全邊界都必須保護。
- 用實際 Markdown／Blogger 轉換與顯示驗收，不以自製替代流程推定成功。
- 分別核對 Commit、Push、發布與 OAuth 變更授權；已給過且適用的授權不重複詢問。
- Push 前查 Workflow 副作用；發布後查實際 run、真實 identity 與公開內容，不能以 Push 成功代替同步成功。

本文件是專案指示入口；被連結的文件須明確讀取，並非任意 Markdown 都會自動載入。既有會話應重讀更新後的規則；不要擅自建立 AGENTS.override.md 或修改全域設定來覆蓋本政策。
