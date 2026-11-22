# 要不要重錄？怎麼錄？— 螢幕錄影決策與腳本

- **建立日期**：2026-11-20
- **死線**：2026-11-22 23:59 HKT
- **現有檔案**：`recordings/screen-recording.mp4`（7 分 22.5 秒、1920×1080、60 fps、37.4 MB、含音軌）

> **如果你要的是「不用背稿、不用讀長句、不用做 PPT 怎麼錄」，直接看
> [RECORDING-CUE-CARDS.md](./RECORDING-CUE-CARDS.md)。**
> 本文件說明為什麼要重錄與工具設定；逐句台詞與發音提示在提示卡那份。

---

## 一、結論：要重錄，而且這不是「加分」問題，是「扣分還在」的問題

### 1. 唯一被點名「錄影與筆記本矛盾」的那一項，只修了筆記本那一邊

評語原文（Justification，−2%）：

> At about **4:36–4:54**, the recording calls the separation after epoch 8 overfitting.
> Your notebook instead says there is no divergence, and validation recovers after the jumps.
> Please **resolve these conflicting explanations** using both loss and accuracy, with the actual epochs and values.

我們這次把 notebook 改對了（6.3 重寫 + 6.3b 受控實驗），但錄影**沒有改**。我實際抽幀確認，
錄影第 9 頁（約 5:00）仍然寫著：

> `scratch_cnn · lines separate after epoch 8 → overfitting, early stop at 14`

而現在的 notebook 明說「不是過擬合、也不是抽樣噪音，是 1e-3 步長下的暫時擺盪，
最佳 val_loss 在 e17、e23 才停」。也就是說：**改之前是「錄影 vs notebook 矛盾」，
改之後是「錄影 vs notebook 更嚴重地矛盾」**——因為 notebook 現在還額外寫了
「舊解釋已被 6.3b 推翻」。評分老師只要再看一次 4:36 那段，同一筆 −2% 會再扣一次。

### 2. 錄影上有一批數字，已經和提交的輸出不一樣（實測比對）

| 錄影上講的 | 現在 notebook 的實測 | 位置 |
|---|---|---|
| `scratch_cnn` val **0.811** | **0.8179** | 6.5 |
| separation after epoch 8、**early stop at 14** | best val_loss **0.5009 @ e17**，**e23 才停** | 6.2 / 6.3 |
| BN 變體 **train 0.809 / val 0.346** | **0.810 / 0.271**（val_loss 3.403） | 6.4.2 |
| 移除 BN 後 **0.800** | **0.807** | 6.4.2 |
| moving_variance **3.3–6.8×** 過大 | **5.78 / 5.93 / 4.98 / 4.43** | 6.4.2 |
| 每 epoch **35 次**更新 | **35 次**（這條沒變，可保留） | 6.4.2 |
| 增強 **0.789 → 0.861** | **0.804 → 0.886**（旋轉已改 ±14.4°） | 6.4.3 |
| `mobilenet_v2` best loss 在 **e20**、「預算不夠」 | 共 **17 epochs**，best val_loss **0.1871 @ e11** | 6.2 |
| 六類 **0.922 / macro F1 0.918** | **0.9314 / 0.926** | 9.3 |
| 部署比較 **0.914 vs 0.811** | **0.9393 vs 0.8179** | 6.6 |

評分規格附錄 A 對論證分的說明是：「沒有解讀的圖表、未經測試的建議修正，或**與輸出矛盾的說法**，
都會失去論證分數。」這十條全部落在那一句話的射程內。

### 3. 這一版修訂的內容，錄影一個字都沒提到

新增的 2.4b、3.4b、4.1b、6.3b、6.4.1（實際預測）、7.3、8.2b、8.3b、8.4b、9.3，
全部是這次修訂的實質內容。作業要求錄影要講「訓練超參數、驗證損失／準確率、曲線解讀與模型比較」，
而錄影是唯一會讓老師「聽到」你怎麼讀曲線的地方。目前那一分鐘讀錯的內容，正好是 15 分的 Justification。

