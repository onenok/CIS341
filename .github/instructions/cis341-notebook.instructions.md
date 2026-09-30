---
name: cis341-notebook
description: "Use when creating, editing, or reviewing Jupyter notebook cells in the CIS341 workspace, especially assignment1/S26202765_assignment1.ipynb. Enforces a consistent per-task cell structure (markdown heading, description, code, test output, screenshot placeholder with caption) and the assignment's submission rules. CIS341 作業 notebook 的 cell 結構與繳交規範。"
applyTo: "**/*.ipynb"
---

# CIS341 Notebook 撰寫規範

適用於本工作區所有 `.ipynb`，主要對象是 `assignment1/S26202765_assignment1.ipynb`。

## 每個任務的固定 cell 結構

每個任務（Task 1–5）依序使用以下 cell，**順序不可調換**：

1. **Markdown 標題 cell**
   - 格式：`## Task N: <名稱> (<分數> marks)`
   - 內容：Objective 一句話 + 該任務的 Must 清單（逐條列出，方便對照評分表）
2. **Markdown 說明 cell**
   - 說明這個 app 做什麼、使用者怎麼操作、輸出怎麼讀
   - 若規格有「會扣分」的例子，在這裡寫明「本實作採用 X 而非 Y」
3. **程式碼 cell（可多個）**
   - 每個 cell 開頭用註解標明對應哪條 Must，例如 `# Must 1: score_guess(secret, guess)`
   - 純函式（如 `gcdlcm`、`score_guess`）與 Gradio UI **分開成不同 cell**
4. **測試 cell**
   - 直接呼叫函式並印出結果，涵蓋規格指定的測試案例
   - 例如 Task 1 必須測 `(12, 18)`, `(0, 5)`, `(0, 0)`, `(-8, 12)`, `abc`
5. **Markdown 截圖 cell**
   - 標題：`### Screenshots`
   - 逐條列出規格要求的截圖，每條一行 caption
   - 尚未截圖時保留佔位文字：`> ⚠️ 待補：<截圖說明>`

## 程式碼規範

- **AI 參與標註**：規格要求 "State in comments which tools you used and for what"。
  在 notebook 第一個 cell 與每個任務的程式碼 cell 中，用註解誠實標註哪些部分由 AI 協助。
- **模型載入與訓練必須在 app 之前**：
  - Task 4 的 `gensim.downloader.load("glove-wiki-gigaword-100")` 放在**獨立 cell**
  - Task 5 的 AE/VAE 訓練放在**獨立 cell**
  - 兩者都不可寫進 Gradio 的處理函式內
- **輸出格式**：不可把 raw 資料直接丟給使用者
  - Task 4：不可印 `[('paris', 0.71), ...]` 或 JSON，要用 `gr.Label`
  - Task 5：不可印 `array([[ 0.1234567, ...]], dtype=float32)`，要四捨五入成 `0.12, -1.30, 0.85`
- **錯誤處理**：所有使用者輸入路徑都要有 `gr.Error` 或明確訊息，不可讓 traceback 冒出來

## 繳交規範（來自 PDF）

- 五個任務**全部在同一個 notebook**
- 截圖放在**所屬任務的 cell 下方**，或集中成一份 PDF
- 每張截圖要有**一行 caption** 說明它展示什麼
- 截圖必須是**自己跑起來的 app**，不能是 mockup
- 缺截圖 → 該介面的 UI/UX 分數**砍半**

## 禁止事項

- 不要為了「整齊」而把多個任務合併成一個 cell
- 不要刪除或改寫規格指定的常數（例如 Task 2 的 `WORDS` 清單）
- 不要在 notebook 中留下未執行的實驗性 cell；驗證用的臨時腳本寫成 `_*.py` 檔
- 不要把截圖佔位文字當成已完成；沒有圖就是沒有分