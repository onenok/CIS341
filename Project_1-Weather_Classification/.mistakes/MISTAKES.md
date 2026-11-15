# 工作區錯誤紀錄

### 錯誤：PDF Markdown 轉換器誤判標題與表格

- **時間**：2026-11-07 21:00
- **分類**：`需求理解錯誤` / `格式轉換錯誤`
- **任務描述**：將 `CIS341-Project1-2627.pdf` 轉換為 Markdown，保留標題、表格與圖片。
- **錯誤描述**：
  - ❌ 通用短句規則未辨識首頁文件標題，並把表格欄位轉成 `##` 標題。
  - ✅ 重新依文件語意重建標題層級和 Markdown 表格。
- **根本原因**：只依文字外觀猜測標題，未對表格區塊進行結構化處理。
- **修正方式**：首頁標題改用 `#`；章節使用正確層級；表格改為 Markdown 表格。
- **預防措施**：轉換後逐頁檢查標題及表格，不能只檢查文字是否存在。
- **經驗教訓**：PDF 文字抽取結果仍需要語意層級校正。

### 錯誤：edit 工具對 Python 多行 new_str 造成縮排位移，導致 IndentationError

- **時間**：2026-11-09 13:35
- **分類**：`工具誤用` / `縮排錯誤`
- **任務描述**：修改 `tools/check_weather_lib.py`，用 `edit` 工具替換一段 `try:` 區塊內容。
- **錯誤描述**：
  - ❌ `old_str` 首行有 4 空格縮排，`new_str` 首行我同樣寫了 4 空格縮排
  - 結果：首行被「吃掉」4 空格（`step(...)` 跑到第 0 欄），其餘行卻被「加上」4 空格 → `IndentationError: unexpected indent`
  - ✅ 正確做法：改用 Python 腳本按行號重寫區塊（`lines[start:end] = block`）
- **根本原因**：`edit` 工具在處理含縮排的多行 `new_str` 時，無法可靠保留相對縮排；同一問題在 `swipe_filter.py` 也曾發生過（`def act` 被縮進 `view()` 內變成嵌套函式）。
- **修正方式**：
  - 修正前：`edit` 工具直接替換 → 縮排錯亂
  - 修正後：`python -` here-string 腳本，用 `next(i for i,l in enumerate(lines) if l.strip().startswith(...))` 定位區塊邊界後整段替換
- **預防措施**：
  1. 對 `.py` 檔的多行縮排區塊，優先用 Python 腳本按行號重寫，不要用 `edit`
  2. 若一定要用 `edit`，`new_str` 只放單行，或讓 `old_str` / `new_str` 都從第 0 欄開始（不含縮排）
  3. 每次編輯後立刻用 `python -c "import ast; ast.parse(open(f).read())"` 或執行檔案驗證語法
- **經驗教訓**：`edit` 工具不是可靠的縮排編輯器，Python 檔案的多行區塊一律用行號腳本處理。

### 錯誤：誤把 `CELLS[n]` 的 key 當成 notebook 的現行 cell 位置

- **時間**：2026-11-09 17:45
- **分類**：`假設錯誤` / `工具誤用`
- **任務描述**：`tools/_patch_cells.py` — 批次覆寫 `tools/fill_notebook.py` 內 11 個 cell
- **錯誤描述**：
  - 直接寫 `set_cell(11, ...)`、`set_cell(13, ...)`，假設 `CELLS[n]` 的 n 就是 notebook 現行索引
  - 實際執行立刻 `ValueError: substring not found`，因為 `CELLS` 的 key 是**原始**索引（2、4、6…72，全為偶數）
  - 插入 AI 揭露 markdown cell 後，現行位置整體 +1，所以現行 11 對應的是 `CELLS[10]`
- **根本原因**：同一份檔案裡同時存在「原始索引」與「現在位置」兩種座標，我在寫修補器時只憑記憶選了錯的那一套，事前沒有先列出所有 key 驗證。
- **修正方式**：
  - 加上對照表 `SLOT = {11: 10, 13: 12, ...}`，`set_cell()` 內先 `n = SLOT.get(n, n)`
  - 之後每次改 cell 前，先 `re.findall(r'^CELLS\[(\d+)\]', ...)` 印出實際 key
- **預防措施**：
  1. 任何「按索引定位」的操作，先印出目標結構的實際 key 清單再動手
  2. 有兩套座標系並存時，一律用具名 id，不得已才用索引並寫明是哪一套
  3. 批次腳本先做 dry-run（只印「將覆寫 X→Y」）再實際寫入
- **經驗教訓**：索引是最脆弱的定位方式，兩套索引同時存在時幾乎一定會用錯一套；能先用 id 就用 id。

### 錯誤：用 PowerShell here-string 寫含巢狀引號的 Python 會壞掉

- **時間**：2026-11-09 17:55
- **分類**：`工具誤用` / `字串判斷誤用`
- **任務描述**：把 9.4 節的 Gradio description 寫進 `tools/fill_notebook.py`
- **錯誤描述**：
  - here-string 內寫 `description=f"Classes: {\", \".join(SIX)}",`，`\"` 被 PowerShell/Python 多層轉義吃掉
  - 結果檔案裡留下 `{\", \".join(SIX)}`，`compile()` 報 `unexpected character after line continuation character`
- **根本原因**：`@'"'"'...'"'"'@ | python -c` 這條路徑上同時有 PowerShell 字串、Python 字串、目標檔案三層引號，轉義容易錯。
- **修正方式**：改用「按行號取檔 → 直接指定新整行字串 → 寫回」，避免在 shell 裡寫含引號的程式碼。
- **預防措施**：
  1. 需要寫含引號的程式碼時，用檔案（`create` 工具）而不是 shell here-string
  2. 寫完一律 `compile()` 驗證，這次就是靠 `compile()` 才抓到
- **經驗教訓**：shell 是最好的膠水，但最差的程式碼編輯器；有引號就別走 shell。