### 4. 現有錄影的合規風險（不是美感問題）

- **畫面右下角的 cideo.com 水印**：你已說明那是把 9 分多鐘的成品放進線上工具
  **加速 1.25×** 壓到 7:22 造成的，旁白確實是你本人。所以它不是「合成音」問題，
  但仍然留下三個實際風險：
  1. 老師看到第三方網站水印，**第一反應就是懷疑這支影片被工具處理過**。作業要求
     「由你本人以英語旁白的螢幕錄影」，一旦要先自證，就已經是失分的位置。
  2. 1.25× 會同時把**音高拉高大約 4 個半音**。人聲加速後音色會變得偏薄、偏尖，
     聽起來反而不像自然講話——這恰恰是「像合成音」的成因。
  3. 原本 9 分多鐘這個事實本身說明**內容超預算**。加速只是把超長藏起來，
     沒有解決「講太多、示範太少」的結構問題。而這支影片的實際操作只有約 15 秒，
     加速後更壓縮到只剩十幾秒，反而讓「示範一次真實預測」這一條更不合格。
- 整支 7 分 22 秒裡，**實際操作介面只有約 15 秒**（我掃描整支影片的畫面白度，
  只有 6:20–6:35 那段不是簡報）。作業寫「在錄影中示範一次真實預測」，
  評分規格寫「示範各類別的實際預測，附上可讀的輸入與預期／實際答案。
  **僅啟動介面並不能證明預測可用。**」
- 滑桿是舊的 1–3 秒版。第 2 項扣分（−1.5%）講的就是那個控制，
  老師在錄影上看到的還是沒修的樣子。

### 5. 時間夠

現在是 11/20 21:25，死線 11/22 23:59，還有約 2 天。重錄本身的成本是
**排練 1 次 + 錄 2–3 個 take + 剪接 ≈ 2 小時**，不含準備。這個投入換回一個
2 分的爭議項與十條矛盾的數字，值得。

### 6. 如果堅持不重錄，最起碼要做的事

（我建議不要走這條，但如果時間真的不夠）在 notebook 6.3 開頭加一句明確的
「本節結論取代先前口頭說明」的聲明，並在 `REVISION-CHANGES.md` 的 C 節改成
「未重錄，衝突已在 notebook 內解決」。這樣做的風險是：老師的評語是
「resolve these conflicting explanations」，他預期的是兩邊一致，不是「宣告舊的那邊作廢」。
最樂觀也只會拿回部分分數，而那十條過期數字不會因為任何宣告而變成正確。

---

## 二、怎麼錄（工具與設定）

### 器材

| 項目 | 建議 | 理由 |
|---|---|---|
| 錄影軟體 | **OBS Studio** | 作業明文指定「請使用 OBS，或在你自己的電腦上錄製 Teams 會議」 |
| 解析度 | **1920×1080，30 fps** | 1080p 已經是上限；30 fps 足夠，60 fps 只會讓檔案大一倍 |
| 編碼 | x264，**CQP 22–24**，preset veryfast | 文字要銳利；CQP 固定品質比 CBR 省空間 |
| 音訊 | 麥克風單聲道 48 kHz，AAC 128–160 kbps | 語音不需要立體聲 |
| 音量 | 講話峰值 −12 到 −6 dB，底噪低於 −50 dB | 作業要求「聲音清楚」 |
| 檔案大小 | 目標 < 200 MB | 太大了老師不方便；仍可在 OneDrive 給連結 |

> 不要用簡報轉影片服務（cideo 那類）。要的是「螢幕錄影 + 你本人旁白」。
> **也不要為了趕時間去加速。** 縮短長度的正確做法是少講幾句，不是把聲音拉快。

### 畫面準備（開錄前 20 分鐘做完）

1. **關掉通知**：Windows 設定 → 系統 → 焦點輔助 → 僅鬧鐘。關掉 Teams／Discord／LINE。
2. **關掉不相關的視窗與瀏覽器分頁**；書籤列隱藏（Ctrl+Shift+B）。
3. **VS Code 字級放大**：`Ctrl` + `=` 按 2–3 次，讓 1080p 下數字可讀。
   Notebook 的輸出表格尤其要確認「0.8179」這種小數點看得清楚。
