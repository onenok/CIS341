---
name: gradio
description: "Use when writing or debugging Gradio code in the CIS341 workspace: gr.Blocks layouts, gr.State session state, gr.ImageEditor composite handling, gr.Label score display, gr.HTML coloured tiles, gr.Gallery select events, gr.Error/gr.Warning/gr.Info feedback, and slider change events. Covers the components this assignment needs beyond what was taught in class. CIS341 作業所需的 Gradio 元件用法與陷阱。"
applyTo: "**/*.ipynb"
---

# Gradio 元件用法與陷阱（CIS341 Assignment 1）

本作業用到幾個課堂沒教的元件。以下是每個元件的正確用法與常見錯誤。

## gr.Blocks + gr.Tab（Task 5 強烈建議）

Task 5 的四（或五）個介面放在**同一個 app**，每個介面一個 tab：

```python
with gr.Blocks(title="AE / VAE Lab") as demo:
    gr.Markdown("...說明...")
    with gr.Tab("Reconstruct"):
        ...
    with gr.Tab("Draw"):
        ...
```

好處：使用者只開一個 app，切換實驗不用重啟。分開成四個 app 也可以，但體驗較差。

## gr.State（Task 2、Task 3）

**用途**：讓每個瀏覽器 session 有自己的狀態，而不是所有玩家共用一個。

```python
secret_state = gr.State("")      # 每個 session 一份
guesses_state = gr.State([])
```

**陷阱**：
- `gr.State` 的值**只能透過函式回傳更新**，不能直接賦值
- 函式要回傳新值，並在 `outputs` 中列出該 state
- 若只是要「跨點擊記住」，用模組層級變數也能動，但所有使用者會共用（Task 2 的 Optional 項目就是改用 `gr.State`）

## gr.ImageEditor（Task 5 Draw）

**關鍵陷阱**：`gr.ImageEditor` 的值是**字典**，不是影像。完成的圖在其中一個 key 底下。

```python
def draw_fn(editor_value):
    # editor_value 是 dict，含 "background", "layers", "composite"
    composite = editor_value["composite"]   # 這才是畫完的圖
```

**務必先確認 key 名稱**（不同 Gradio 版本可能不同），做法是印出 `editor_value.keys()` 再決定。

**後續處理**（規格 Must）：
1. 取 composite
2. 轉灰階
3. **偵測背景色**（通常是白底黑線）→ 必要時**反相**成 MNIST 的黑底白字
4. resize 到 28×28

## gr.Label（Task 4）

**用途**：顯示 word → score 的字典，Gradio 自動畫長條圖。

```python
gr.Label(label="Top 5 candidates")   # 輸出時傳 dict
# 回傳：{"paris": 0.71, "rome": 0.68, ...}
```

**陷阱**：傳 list of tuples 或 JSON 字串**不會**畫出長條圖，且規格明說會扣分。

## gr.HTML（Task 2 棋盤）

Gradio 沒有現成的 tile 元件，用 HTML 自己拼：

```python
def render_board(guesses, secret, attempts_left):
    colors = {"G": "#6aaa64", "Y": "#c9b458", "X": "#787c7e"}
    rows = []
    for g in guesses:
        score = score_guess(secret, g)
        tiles = "".join(
            f'<span style="display:inline-block;width:40px;height:40px;'
            f'background:{colors[s]};color:white;text-align:center;'
            f'line-height:40px;margin:2px;font-weight:bold;">{c.upper()}</span>'
            for c, s in zip(g, score)
        )
        rows.append(f"<div>{tiles}</div>")
    return "".join(rows) + f"<p>Attempts left: {attempts_left}</p>"
```

**陷阱**：用字母或符號（`T- R+ A+ C? E+`）標色**只拿一半分數**，必須是真實顏色。

## gr.Gallery + select 事件（Task 3）

```python
gallery = gr.Gallery(label="Gallery", allow_preview=False)
gallery.select(select_fn, None, status_box)   # 讀 gr.SelectData
```

**陷阱**：
- `select` 事件的參數是 `gr.SelectData`，索引在 `evt.index`
- 刪除後**必須清掉選取狀態**，否則下次刪除會刪錯圖（規格明說扣分）
- 空 gallery 要顯示訊息，不能是錯誤

## gr.Error / gr.Warning / gr.Info（全部任務）

| 元件 | 行為 | 適用 |
|------|------|------|
| `gr.Error` | 彈出錯誤並**中止**執行 | 未知單字、非整數輸入、長度錯誤的猜測 |
| `gr.Warning` | 彈出警告但**繼續**執行 | A 和 B 是同一字、可疑但允許的操作 |
| `gr.Info` | 彈出提示 | 操作成功通知 |

```python
raise gr.Error(f"'{word}' is not in the vocabulary.")   # 要 raise，不是呼叫
gr.Warning("A and B are the same word.")                # 不用 raise
```

## 滑桿即時更新（Task 5 Noise）

規格要求「移動滑桿就更新，不用按按鈕」：

```python
sigma_slider.change(noise_fn, inputs=[...], outputs=[...])
```

用 `.change()` 而非 `.release()`，才是拖動時即時更新。

## 通用 UI/UX 檢查清單

每個 app 送出前確認：

- [ ] 每個 input / output 都有 `label=`
- [ ] 有 `gr.Markdown` 說明怎麼用
- [ ] 有 `title=`
- [ ] 所有錯誤路徑都有 `gr.Error`，不會冒出 traceback
- [ ] 輸出是使用者看得懂的形式（不是 raw array / raw list / JSON）