# CIS341 Assignment 2 — 實作流程圖（ipynb）

> 對應規格：[CIS341-Assignment2-2627.md](./CIS341-Assignment2-2627.md)
> 繳交物：**一個**已執行、含輸出的 `.ipynb`，三個部分依序排列。

---

## 0. 總覽：一次編碼，三處重用

本作業的關鍵結構是「**編碼只做一次，之後全部是矩陣運算**」。Part 1 算出的影像向量，被 Part 2 與 Part 3 直接載入重用。

```mermaid
flowchart TD
    S["Setup<br/>GPU runtime + 掛載 Drive"] --> U["解壓 ZIP 到 /content<br/>（不要直接從 Drive 讀圖）"]
    U --> B["掃描資料夾 → 120 個犬種名稱<br/>去除 n0xxxxxxx- 前綴、底線換空白"]
    B --> M["載入 CLIP ViT-B/32<br/>+ preprocess"]
    M --> T["編碼 120 個 prompt<br/>文字向量 (120 × 512) 已 L2 正規化"]
    M --> I["編碼全部 20,580 張照片<br/>影像向量 (20580 × 512)"]
    I --> C1["快取 image_vecs_all.npz + paths<br/>存到 Drive"]
    I --> SUB["依 subset_list.txt 篩出 1,440 張<br/>向量 + 真實犬種標籤"]
    SUB --> C2["快取 subset_vecs.npz + labels<br/>存到 Drive"]

    T --> P1["Part 1 零樣本分類 (60)"]
    C1 --> P1
    P1 --> P2["Part 2 圖像檢索 (20)"]
    C2 --> P2
    C2 --> P3["Part 3 分群 (20)"]

    P1 -.->|"選定的 prompt 與介面截圖"| P2
    P2 -.->|"同一套向量，不重新編碼"| P3

    style C1 fill:#e8f4ff,stroke:#3178c6
    style C2 fill:#e8f4ff,stroke:#3178c6
    style P1 fill:#fff4e5,stroke:#d97706
    style P2 fill:#f0fff4,stroke:#059669
    style P3 fill:#fdf2ff,stroke:#9333ea
```

**為什麼要快取**：Colab 隨時會斷線。重跑一次 20,580 張的編碼是本作業最貴的操作，而它的結果在三個部分都只是唯讀輸入。

---

## 1. Part 1：零樣本分類（60 分）

```mermaid
flowchart TD
    A["Step 1.1<br/>從資料夾名稱建立 120 個可讀犬種名稱"] --> A2{"位置 i 的犬種<br/>是否等於 label i？"}
    A2 -->|"否"| A3["修正排序<br/>（否則所有準確率都是錯的，且不會報錯）"]
    A3 --> A2
    A2 -->|"是"| A4["印出並排檢查<br/>folder name ↔ breed name"]

    A4 --> B1["Step 1.2<br/>選一個模板：a photo of a BREED."]
    B1 --> B2["套用到全部 120 個犬種<br/>→ prompts_A (120 句)"]
    B2 --> B3["編碼 prompts_A<br/>→ text_vecs_A (120 × 512)"]

    B3 --> C1["Step 1.3<br/>predict_breed(image_path, k=5)"]
    C1 --> C2["開圖 → RGB → preprocess<br/>→ image encoder → L2 正規化"]
    C2 --> C3["相似度 = 影像向量 @ text_vecs_A.T<br/>（長度皆為 1，內積即 cosine）"]
    C3 --> C4["排序 → top-k<br/>回傳 [(breed, score), ...]"]
    C4 --> C5["三張照片驗證<br/>標示 top-1 / top-5 是否正確"]

    C5 --> D1["Step 1.4<br/>Gradio：上傳照片 → gr.Label 顯示 top-5"]

    C5 --> E1["Step 1.5<br/>全資料集評估"]
    E1 --> E2["logits = image_vecs_all @ text_vecs_A.T"]
    E2 --> E3["top1_acc / top5_acc<br/>macro F1（zero_division=0）"]

    E3 --> F1["Step 1.6<br/>第二個模板 → prompts_B → text_vecs_B"]
    F1 --> F2["重跑 E1~E3<br/>→ 兩組 prompt 的比較表"]
    F2 --> F3["選定最終模板"]

    F3 -.->|"必須在選定之後才截圖"| D1
    D1 --> D2["截圖 3 張資料集外的狗<br/>+ 1 張不是狗的照片"]
    D2 --> D3["說明非狗照片的結果與原因"]

    style A2 fill:#fff4e5,stroke:#d97706
    style F3 fill:#e8f4ff,stroke:#3178c6
    style D2 fill:#f0fff4,stroke:#059669
```

### 1.1 `predict_breed` 內部資料流