4. **先啟動三個 Gradio 應用**（開錄前就要跑起來，不要讓老師看你等載入）：
   - 影像介面：`http://127.0.0.1:7871/`
   - 主要天氣影片介面：`http://127.0.0.1:7862/`
   - 天氣變化介面：`http://127.0.0.1:7863/`
   （填好表單、選好影片、滑桿先歸位，但**不要按下送出**——留給錄影時按。）
5. **預先想好「要按哪裡」**：錄影最花時間的是找 cell。記下每段的 cell 編號（本文件腳本已列）。
6. **手機／碼錶在旁邊**，每段結束看一次秒數。

### 錄法：一段一段錄

**不要用「三個 take」，改用 14 張提示卡，一張一段、分開錄。**
逐段提示卡在 [RECORDING-CUE-CARDS.md](./RECORDING-CUE-CARDS.md)，
每句只有 6–12 個字、附中文意思與難字發音，講壞了只重錄那一張。

- 分開錄完全合規：作業原文「**你可以剪掉等待時間，但須標明**」。
- **標明方式用「轉場 + 畫面標籤」，不要每段講一句話。**
  規格要求標明的是「已儲存的結果」與「重播的片段」，轉場只表達「跳過了」，
  標籤才表達「這段是預先跑好的」。
  - 每個剪接點：0.3–0.5 秒淡化或黑場。
  - 已存好的輸出：右下角常駐 `pre-executed output`；重播標 `replay`；現場操作標 `live`。
  - 只在第一次剪接講一句 `"I'm cutting the waiting time. From here on, everything is pre-executed output."`，
    之後全靠標籤，省約 25 秒。
  - **不要把 replay 標成 live**；也不要只加轉場不加標籤。
  - 標籤不必好看：規格第 316 行明說不為剪輯精緻度給分。
- **不要再用線上工具加速。** 現有影片的 cideo.com 水印與偏尖的音色就是 1.25× 造成的；
  新做法目標 7:00–7:25，正常語速，不需要任何後製加速。

---

## 三、逐段腳本（目標 7 分 10 秒，硬上限 7 分 30 秒）

> 英文旁白請照讀或照著講，句子刻意寫短、寫口語。中文是給你理解用的。

### 0:00–0:15｜開場（15 秒）

- **畫面**：notebook 標題 cell（cell 0）。
- **旁白**：
  > "This is CIS341 Project 1, weather classification. Four classes — sunny, overcast, rainy and snowy — and a six-class extension. I'll go through the data, the two models, what the training curves actually say, and then run the interfaces live."

### 0:15–0:50｜資料（35 秒）

- **畫面**：cell 12 的類別計數表、cell 13 的 duplicate summary。
- **旁白**：
  > "Four classes, one thousand four hundred seventy-nine files collected. Sunny three hundred forty-one, overcast three hundred fourteen, rainy two hundred eighty-seven, snowy five hundred thirty-seven. After duplicate detection removes seventy-four copies, one thousand four hundred five distinct originals remain — three hundred fifteen, two hundred ninety-two, two hundred sixty-one and five hundred thirty-seven — so every class clears the two-hundred-and-fifty minimum on distinct originals, not on raw files."
  > "Sources are recorded per image. The split is one thousand one hundred twenty-five training and two hundred eighty validation, grouped so near-duplicates never straddle the split."

- **可以坦白的一句（加分的自我認識）**：
  > "One known weakness: sunny and overcast are mostly sky-dominated shots, while rainy and snowy are mostly street-level. So high validation accuracy does not mean it generalises to new scenes. I'll come back to that."

### 0:50–1:30｜前處理與增強（40 秒）