### 錯誤：將未準備資料集造成的模型表現列為 notebook 缺陷

- **時間**：2026-11-09 22:04
- **分類**：`需求理解錯誤` / `假設錯誤`
- **任務描述**：審查 `project1.ipynb` 的已運行版本，使用者要求排除尚未準備 dataset 導致的模型表現問題。
- **錯誤描述**：將低 validation accuracy、sunny video 預測為 rainy、changing-weather 全部預測為 rainy 列為 findings；這些結果可能完全由未完成的 dataset、標籤、分布與訓練品質造成，不能單憑輸出證明是流程邏輯錯誤。
- **根本原因**：沒有嚴格遵守資料集未準備好的排除條件，將模型輸出品質誤當成 dataset-independent correctness 證據。
- **修正方式**：把低準確率與影片預測錯誤改列為不可判定的觀察，不再作為獨立缺陷；preprocessing double-application 在資料輸入 contract 未確認前也只能列為待確認風險。
- **預防措施**：先建立資料相關排除清單；只有能由程式碼、shape、contract、cell dependency 或明確作業規則證明的問題才列為缺陷。
- **經驗教訓**：未完成資料集時，模型表現不能用來判定流程正確性。

### 錯誤：對已存在的 mistake log 使用新增檔案操作

- **時間**：2026-11-09 22:04
- **分類**：`工具誤用`
- **任務描述**：嘗試同步更新全域與 workspace mistake logs。
- **錯誤描述**：使用 Add File 操作建立已存在的 `MISTAKES.md`，導致 patch 失敗；之後使用不被 view 工具支援的負數行號讀取，又造成讀取失敗。
- **根本原因**：未先確認檔案存在，且錯誤假設 view 支援類 Unix 的負數行號。
- **修正方式**：先用只讀 PowerShell 確認檔案並取得尾端內容，再改用 Update File 追加紀錄。
- **預防措施**：修改前先檢查目標檔案是否存在；view 一律使用正數範圍。
- **經驗教訓**：編輯前確認檔案狀態，工具參數不能依其他工具的習慣推測。

### 錯誤：用 `W.DATA_ROOT` 拼出 raw 資料集路徑，導致整段邏輯靜默跳過

- **時間**：2026-11-10 09:58
- **分類**：`假設錯誤` / `路徑錯誤`
- **任務描述**：`tools/fill_notebook.py` cell 7.2 — 取「未見資料」做介面測試
- **錯誤描述**：
  - 寫成 `NEW_DATA_DIR = W.DATA_ROOT / "raw" / "weather-recognition" / "dataset" / "rain"`
  - 我以為 `DATA_ROOT` 是 `datasets/`，實際它是 `datasets/hand-filtered`
  - 結果 `NEW_DATA_DIR.is_dir()` 為 False，`if` 整段被跳過，測試表只剩 `train` / `val` 兩列
  - **沒有丟任何錯誤**，是看輸出發現 `sources: ['train', 'val']` 少一類才察覺
- **根本原因**：憑變數名稱猜語意（DATA_ROOT 以為是資料集根目錄，其實是「已篩選資料」根目錄），沒有先印出常數實際值。
- **修正方式**：
  - 改為 `W.ROOT / "datasets" / "raw" / "weather-recognition" / "dataset" / "rain"`
  - 加上自證：把這些檔案的 md5 與 split 比對，印出「exact copies already in the split: 0」
- **預防措施**：
  1. 使用任何 `*_ROOT` 常數前，先 `print()` 它的實際值，不要靠命名推測
  2. 以 `Path.is_dir()` 當開關時，一定要在 else 分支印出「找不到路徑」訊息，不能靜默跳過
  3. 新增資料來源時，同時寫一個「這個來源真的符合宣稱」的檢查（如 md5 比對）
- **經驗教訓**：`is_dir()` 守衛是沉默的失敗製造機；條件式的資料載入一定要有 else 訊息。

### 錯誤：在 here-string 內用 `\u` 轉義寫中文，打錯碼點得到亂碼

- **時間**：2026-11-10 09:52
- **分類**：`工具誤用`
- **任務描述**：寫 8.4b 節的 markdown 標題
- **錯誤描述**：`\u9b57\u8b49` 應為 `\u9a57\u8b49`（驗證），前者是無意義字元，會直接顯示在 notebook 上
- **根本原因**：手動輸入 Unicode 碼點，沒有用真正的字元。
- **修正方式**：`t.replace` 換回正確碼點。
- **預防措施**：Python 腳本內直接寫中文字元（檔案存 UTF-8），不要手打 `\uXXXX`。
- **經驗教訓**：能手寫中文就手寫，碼點轉義留給工具產生。

### 錯誤：第二次踩到 `edit` 工具多行 Python 縮排位移

- **時間**：2026-11-10 10:35
- **分類**：`工具誤用`
- **任務描述**：改 `tools/fill_notebook.py` 內 cell `00b64b02` 的 `else:` 分支（把 `deployed_spec = None` 改成實值）
- **錯誤描述**：
  - 用 `edit` 工具替換 5 行內容，`new_str` 的縮排是 4 空格，工具輸出後變成 8 空格
  - 結果：`SyntaxError: unexpected indent`，cell 直接無法 compile
- **根本原因**：`edit` 工具在含縮排的 Python 區塊上會位移縮排（本專案第 2 次發生）。第一次已記錄，但這次為了「只改 5 行」又貪方便用了它。
- **修正方式**：
  - 用 Python 腳本按**完整段落**（含前後錨點）比對替換，並強制 `assert t.count(old) == 1`
  - 修正後 `compile()` 驗證 40 個 cell 全數通過
- **預防措施**：
  1. 本專案任何縮排敏感的 Python 修改，一律寫 Python 腳本做比對替換，不用 `edit`
  2. 替換後**立刻** `compile()` 該 cell，不要累積多個修改後才驗證
  3. 換行字串比對時把 `else:` / `def` 等錨點一起包進 `old`，避免部分比對