```mermaid
flowchart LR
    IMG["image_path"] --> OPEN["PIL.open()"]
    OPEN --> RGB["convert('RGB')<br/>（處理灰階 / RGBA / CMYK）"]
    RGB --> PRE["clip preprocess<br/>resize 224 + center crop + normalize"]
    PRE --> ENC["model.encode_image()"]
    ENC --> FEAT["float32 向量"]
    FEAT --> NORM["F.normalize(dim=-1)"]
    NORM --> DOT["@ text_vecs.T  →  (120,)"]
    DOT --> TOPK["torch.topk(k)"]
    TOPK --> OUT["[(breed, score), ...]"]
```

### 1.2 三個容易扣分的點

| 風險 | 後果 | 對策 |
| --- | --- | --- |
| 犬種清單順序與 `label` 不一致 | 全部準確率錯誤，且**沒有任何錯誤訊息** | 用 `assert` + 並排列印驗證 |
| 用子集跑出數字就交 | 1.5 該步驟 0 分 | 最終數字必須跑滿 20,580 張 |
| 1.4 截圖在 1.6 選模板之前拍 | 截圖與最終 prompt 不符 | 先完成 1.6 選定，再回頭截圖 |
| 沒有處理非 RGB 圖 | 1.3 扣 2 分 | `convert("RGB")` 一律先做 |

---

## 2. Part 2：圖像檢索（20 分）

```mermaid
flowchart TD
    A["載入 subset_vecs.npz<br/>1,440 × 512 + 檔案路徑 + 真實犬種"] --> B["Step 2.1<br/>find_similar(image_path, k=5)"]
    B --> B1["以 Step 1.3 相同方式編碼查詢照片"]
    B1 --> B2["scores = q_vec @ subset_vecs.T"]
    B2 --> B3["top-k → [(path, breed, score), ...]"]
    B3 --> B4["展示一張查詢<br/>顯示最近照片 + 犬種 + 分數"]

    B3 --> C1["Step 2.2<br/>Gradio 檢索介面"]
    C1 --> C2["輸入：gr.Image 上傳 + gr.Slider(k)"]
    C2 --> C3["輸出 1：gr.Label ← predict_breed<br/>（Part 1 選定的 prompt）"]
    C2 --> C4["輸出 2：gr.Gallery ← find_similar<br/>caption = 真實犬種"]
    C3 --> D1["Step 2.3<br/>3 張狗照片 × 2 個 k 值<br/>= 6 張截圖"]
    C4 --> D1
    D1 --> D2["每張截圖下方 1–2 句<br/>檢索結果與預測犬種是否一致"]
    D2 --> D3{"不一致？"}
    D3 -->|"是"| D4["改看最近照片共享了什麼<br/>姿勢 / 毛色 / 背景"]
    D3 -->|"否"| D5["紀錄：文字路線與圖像路線同答案"]

    style C3 fill:#fff4e5,stroke:#d97706
    style C4 fill:#f0fff4,stroke:#059669
```

---

## 3. Part 3：分群（20 分）

```mermaid
flowchart TD
    A["載入 subset_vecs.npz<br/>（已 L2 正規化，故 k-means 等價於 cosine 分群）"] --> B["Step 3.1<br/>build_clusters(n_clusters)"]
    B --> B1["KMeans(n_clusters=10,<br/>random_state=341, n_init=10)"]
    B1 --> B2["fit_predict → labels"]
    B2 --> B3["np.bincount → 各群照片數"]
    B1 --> B4["transform → 每張照片到每個群中心的距離"]
    B4 --> B5["每群取代表：<br/>只在自己群的成員中，找離自己群中心最近的"]
    B3 --> B6["回傳 sizes + representatives + labels"]
    B5 --> B6
    B6 --> B7["展示 10 群的 sizes 與代表照片"]

    B6 --> C1["Step 3.2<br/>三欄 Gradio 介面"]
    C1 --> C2["左：gr.Slider(10–50) + 按鈕"]
    C1 --> C3["中：gr.Gallery 代表照片<br/>caption = 群號 + 張數"]
    C1 --> C4["右：gr.Gallery 該群全部照片"]
    C3 --> C5["select 事件<br/>gr.SelectData.index → gr.State 取目前分群"]
    C5 --> C4
    C3 --> C6["allow_preview=False<br/>（點擊＝選取，不是放大）"]

    C5 --> D1["Step 3.3<br/>兩種設定（如 10 / 40 群）各開一群截圖"]
    D1 --> D2["描述主要群組：<br/>大小 / 相似性 / 凝聚因素"]
    D2 --> D3["只描述看到的外觀（毛色、姿勢、場景、人）<br/>不點名犬種"]

    style C5 fill:#e8f4ff,stroke:#3178c6
    style C6 fill:#fdf2ff,stroke:#9333ea
    style D3 fill:#fff4e5,stroke:#d97706
```