- **畫面**：cell 31（4.1b 旋轉換算）、cell 35（並列預覽）、cell 27（3.4b 路徑量測）。
- **旁白**：
  > "Preprocessing is applied exactly once, and in one place. Scratch model: resize to 128, divide by 255. Transfer model: resize to 224, mobilenet's own preprocess_input."
  > "The rotation argument is a fraction of a full turn, so the first version's 0.15 was fifty-four degrees — not a small handheld tilt. That put 44 percent of samples past thirty degrees. It's now 0.04, which is fourteen point four degrees, with nothing past thirty."
  > "Same-image check: the training loader and the inference path now produce bit-identical tensors, maximum difference 0.0. The old PIL path did not — that was a real bug, and section 3.4b measures it."

### 1:30–1:55｜兩個模型（25 秒）

- **畫面**：cell 45 的參數量比較表。
- **旁白**：
  > "Two designs. Scratch: four convolution blocks, global average pooling, dropout 0.4, one dense layer — two hundred fifty-seven thousand parameters, all trainable."
  > "Transfer: frozen MobileNetV2 backbone plus a small head — five thousand one hundred and twenty-four trainable parameters, zero point two percent. That hundred-percent versus zero-point-two contrast is the comparison."

### 1:55–3:05｜訓練與曲線（70 秒，**最重要的一段**）

- **畫面**：cell 51（training log / history）、cell 53 的曲線圖、cell 52 的 log。
- **旁白**：
  > "Seed 341, Adam at one-e-three, batch thirty-two, sparse categorical cross-entropy, early stopping after six epochs on validation loss."
  > "Scratch model: twenty-three epochs. Best validation loss is zero point five zero zero nine at epoch 17, and training stops at epoch 23. Final training accuracy 0.850, validation 0.804 — a gap of plus 0.046, about thirteen images. That's mild, not runaway."
  > "It is not overfitting at epoch 8, which is what the previous narration said. Here is the actual correction." ← **這句必須有**

- **畫面**：切到 cell 55/56（6.3b 的表）。
- **旁白**：
  > "I retested the jumps with three runs that differ only in learning rate: one-e-three with the plateau schedule, one-e-three constant, and three-e-four constant. Everything else identical."
  > "The schedule is not the cause — the first two runs jump at the same epochs, and the plateau doesn't act until epoch 12. A smaller learning rate only shrinks the jumps: three-e-four has seventy percent of the amplitude, but still jumps."
  > "It is not sampling noise. I recomputed validation loss every epoch on two disjoint halves of the validation set. Twelve jumps, and all twelve raised the loss on both halves at once. Resampled noise cannot do that."
  > "In ten of the twelve the training loss fell while validation rose, so it's a temporary oscillation, and early stopping picks epoch 12, 9 and 17 — none of them straight after a jump."

- **畫面**：cell 68（6.5 兩模型評估）。
- **旁白**：
  > "Transfer model: seventeen epochs, best validation loss zero point one eight seven one at epoch 11, validation accuracy zero point nine three nine three, macro F1 zero point nine three four. That's the model I deploy."

### 3:05–4:00｜除錯三項（55 秒）

- **畫面**：cell 60 的兩張表 + cell 61 的輸出（6.4.1）；cell 63 的表（6.4.2）；cell 65（6.4.3）。
- **旁白**：
  > "Three controlled investigations, one factor each, same 280 validation images."
  > "Preprocessing twice. I rebuilt the earlier network — with the scaling layer inside the model and batch norm after every convolution — and ran it. All two hundred eighty validation images were predicted overcast. Accuracy zero point two zero seven one, which is worse than always guessing snowy at zero point three eight two one. Every image's top probability is between zero point four zero one and zero point four zero four — the model saw two hundred eighty identical inputs. Fixing it: zero point eight one seven nine, four classes."
  > "Only one of those two defects collapses the model. Double scaling alone gives zero point five one seven nine with all four classes. Both together collapse it."
  > "Batch norm. Training 0.810, validation 0.271. The stored moving variance is four to six times the measured batch variance, because there are only thirty-five updates per epoch and momentum is 0.99. Remove it and validation goes to 0.807."
  > "Augmentation. I reduced the rotation first — that helped, 0.789 to 0.804 — but switching augmentation off gave 0.886 against 0.804. So on this dataset, with a four-layer model, augmentation didn't pay. I'm not claiming augmentation is useless in general."