- **後續更正（2026-11-10 11:35，使用者質疑後實測）**：
  - 原本的預防措施「一律寫 Python 腳本」被使用者指出是循環論證：寫腳本本身也要用工具。
  - 實測 7 次同一組 `old_str`/`new_str`，其中 1 次縮排被加倍、6 次正常 → 這是**間歇性**問題，不是必然，也不是可以靠排版格式繞開的規則。
  - 真正有效的分工：
    1. 建新腳本用 `create`（`file_text` 逐字寫入，無縮排推論）→ 本輪 4 個腳本全部語法正確
    2. 改既有檔案的縮排敏感區塊，用 `create` 產生的修補腳本做 `text.replace(old, new)` + `assert count == 1`，由 Python 嚴格字面替換
    3. 若真的用 `edit`，替換後**立刻** `compile()` 該區塊，不要累積
- **經驗教訓**：已經記錄過的坑再踩一次，代表預防措施沒有落實成流程。規則寫在筆記上不算數，寫進每次的操作習慣才算。

### 錯誤：修 cv2 stubs 問題時把 `*"mp4v"` 的星號解包弄丟

- **時間**：2026-11-10 20:45
- **分類**：`邏輯缺陷` / `工具誤用`
- **任務描述**：修 `weather_lib.py` L735 `cv2.VideoWriter_fourcc` 的 Pylance 警告（stub 裡沒有這個屬性）
- **錯誤描述**：
  - 原本：`cv2.VideoWriter_fourcc(*"mp4v")` → 把字串解包成 `'m','p','4','v'` 四個字元
  - 我改成：`getattr(cv2, "VideoWriter_fourcc")("mp4v")` → **只丟一個字串**
  - 結果：`TypeError: VideoWriter_fourcc() missing required argument 'c2' (pos 2)`
- **根本原因**：專注在「怎麼繞過型別檢查」，把 `*` 解包在重構時丟掉了。**改寫既有呼叫時只盯著要修的警告，沒有逐字核對原本的呼叫簽名。**
- **修正方式**：
  - `fourcc = getattr(cv2, "VideoWriter_fourcc")(*"mp4v")`（把星號補回）
  - `check_weather_lib.py` → `failures: 0`，`run_notebook_check.py` → `ERRORS: none`
- **預防措施**：
  1. 修型別警告時，**先抄下原始呼叫的完整簽名**（含 `*`、關鍵字參數），改寫後逐字比對
  2. 任何 `getattr(x, "name")(...)` 的改寫，參數必須與原呼叫**完全一致**，只換取值方式
  3. 改完立刻跑該函式的煙霧測試，不要靠「看起來對」判斷
- **經驗教訓**：繞過型別檢查的最小改動是「換取值方式」，不是「重寫整個呼叫」。動手前先看清楚原本傳了什麼。

### 錯誤：在使用者明確說「先不要寫」的情況下，仍在 banner 寫入該觀察

- **時間**：2026-11-10 21:20
- **來源專檔**：Project_1-Weather_Classification（CIS341 Project 1 天氣分類）
- **分類**：`需求理解錯誤`
- **任務描述**：依使用者指示把 notebook 中「結果相關的結論」延後到資料集齊全之後，在 4 個 markdown cell 加入「資料集尚未齊全」的警示 banner
- **錯誤描述**：
  - 使用者用 `ask_user` 給出四項決定，其中 `bias=skip` 明確表示**先不要把「sunny 樣本偏向海景圖」這件事寫進 notebook**
  - 我在 banner 內文仍寫了「而且 sunny 的樣本明顯偏向海景」一句
  - 結果：banner 與使用者決策互相矛盾，且四處重複貼同一份長文，反而稀釋警示效果
- **根本原因**：我把「自己分析出的一個更有洞察力的觀察」當成「應該加進去」的內容，**用自己的判斷蓋過使用者的明確決策**。使用者說 skip 的理由是「目前資料不足以下這個判斷」，而我卻認為這個觀察比數量不足更根本 —— 但那是**我的**判斷，不是他要我寫進作業的內容。
- **修正方式**：
  - 撰寫 `tools/_defer_tier2.py`，從 banner 起點截斷後重寫，移除海景那句
  - banner 改為兩級：`fdbab685`（§6）與 `1a293755`（§8）用全文；`c06fe20b`（6.4）與 `c15f7f0b`（6.6）用三行短版
  - 驗證：notebook 全文 `海景` 出現 0 次、`資料集尚未齊全` 出現 4 次
- **預防措施**：
  1. `ask_user` 的每個選項都是**硬約束**，不是「建議」。寫任何文字前先回頭逐項核對，特別是 `skip` / `remove` 這類否定型選項
  2. 若我認為某個被 skip 的內容其實很重要，**應該在回報時提出並詢問**，而不是直接寫進去再讓使用者發現
  3. 同一段警示文字重複貼 4 次會失效 —— 預設「章節級全文 + 小節級一行」，不要全文複製
- **經驗教訓**：使用者的決策優先於我的洞察。覺得他判斷錯，就說出來讓他決定，不要用手把事情做進去。

---

### 錯誤：品質門檻憑空設定，未用現有資料集校準，誤殺 52 張合格圖

- **時間**：2026-11-11 21:50
- **來源專檔**：Project_1-Weather_Classification（CIS341 Project 1 天氣分類）
- **分類**：`假設錯誤` / `過度簡化`
- **任務描述**：`tools/make_candidates.py` 為 snowy 設定 veto 規則（`MIN_SIDE` / `MIN_BYTES`）
- **錯誤描述**：
  - ❌ 我寫了 `MIN_SIDE = 200`、`MIN_BYTES = 6000`，理由是「太小的圖看不出雪紋理」
  - 實際：621 張裡有 53 張被這條規則否決，全部是 275×183 / 259×194 / 約 11 KB 的圖
  - 但**現有資料集本身**的尺寸根本達不到這個門檻：
    - sunny：min-side 中位數 183，61% 低於 200
    - overcast：min-side 中位數 175，78% 低於 200
    - rainy：min-side 中位數 413，但 p25 只有 194
    - 檔案大小：overcast 中位數 **5 KB**，sunny 中位數 8 KB
  - 也就是說：我用一個比資料集自身標準嚴格得多的門檻在篩新資料，把**比現有圖更清楚**的圖否決掉了
  - 使用者直接看出問題：「很多沒問題的都被 reject 了」