### 3.1 群組代表選擇的邏輯

```mermaid
flowchart LR
    D["dist = KMeans.transform(vectors)<br/>shape (1440, n_clusters)"] --> L["labels = kmeans.labels_"]
    L --> G["for g in range(n_clusters):"]
    G --> M["mask = labels == g"]
    M --> P["候選 = dist[mask, g]"]
    P --> A["argmin → 該群中離群中心最近的成員"]
    A --> R["representative[g] = subset_paths[mask][argmin]"]
```

> 只在自己群的成員中比較，是因為「全域最近群中心的照片」有時屬於別的群。

---

## 4. Notebook cell 順序建議

| # | 類型 | 內容 | 對應 |
| --- | --- | --- | --- |
| 1 | md | 標題、模型名稱、AI 揭露聲明摘要 | — |
| 2 | code | 掛載 Drive、解壓、列出資料夾數量 | Setup |
| 3 | code | 載入 CLIP、定義 `preprocess` / `encode_image` / `encode_text` | Setup |
| 4 | code | 編碼全部照片 + 存 `.npz`（含「已存在則載入」分支） | 共用 |
| 5 | code | 建立 subset 向量與標籤 | 共用 |
| 6 | md | `## Part 1: Zero-shot classification (60 marks)` + Must 清單 | 1 |
| 7 | code | 建立犬種清單 + `assert` 對齊檢查 | 1.1 |
| 8 | code | 模板 A → `prompts_A` → `text_vecs_A` + 印範例 | 1.2 |
| 9 | code | `predict_breed` 函式 | 1.3 |
| 10 | code | 三張照片測試（top-1 / top-5 標示） | 1.3 |
| 11 | code | 全資料集評估 Ａ（top-1 / top-5 / macro F1） | 1.5 |
| 12 | code | 模板 B → 評估 Ｂ → 比較表 → 選定 | 1.6 |
| 13 | code | Gradio 犬種介面（呼叫 `predict_breed`） | 1.4 |
| 14 | md | 截圖：3 張狗 + 1 張非狗 + 文字解釋 | 1.4 |
| 15 | md | `## Part 2: Image retrieval (20 marks)` | 2 |
| 16 | code | `find_similar` + 一張查詢結果展示 | 2.1 |
| 17 | code | Gradio 檢索介面（Image + Slider → Label + Gallery） | 2.2 |
| 18 | md | 截圖：3 照片 × 2 k 值，每張一句評論 | 2.3 |
| 19 | md | `## Part 3: Clustering (20 marks)` | 3 |
| 20 | code | `build_clusters(n)` + 10 群 sizes / 代表照片 | 3.1 |
| 21 | code | Gradio 三欄探索器（Row / Column / State / SelectData） | 3.2 |
| 22 | md | 截圖：兩種設定各開一群 + 主要群組描述 | 3.3 |
| 23 | md | AI 揭露（逐部分）、資料來源、引用 | — |

> ⚠️ cell 13 的介面依賴 cell 12 選定的模板，但截圖放在 cell 14 —— 這個「先跑、後截圖」的順序不要顛倒。

---

## 5. 快取檔案規格

| 檔案 | 內容 | shape | 用途 |
| --- | --- | --- | --- |
| `all_vecs.npz` | `vectors`, `paths` | `(20580, 512)`, `(20580,)` | 1.5 全量評估 |
| `subset_vecs.npz` | `vectors`, `paths`, `breeds` | `(1440, 512)` | 2.1、3.1 |
| `text_vecs_A.npy` | 模板 A 的 120 個向量 | `(120, 512)` | 1.3–1.5 |
| `text_vecs_B.npy` | 模板 B 的 120 個向量 | `(120, 512)` | 1.6 |

全部以 `float32` 儲存；向量一律先 `F.normalize(..., dim=-1)` 再存，事後就不必再正規化。

---

## 6. 全作業檢查清單

- [ ] 三個 Gradio 介面都有**實際跑起來**的截圖（不是 mockup）
- [ ] 1.5 的數字跑滿 20,580 張，不是示範用子集
- [ ] 兩組 prompt 的 top-1 / top-5 / macro F1 在同一張表
- [ ] 1.6 有「為什麼 prompt 不同結果不同」的自述解釋（提到訓練資料文字、歧義犬種名）
- [ ] 2.3 共 6 張截圖，每張都有評論
- [ ] 3.3 有兩組設定的截圖，且描述**不點名犬種**
- [ ] 三個部分都各自寫了 AI 揭露（工具 + 具體問題 + 是否驗證有效）
- [ ] 截圖貼在**建立該介面的 cell 旁**
- [ ] Moodle 狀態為 `Submitted for grading`（不是草稿）