### 4:00–4:25｜部署選擇（25 秒）

- **畫面**：cell 70 的比較表。
- **旁白**：
  > "Deployment: transfer, zero point nine three nine three against zero point eight one seven nine, and far less training time. It's used by the image interface and by every video function."

### 4:25–5:10｜影像介面（45 秒）

- **畫面**：切到 `127.0.0.1:7871`（先開好），現場做一次預測：拖入一張**驗證集**的圖（不要用訓練圖）。
- **操作**：拖圖 → 送出 → 指 `gr.Label` 的四個機率。
- **旁白**：
  > "This is the deployed model on a validation image — not a training image. Top class [read it], [read the probability]. All four probabilities are shown, and the class order is the same everywhere: sunny, overcast, rainy, snowy."
  > "Section 7.2 saves one test per class with the expected and the actual label, and marks whether each image is training, validation or new."

### 5:10–6:20｜影片介面（70 秒，**第二重要**）

- **畫面**：切到 `127.0.0.1:7862`（主要天氣）。先示範**被拒絕的間隔**，再示範正常的。
- **操作**：滑桿拉到 1.0 → 送出（等它跑完）→ 顯示取樣幀拼圖與機率表。再把滑桿拉到 0.5 送出。
- **旁白**：
  > "The main-weather interface. The interval control takes 0.25 to 1.0 seconds — the specification says at least once per second, so the gap must never exceed one second. Anything above 1.0, or zero, is rejected with an error, and anything at or below 1.0 is accepted."
  > "On the sunny clip: nine frames, one second apart, and the mean is snowy 0.4368 against sunny 0.3150, so it reports snowy."

- **畫面**：指拼圖與切帶結果（notebook 8.1）。
- **旁白**：
  > "That's the sampled frames the model actually saw. My first guess was that it reads the lower half, but the bottom sixty percent on its own is rainy 0.7459 — not snowy. The top forty percent is a draw between sunny and snowy. Neither half produces snowy."
  > "What produces it is one thin dark strip. Remove the tree line between sky and water and snowy jumps from 0.4368 to 0.7709. So the decision is composition-driven, and the blue sky is only seventeen to twenty-three percent of the frame."

- **畫面**：切到 `127.0.0.1:7863`（變天介面），跑 `video2.mp4`，顯示回傳的**標註影片**與時間軸。
- **旁白**：
  > "The changing-weather interface returns the annotated video next to the timeline, so predictions can be checked against the scene. Thirty-nine sampling points on this clip, and overcast never wins one. Keeping only the sky raises overcast twenty-seven times — so it sees the grey sky, but eleven of those twelve sky crops come back as snowy. The ground then outvotes it, at a mean of 0.99 for rainy."

### 6:20–6:55｜六類（35 秒）

- **畫面**：cell 98、cell 100 的混淆矩陣。
- **旁白**：
  > "Six classes adds foggy and lightning — nine hundred fifteen and three hundred nine images, so two thousand six hundred twenty-nine distinct in total. Validation accuracy zero point nine three one four, macro F1 zero point nine two six on five hundred twenty-five images."
  > "That is not better than four-class; the split is different and the new classes are easier. Thirty-six errors, and seventeen of them are pushed into foggy. That's where the confusion actually is."

### 6:55–7:10｜AI 使用與收尾（15 秒）

- **畫面**：cell 3（AI 使用聲明）。
- **旁白**：
  > "I used GitHub Copilot agent mode. It drafted the library code, the plots and the investigation probes. I chose the experiments, ran every cell, checked every number against the output, and rejected several of its proposals — batch norm everywhere, lowering the momentum, deleting the preprocessing hook, and claims that augmentation is harmful. All four rejections are shown with the measurement that refuted them in 6.4. That's it."

---

## 四、必須說 / 不可以說

### 必須說（對應作業六點與評分規格）