- **根本原因**：
  1. 門檻是憑「我覺得」訂的，沒有先量測 `datasets/hand-filtered` 的實際分布
  2. 更根本：我把門檻當成「絕對品質標準」，但它應該是「相對於既有資料集的一致性標準」。新資料只要不**劣於**現有資料就不該被擋
  3. 沒有把被否決的圖做成複審表，導致錯誤無法被使用者發現（否決項完全不進 `status == proposed` 的渲染）
- **修正方式**：
  - `MIN_SIDE = 200 → 128`、`MIN_BYTES = 6000 → 2500`，並在程式碼註解寫明校準依據（引用各類 p25 與最小檔大小）
  - 結果：vetoed 63 → 12（剩下的 9 張是 `snow_none > 0.6`，圖上確實幾乎沒雪）、duplicate 12 → 25、proposed 545 → **584**
  - 新增 `candidate_sheets.py --include vetoed,duplicate --suffix _vetoed`，讓否決項也能被人工複核
- **預防措施**：
  1. 訂任何資料品質門檻前，先跑 `describe()` 量測**現有資料集**的同一指標，門檻設在既有分布之內
  2. 篩選規則必須可複核 —— 被排除的東西一定要能顯示出來，不能只存在 CSV 的 `status` 欄裡
  3. 「嚴格」不等於「正確」。篩選的目的是排除壞資料，不是展現品味
- **經驗教訓**：門檻要有兩個參照點 —— 作業要求的下限，以及自家資料集的實際分布。少了後者，篩選就變成憑空創造標準。

---

### 錯誤：`clip_top_class` 漏掉 rain 類別，把下雨圖判成 snowy

- **時間**：2026-11-11 21:45
- **來源專檔**：Project_1-Weather_Classification（CIS341 Project 1 天氣分類）
- **分類**：`邏輯缺陷` / `過度簡化`
- **任務描述**：`tools/make_candidates.py` 的 `clip_top_class()`，用來產生 `clip_top` 與 `clip_agrees` 兩欄
- **錯誤描述**：
  - ❌ 初版：`labels = ["snowy", "foggy", "sunny", "overcast"]`，只在這 4 個類別間取 `argmax`
  - CLIP 分數其實有 4 個 prompt group：`scene` / `snow` / `time` / `precip`，衍生出 `rain`、`night`、`fog` 等欄位
  - 問題：下雨的圖在 4 類競賽中**沒有 rain 可以輸**，於是只要 `snow_hi` 比 `fog`/`clear`/`overcast` 高一點，就會被封為 `snowy`
  - 實例：複審表 sheet_012 的 #531、#532 是撐傘、地面積水濺起的**雨天照**，`clip_rain` 高達 **0.986 / 0.909**，卻因為 `snow_hi` 0.387 贏過其他 3 類而被標成綠框「CLIP 同意」
  - 影響規模：545 張 proposed 中有 **21 張** 的 `clip_rain` 高於 4 類最大值
- **根本原因**：
  1. 我用「四個目標類別」當成 CLIP 的完整判斷空間，但 CLIP 的分數另外還有 `rain`/`night`/`graphic`/`indoor` 這些**不合格條件**
  2. 二元式的「CLIP 同不同意」被我用單一 argmax 實作，忽略了「兩個都對」或「兩個都錯」的可能
  3. 使用者之所以發現，是因為他看的是**圖**，我看的是**數字** —— 綠框在我眼裡是「同意」，在他眼裡是明顯的雨天照
- **修正方式**：
  - 改成 `CLIP_BUCKETS` 清單，納入 `rainy / night / graphic / indoor` 共 8 個桶
  - 修正後 `clip_top` 分布：snowy 409、foggy 81、sunny 40、overcast 30、**rainy 20**、night 4
  - 20 張雨天圖不再被誤標為 snowy，`clip_agrees` 由 408→409，而 `False` 由 137→175（多出的 38 張是原本被錯誤歸類的）
- **預防措施**：
  1. 用 `argmax` 做分類前，先列出**所有**可比較的欄位，確認沒有遺漏會贏的類別
  2. 「CLIP 同意」這種判斷要保留原始分數欄位，讓人工能覆核，不要只輸出一個布林值
  3. 排序或標記的結果一定要抽樣看實際圖片驗證 —— 數字合理不代表語意正確
- **經驗教訓**：`argmax` 的答案只在你列出的候選集合內有效。少列一個選項，它就會悄悄變成別人的答案。

### 錯誤：Save 按鈕用「clean slate」覆寫，把使用者整晚的複審清空

- **時間**：2026-11-12 10:40
- **分類**：`邏輯缺陷` / `資料遺失`
- **任務描述**：`tools/review_board.py` 的 `on_save` 與 `gr.State` 初始化
- **錯誤描述**：
  - 我寫的 `on_save` 是「把畫面上所有候選人的 decision 清空，再套用這一輪的標記」
  - `gr.State({"rejects": []})` 開頁時永遠是空清單
  - 使用者隔天重新開頁、畫面上沒有任何標記，一按 Save 就把前一天的 41 個 reject 全部寫成空值
  - `decisions_snowy.csv` 的 append log 保留了紀錄，才救得回來
- **根本原因**：把「UI 目前的選取狀態」當成「資料的完整狀態」。Save 的語意應該是「把差異寫回去」，不是「用畫面覆蓋檔案」。此外 State 沒有從既有資料初始化。
- **修正方式**：
  - State 開頁時從 CSV 載入已有 reject：`already = sorted(df.loc[df.decision=="reject","candidate_id"])`
  - 額外追蹤 `restored` 集合（這一輪被復原的 id）
  - Save 只寫真正被動過的列：`restored -> ""`、`rejects -> "reject"`，其餘不動
  - 三種情境都驗證：開新頁不撳 → 45 不變；多撳 2 個 → 47；復原 1 個 → 44
- **預防措施**：
  1. 任何「Save / 套用」按鈕，先問「如果使用者完全沒動，按下去會發生什麼」
  2. 前端 state 只存差異，不要存完整集合；完整集合以檔案為準
  3. 破壞性寫入前先寫 append-only log（這次就是靠它救回）
  4. 用「開新 session 空手按 Save」當必測案例
- **經驗教訓**：Save 按鈕的預設語意應該是 merge，不是 replace。空白狀態按下去不可以改變任何既有資料。

### 錯誤：在 cuaca 資料處理前誤把原始圖片直接視為可入庫資料
- **時間**：2026-11-13 13:59
- **分類**：需求理解錯誤 / 過度簡化
- **任務描述**：cuaca 三類資料加入 sunny、overcast、rainy
- **錯誤描述**：未先依使用者已說明的「同一圖片經變換後重複」建立去重後候選集，就提出直接併入並重建資料集的方案。
- **根本原因**：把資料夾張數當成有效獨立樣本數，忽略來源資料集的變換副本特性與使用者既定流程。
- **修正方式**：停止直接併入；先建立全域指紋/感知雜湊去重結果，再將代表圖做成候選 manifest，沿用 snowy 審圖板逐張人工確認。
- **預防措施**：所有新來源先完成去重報告與候選帳本，未經人工審核不得寫入 hand-filtered 或 image_index。
- **經驗教訓**：資料夾中的圖片數不等於可用獨立樣本數，必須先去重再審核。

### 錯誤：cuaca 去重工具直接執行時找不到 weather_lib
- **時間**：2026-11-13 14:00
- **分類**：工具誤用 / 路徑錯誤
- **任務描述**：執行 	ools/make_cuaca_candidates.py
- **錯誤描述**：首次執行報 ModuleNotFoundError: No module named 'weather_lib'。
- **根本原因**：新工具未像既有工具一樣在匯入前將專案根目錄加入 sys.path。
- **修正方式**：在模組頂端加入 sys.path.insert(0, str(ROOT))，並保留延遲匯入 weather_lib。
- **預防措施**：新建 tools 腳本時先對照既有腳本的直接執行入口與匯入初始化。
- **經驗教訓**：工具腳本必須同時支援從專案根與 tools 目錄直接執行。

### 錯誤：加入 lightning 後使用四類預設重建 index
- **時間**：2026-11-13 19:44
- **分類**：假設錯誤 / 資料遺漏
- **任務描述**：將 309 張 lightning 候選加入正式資料集並重建 index/split
- **錯誤描述**：第一次呼叫 uild_index() 使用預設 CLASS_ORDER，只掃描 sunny、overcast、rainy、snowy；結果 lightning 已複製但未進入 image_index 或 split。
- **根本原因**：沒有注意 CLASS_ORDER 是四個基礎類別，foggy/lightning 是額外類別，需明確傳入 labels。
- **修正方式**：改用 uild_index(labels=["sunny", "overcast", "rainy", "snowy", "lightning"])，重新產生 index、dedupe 與 split。
- **預防措施**：每次新增類別後，重建資料集都明確列出要納入的 labels，並比較各 hand-filtered 資料夾與 index 的數量。
- **經驗教訓**：資料夾已存在不代表資料管線會自動掃描；要驗證 index 的 label 分布。

### 錯誤：把知覺雜湊的誤判當成真重複，並要求使用者二選一
- **時間**：2026-11-13 20:31
- **分類**：過度簡化 / 邏輯缺陷
- **任務描述**：foggy 入庫時 dedupe 報跨類衝突，我建立對照頁面讓使用者選邊
- **錯誤描述**：使用者在對照頁面看到 4 組圖後指出「這幾張圖完全不一樣」，我才去量測。實際像素差異 38.75、38.15、63.98、89.31（0-255），md5 全不同，根本不是同一張圖。
- **根本原因**：uild_index 只靠 ahash + dhash 各 6 bit 判定近似重複。暗背景 + 單一亮光源的夜景，無論拍的是霧街還是閃電，8x8 灰階結構幾乎一樣，兩種雜湊都會落在門檻內。我沒有驗證「被判重複的兩張圖到底像不像」就直接建 UI 讓使用者裁決。
- **修正方式**：
  1. weather_lib.py 新增 pixel_diff()：64x64 灰階縮圖的平均絕對差。
  2. uild_index(..., pixel_threshold=12.0)：ahash、dhash 通過後再要求像素差異 ≤ 12。
  3. 
eps 每筆加上 path 以便比對。
  4. 重跑後跨類衝突 0；剩餘 62 組近似重複像素差異中位數 1.39、最大 11.94，全為真重複。
- **預防措施**：
  1. 任何「自動判定重複」的結果，先抽樣視覺驗證再拿去用或建介面。
  2. 建立錯誤回報頁面前，先自己確認資料本身是否合理，不要把錯誤前提包成 UI 丟給使用者。
  3. 多模態（雜湊）判定加一個像素層級的二次驗證。
- **經驗教訓**：使用者說「這些圖不一樣」時，先量測再說；雜湊碰撞在低對比或高對比夜景上非常常見。

### 錯誤：預處理在同一個 pipeline 中執行了兩次（tf.data 一次 + 模型內一次）