1. 資料來源與每類張數（✓ 0:15 段）
2. 增強與資料準備 + 預覽（✓ 0:50 段）
3. 兩個模型的設計原則（✓ 1:30 段）
4. 訓練超參數、驗證損失／準確率、**曲線解讀**、模型比較（✓ 1:55 段最長，值得）
5. 介面設計 + **一次真實預測**，然後影片結果（✓ 4:25 與 5:10 段，必須真的操作）
6. 六類延伸（✓ 6:20 段）
7. AI 工具、你請它做什麼、**測試後是否有效**、採用了什麼、拒絕了什麼（✓ 6:55 段）

### 不可以說（會直接掉分）

| 不要說 | 因為 |
|---|---|
| "lines separate after epoch 8 → overfitting" | 這是修訂前的錯誤解讀，正是被扣 2 分的那句 |
| "early stop at 14" | 實際是 e23 才停，最佳在 e17 |
| "val 0.811 / 0.346 / 0.800 / 3.3–6.8× / 0.789→0.861" | 全部是舊數字 |
| "mobilenet loss still falling at epoch 20" | 現在只有 17 epochs |
| "six-class 0.922 / 0.918" | 0.9314 / 0.926 |
| "the model works well on new scenes" | 獨立 benchmark 只有 0.5/15，這樣說等於自打臉 |
| "augmentation is useless" | 6.4.3 明列三個不能下這個結論的理由 |
| "the collapse is still happening" | 已修好，現在塌陷只出現在重建的對照模型裡 |
| "sampling noise explains the jumps" | 這正是被 6.3b 推翻的舊解釋 |
| 任何「大概／可能／應該是」的因果推測 | 規格要求「未經測試的建議修正」會失分 |

### 兩個語言上的小提醒

- 類別名固定念 `sunny / overcast / rainy / snowy`（六類加 `foggy / lightning`），
  與 `class_order.json` 一致，不要念中文。
- 數字念法保持一致：`zero point eight one seven nine` 或 `point eight one eight`，同一個數字前後不要兩種念法。

---

## 五、錄完之後的檢查清單

- [ ] 長度 ≤ **7:30**（硬上限，含六類示範）
- [ ] 旁白是**你本人**的聲音，英文，沒有合成音、沒有浮水印
- [ ] 畫面中所有數字都在 notebook 執行輸出裡找得到（至少抽查 0.8179、0.9393、0.2071、0.271/0.807、0.804/0.886）
- [ ] 真的有操作介面一次（拖圖 → 送出 → 讀 `gr.Label`），不是只開著
- [ ] 有示範**被拒絕的間隔值**（顯示 `gr.Error`）與**被接受的**值
- [ ] 兩支變天影片都跑過（`video2.mp4` 與 `common-changing-weather.mp4`）
- [ ] 變天介面有顯示**回傳的標註影片**與時間軸
- [ ] 每個剪接處都有轉場，且已存好的輸出有 `pre-executed output` 標籤
- [ ] 檔案 < 200 MB；太大就轉檔或給 OneDrive 連結
- [ ] 檔名沿用 `recordings/screen-recording.mp4`（覆蓋舊檔），或改成 `screen-recording-v2.mp4` 並同步更新 `dist/README.txt` 與 `REVISION-CHANGES.md` C 節

---

## 六、時程建議（今晚到死線）

| 時間 | 做什麼 |
|---|---|
| 11/20 晚（30 分） | 讀完本文件、決定走重錄路線；把三個 Gradio 應用與 OBS 設定好 |
| 11/21 上午（40 分） | 排練一次（不上麥、只看秒數），調整每段長度；把要對照的 cell 編號記在便條紙上 |
| 11/21 下午（60 分） | 錄 Take 1–3，剪接，檢查清單逐項打勾 |
| 11/21 晚（30 分） | 覆蓋 `recordings/`、更新 `dist/README.txt` 與 `REVISION-CHANGES.md` C 節、重打包 zip |
| 11/22（緩衝） | 只剩上傳與 Moodle 確認「Submitted for grading」 |

> 上傳前務必確認 Moodle 顯示 **Submitted for grading**，並把 zip 與錄影的 OneDrive 連結
> 保留到評分與後續檢查結束。