- **時間**：2026-11-14 16:35
- **來源專檔**：Project_1-Weather_Classification（CIS341 天氣分類）
- **分類**：`邏輯缺陷` / `重複執行`
- **任務描述**：`project1.ipynb` cell 35（`build_scratch_cnn`）與 cell 37（`build_transfer_model`）；`weather_lib.make_dataset` 套用 `spec.fn`
- **錯誤描述**：
  - `weather_lib.make_dataset` 在 tf.data 管線中執行 `spec.fn(x)`：
    - `scratch` → `x / 255`，得到 `[0, 1]`
    - `mobilenet_v2` → `preprocess_input(x)`，得到 `[-1, 1]`
  - 但模型內部又各做了一次：
    - cell 35：`layers.Rescaling(1/255)` → 再除一次，像素變成 `[0, 0.0039]`
    - cell 37：`layers.Lambda(preprocess_input)` → 再映射一次，全部擠到約 `-1.0`
  - 後果：整張圖幾乎變成常數，mobilenet 四類驗證準確率只有 **0.514**，驗證預測集中在 2 個類別
  - 因兩處都錯，訓練／影片推論／Gradio 三條路徑「一致地錯」，表面看不出不一致，只有準確率異常
- **根本原因**：撰寫時在「資料管線負責前處理」與「模型自帶前處理」兩種設計之間搖擺，結果兩邊都寫了，卻沒有任何一處斷言「前處理只發生一次」。cell 21 的探針只驗證 `spec.fn` 的輸出，沒有驗證模型實際收到的張量。
- **修正方式**：
  - cell 35：移除 `x = layers.Rescaling(1.0 / 255, name="rescale_0_1")(inputs)`
  - cell 37：移除 `x = layers.Lambda(...preprocess_input...)(inputs)`，改為 `x = base(inputs, training=False)`
  - `weather_lib.spec_for()` 的 `note` 改為明確聲明「模型不含縮放層，此函式是唯一縮放處」
  - `weather_lib.make_dataset()` docstring 加入同樣契約
  - cell 23 / 77 的 `class_order.json` 增加 `preprocess` 欄位，讓存檔模型自我描述
  - 修正後 epoch 1：scratch `0.207 → 0.571`、mobilenet `0.482 → 0.800`；epoch 3 mobilenet 達 **0.886**，驗證預測分佈與真實分佈吻合
- **預防措施**：
  1. 前處理（縮放、正規化）只能有一個權威位置；若模型自帶縮放層，管線必須改為 identity，反之亦然
  2. 在 pipeline 與模型交界處加驗證：印出「模型真正收到的張量」的 min/max/mean，而非只印 `spec.fn` 的輸出
  3. 看到「訓練／驗證／推論三條路徑一致但準確率異常低」時，優先懷疑共同的資料路徑，不是模型架構
  4. 建模後立刻檢查 `model.layers[:2]`，確認第一層是預期的 `Conv2D` 或 `Functional`（backbone），不是 `Rescaling` / `Lambda`
- **經驗教訓**：重複執行不會報錯，只會讓模型安靜地變笨。要驗證的是「模型收到什麼」，不是「我以為我送出了什麼」。

### 錯誤：BatchNorm 的 moving statistics 在少量 step 下失效，導致驗證集塌陷成單一類別

- **時間**：2026-11-14 16:35
- **來源專檔**：Project_1-Weather_Classification（CIS341 天氣分類）
- **分類**：`假設錯誤` / `框架預設值誤用`
- **任務描述**：`project1.ipynb` cell 35 的 `build_scratch_cnn`，連續 `BatchNormalization()` 使用 Keras 預設 `momentum=0.99`
- **錯誤描述**：
  - 訓練 7-8 epochs 後 `train_acc=0.81` 但 `val_acc` 從第 1 epoch 起固定 **0.207**，val_loss 單調上升
  - `val_acc=0.207` 剛好等於驗證集多數類比例（60/280），表示模型對每張圖都輸出同一類
  - 對同一批驗證資料實測：`training=True`（用當前 batch 統計）準確率 **0.857**，`training=False`（用 moving average）**0.329**，差距 **+0.529**
  - 量測各層統計量，儲存的 `moving_var` 比真實批次 `var` 大 **8-10 倍**
- **根本原因**：
  - Keras 更新公式為 `moving = moving * momentum + batch * (1 - momentum)`，`momentum=0.99` 的有效視窗是 `1/(1-0.99) = 100` 次更新
  - 本資料集 1125 張訓練圖 ÷ batch 32 = **每 epoch 只有 36 次更新**，要 2.8 個 epoch 才輪換一次視窗
  - 未訓練時各層輸出分佈寬（var 大），收斂後變窄；moving average 是落後指標，仍帶著早期寬分佈的記憶，形成**系統性偏差**而非隨機誤差
  - 分母 `sqrt(var)` 大 10 倍 → 開根號後約 3.2 倍；四層疊乘 3.2⁴ ≈ 100 倍衰減，後續 `Dense` 收到近乎零的輸入
  - 次要因素：`EarlyStopping(monitor="val_loss", patience=6)` 在 BN 尚未成熟的上升期（epoch 1-6 val_loss 1.42→3.47）就觸發，把模型砍在崩潰狀態
- **修正方式**：
  - 移除 cell 35 的 4 個 `BatchNormalization` 層
  - 實測比較（15 epochs，同 split / seed / augmentation）：

    | 方案 | 最佳 val_acc | batch/inference 差距 | 15ep 耗時 |
    |---|---:|---:|---:|
    | BN momentum=0.99 | 0.793 | +0.089 | 7.1 分 |
    | GroupNorm groups=8 | 0.864 | -0.007 | 7.4 分 |
    | 無 normalization | 0.821 | -0.043 | 2.8 分 |

  - 選擇「移除 BN」：無隱藏狀態、速度最快、效果在噪音範圍內不輸
- **預防措施**：
  1. 小資料集（每 epoch 更新次數遠小於 `1/(1-momentum)`）不要用 BatchNorm，或必須把 `momentum` 調到 `0.9` 以下
  2. 若堅持用 BN，必須驗證 `training=True` 與 `training=False` 的輸出一致性，不能只看 loss 曲線
  3. `val_acc` 恰好等於多數類比例時，這是「模型塌陷」的明確訊號，應先印出預測分佈再動超參數
  4. 遇到「train 上升、val 不動」不要先怪 overfitting；先量測 train / inference 兩條路徑的差異
- **經驗教訓**：框架預設值是為大資料集設計的。`momentum=0.99` 在 ImageNet 上合理，在 288 次更新的小資料集上致命。任何有「歷史記憶」的層，都要先算清楚「需要多少步才會成熟」。

### 錯誤：驗證腳本與 notebook 的實作不一致，導致「驗證通過」其實沒驗證到

- **時間**：2026-11-14 16:20
- **分類**：`邏輯缺陷` / `假設錯誤` / `驗證失效`
- **任務描述**：`project1.ipynb` cell 35 的 `build_scratch_cnn` — 移除 `Rescaling` 層與 `BatchNormalization` 層
- **錯誤描述**：
  - 修改前：`x = layers.Rescaling(1.0 / 255, name="rescale_0_1")(inputs)`，之後迴圈從 `x` 開始串接
  - 我移除了 Rescaling 那行，但**沒有**補上 `x = inputs`
  - 結果：迴圈第一次迭代執行 `layers.Conv2D(...)(x)` 時，`x` 尚未定義
  - 實際錯誤：`UnboundLocalError: cannot access local variable 'x' where it is not associated with a value`
  - 連鎖後果：cell 35 失敗 → cell 39（`scratch_model.summary()`）與 cell 45（四類訓練）全部失敗 → 整份執行結果中**四類模型完全沒有訓練**
- **根本原因**：
  - 我在 `runs/verify_fix.py` 裡寫的是 `x = inputs if block == 1 else x`，這是刻意繞開「第一次迭代 x 未定義」的寫法，所以驗證腳本跑得通
  - 但 notebook 的 patch 版本用的是 `x = inputs` + 直接進入迴圈，我沒有把兩邊對齊
  - 於是我用「行為等價」的驗證腳本，去驗證了一個「內容不等價」的 notebook cell
- **修正方式**：
  - 在 `for block, filters in ...` 迴圈之前插入一行 `x = inputs`
  - 修正後重跑完整 notebook：0 錯誤，四類 scratch_cnn 0.8036、mobilenet_v2 0.9143
- **預防措施**：
  1. **驗證腳本必須從 notebook 直接抽出程式碼**，不能手動重打一遍。做法：用 `json` 讀 notebook，把目標 cell 的 source 用 `exec()` 執行，而不是複製貼上
  2. 若無法避免複製，複製後必須 diff 兩份程式碼，確認逐字一致
  3. 「邏輯等價」不是「程式碼等價」—— 等價推理本身就可能出錯
  4. 修改包含控制流的程式碼（迴圈前後的變數初始化）時，要檢查「迴圈首次迭代時所有變數是否都已定義」
- **經驗教訓**：用「我自己重寫的版本」去驗證「我改過的正式版本」，等於沒驗證。驗證的對象必須是真正要交付的那份程式碼。

### 錯誤：用「同一個函式呼叫兩次」驗證前處理重複，卻沒發現該函式會就地改寫輸入

- **時間**：2026-11-14 22:24
- **來源專檔**：Project_1-Weather_Classification（CIS341 天氣分類）
- **分類**：`假設錯誤` / `邏輯缺陷` / `驗證方法錯誤`
- **任務描述**：重寫 `project1.ipynb` cell 49 的 6.4.1 節，用探針值 `[0, 128, 255]` 證明「前處理被執行了兩次」會把像素壓成常數。
- **錯誤描述**：
  - 我寫的驗證程式碼是 `once = W.spec_for("mobilenet_v2").fn(probe)`，接著 `twice = W.spec_for("mobilenet_v2").fn(once.reshape(1,1,3))`。
  - 預期 `twice` 應該是 `[-1.0079, -1.0078, -1.0078]`（幾乎常數），`once` 是 `[-1, 0.0039, 1]`。
  - 實際印出：`once` 與 `twice` **完全相同**，都是 `[-1.0078, -1.0000, -0.9922]`。表格的「修正後像素範圍」變成荒謬的 `[-1, -1]`。
  - 我一度懷疑 Keras 3.1.1 改變了 `preprocess_input` 的公式，白花時間在錯誤方向上。
- **根本原因**：
  1. Keras 的 `mobilenet_v2.preprocess_input` 實作為 `x /= 127.5; x -= 1.0`，**回傳的是同一個物件**（`r is a` 為 `True`、`np.shares_memory(r, a)` 為 `True`），所以它就地改寫了傳入的 numpy 陣列。
  2. 於是 `once` 這個「結果」與 `probe` 這個「輸入」是同一塊記憶體。第一次呼叫把 `probe` 改成 `[-1, 0.0039, 1]`；第二次呼叫作用在已是 `[-1, 0.0039, 1]` 的同一塊記憶體上，得到 `[-1.0078, -1, -0.9922]` 再寫回同一塊 → 兩個變數自然印出同一個值。
  3. 我沒有先確認「這個函式是不是純函式」就假設它是。
- **修正方式**：
  - `weather_lib.py`：`_mobilenet_v2` 改為先複製再處理，讓 `spec.fn` 成為純函式。
  - 修正前：`return tf.keras.applications.mobilenet_v2.preprocess_input(x)`
  - 修正後：先 `if isinstance(x, np.ndarray): x = x.copy()` 再呼叫 `preprocess_input(x)`。
  - `project1.ipynb` cell 49：量測一律經過 `fresh_probe()` 取得新陣列，`fn` 的輸入處再 `reshape` 出新物件。
  - 驗證後正確輸出：`once = [-1, 0.0039, 1]`、`twice = [-1.0078, -1, -0.9922]`，可變範圍從 `2.0` 塌成 `0.0157`。
- **附帶發現（真實的第三個缺陷）**：`weather_lib` 既有的呼叫點（`make_dataset` L498、`predict_frames` L712、`annotate_video` L789）都傳 `tf.Tensor` 或新建陣列，所以正式流程沒有被就地改寫影響（這也是四類 0.9143 仍成立的原因）；但這是隨時會咬人的地雷，已一併移除。
- **預防措施**：
  1. 把任何第三方函式接進自己的 pipeline 當「純函式」用之前，先測 `fn(a) is a` 與 `np.shares_memory(fn(a), a)`。
  2. 需要證明「套用兩次會壞掉」時，**兩次都要傳入獨立的副本**，否則測到的是別的東西。
  3. 表格或圖表出現看似不可能的數字（如像素範圍 `[-1, -1]`、兩個變體輸出完全相同）時，先當成程式錯誤來查，不要推給「函式行為改變」。
  4. 驗證腳本必須直接 `exec()` notebook 的原文，而不是自己重寫一份等價邏輯（與上一筆錯誤同源）。
- **經驗教訓**：看起來「理所當然是純函式」的函式，可能就地改寫你的陣列；共享記憶體會讓兩個變數變成同一個變數。先用 `is` 和 `shares_memory` 驗證，再開始推理。

## 📝 錯誤記錄：把「圖片張數」當成「元素數量」計算每通道變異數

- **時間**：2026-11-15 11:00
- **來源專檔**：Project_1-Weather_Classification（CIS341 天氣分類）
- **分類**：`邏輯缺陷` / `型別錯誤`
- **任務描述**：`project1.ipynb` cell 51 — 比較 BatchNormalization 的 `moving_variance` 與驗證集在該層的實際變異數
- **錯誤描述**：
  - 為了避免一次把 280 張圖在四層的中間特徵全部收進記憶體（約 250 MB，實測 `numpy._ArrayMemoryError`），改成逐批次累加。
  - ❌ 第一次：用單遍公式 `sum(x^2)/n - mean^2`，因為激勵值的平均遠大於分散程度，兩個大數相減產生災難性相消 → 算出**負的變異數**（-1.3e7）與荒謬比值（6.5e10）
  - ❌ 第二次：改用兩遍掃描（先算平均再算離差平方），但除數用「圖片張數 `seen`」→ 得到變異數 1.98e11
  - ✅ 正確：除數必須是**該層的元素個數** `batch*H*W`
- **根本原因**：BN 的 `moving_variance` 是**逐通道**統計量，所以攤平成 `(batch*H*W, C)` 之後，每個通道的樣本數是 `batch*H*W`，不是 `batch`。四層的 H、W 各不相同（32×32、16×16、8×8、4×4），所以每個層都要各自累加自己的元素個數。我用「幾張圖」當除數，等於把平均值放大了 H×W 倍（bn1 是 1024 倍），變異數自然放大 H²W² 倍。
- **修正方式**：
  - 程式碼位置：`project1.ipynb` cell 51（`weather_lib` 未涉及）
  - 修正前：`means = [acc / seen for acc in means]`
  - 修正後：`counts[i] += int(flat.shape[0])` 逐層累加，再 `means = [acc / n for acc, n in zip(means, counts)]`
  - 驗證：變異數回到 0.009–0.046 的合理範圍
- **預防措施**：
  1. 計算統計量前，先寫下「分母代表什麼實體」——是樣本數、元素數、還是類別數
  2. 看到 `e+11` 這種數量級的數字就要警覺，正常激勵值的變異數不會超過 10
  3. 攤平多維張量做統計時，列出 `reshape` 前後的形狀對照，確認每個軸的意義
  4. 優先使用 `np.var` 在單一小陣列上驗算，再放大到批次累加版本
- **經驗教訓**：形狀 `(N, H, W, C)` 攤平成 `(-1, C)` 之後，第一維已經不是 `N`。凡是「逐通道」統計，分母一定是 `N*H*W`，而每一層的 H、W 都不同，必須逐層記帳。


### 錯誤：load_split 只補上 ROOT 前綴，沒有統一磁碟機大小寫

- **時間**：2026-11-15 13:56
- **來源專檔**：Project_1-Weather_Classification（CIS341 天氣分類）
- **分類**：`路徑錯誤` / `型別錯誤`
- **任務描述**：`weather_lib.py` — 把 split CSV 的絕對路徑改成可攜式相對路徑
- **錯誤描述**：
  - ❌ 第一版 `load_split` 只做 `ROOT / p`，結果同一張圖產生兩種字串表示：
    - `c:\Users\honok\...`（CSV 內原本的內容）
    - `C:\Users\honok\...`（由 `ROOT` 推導）
  - 預期：round-trip 後 DataFrame 完全相同
  - 實際：`Path` 比較為 True，但字串比較為 False → 若下游用 `path` 欄位做 groupby / merge 的鍵，會產生重複群組
- **根本原因**：Windows 的磁碟機代號大小寫不敏感，`Path("c:/x") == Path("C:/x")` 為真，所以 `Path` 相等測試通過，掩蓋了字串不一致。沒有把「輸出必須是單一表示法」當成需求。
- **修正方式**：
  - 位置：`weather_lib.py` `load_split` / 新增 `_anchor()`
  - 修正前：`split["path"] = [str(ROOT / p) if not Path(p).is_absolute() else p ...]`
  - 修正後：`_anchor()` 先 `p.resolve()`（Windows 上會正規化為磁碟實際大小寫），再 `relative_to(ROOT)` 重新組回，確保所有路徑都以 `ROOT` 的拼法輸出
- **預防措施**：
  1. 任何「從外部檔案讀進來的路徑」都要經過同一個正規化函式，不要在呼叫端各自拼接
  2. Windows 上驗證路徑一致性時，不能只比 `Path`，要比字串
  3. 寫 round-trip 測試時，斷言要同時涵蓋「字串相等」與「檔案存在」
- **經驗教訓**：`Path.__eq__` 在 Windows 會隱藏大小寫差異，讓我以為測試通過；對於要被當成鍵使用的路徑字串，必須額外斷言字串完全相等。
