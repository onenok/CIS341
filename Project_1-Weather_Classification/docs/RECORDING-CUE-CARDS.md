# 錄影提示卡：不用背稿、不用讀長句、不用做 PPT

- **建立日期**：2026-11-20
- **搭配文件**：[RECORDING-PLAN.md](./RECORDING-PLAN.md)（為什麼要重錄、工具設定）
- **先讀完這一頁再開 OBS**

---

## 〇、先解決你提出的三件事

你說的三個困難，其實只要換一個錄法就全部消失：

> ① 看英文腦袋來不及轉 ② 有些字不會讀 ③ 不知道要用什麼方式讀

| 你的困難 | 解法 | 為什麼有效 |
|---|---|---|
| 看不懂英文 | **每一句只有 6–12 個字，全部用最簡單的字寫**，下面附中文意思 | 你不是在讀文章，是在讀一句話 |
| 不會讀某些字 | 每個難字都給了**近似發音**（見第五節）；句子也刻意避開難字 | 沒把握的字直接不用 |
| 不知道怎麼「講」 | 改成**一句一句錄**：看一句 → 講一句 → 停 3 秒 → 看下一句 | 腦袋只需要裝一句，不用裝一段 |

還有一個關鍵事實你之前不知道：

> **作業沒有要求用 PowerPoint。**
> 原文（`CIS341-Project1-2627.zh-Hant.md` 第 206 行）：
> 「建議使用 PowerPoint 投影片，但**你也可以直接從 notebook 簡報**。」

所以最省力、也最不容易出錯的做法是：**直接從你的 notebook 講。**
理由是 notebook 裡的英文已經是你核對過的，數字也一定跟輸出相符——
你不需要再造一份英文簡報，也就不會有「簡報數字和 notebook 不一樣」這種事。

---

## 一、為什麼不要再加速（1.25×）

你之前那支是 9 分多鐘加速到 7:22。這次不要這樣做：

| 問題 | 說明 |
|---|---|
| 水印 | cideo.com 的字樣會一直留在畫面角落。老師第一眼看到第三方網站水印，就得先懷疑這支影片被工具處理過 |
| 音高 | 1.25× 會把人聲拉高大約 4 個半音，聲音變薄變尖——**這反而更像合成音** |
| 根本原因 | 原本 9 分鐘代表內容超預算。加速只是把超長藏起來，示範時間還是只有十幾秒 |

**這次的目標是 7 分 20 秒左右，正常語速，不做任何後製加速。**
下面的提示卡就是照這個長度設計的。

---

## 二、錄法：一段一段錄，最後接起來

作業允許剪接，原文（第 211 行）：「**你可以剪掉等待時間，但須標明**已儲存的結果與重播的片段。」

> **重要**：它要求標明的是「**已儲存的結果**」與「**重播的片段**」，**沒有**要求每個剪接點都講一句話。
> 所以用「轉場 + 畫面標籤」就合規，而且比講話省約 25 秒。詳見第三節。

### 步驟

0. **三支介面我已經啟動好，現在就能用**（見第九節，重開機後要再跑一次）。
1. **OBS 設定**照 [RECORDING-PLAN.md](./RECORDING-PLAN.md) 第二節（1080p / 30 fps / CQP 22）。
2. **手機打開本文件**（或印出來），放在鏡頭旁邊。螢幕上只放 notebook。
3. **一次只錄一張卡**，檔名 `01.mp4`、`02.mp4`……共 15 個檔。
4. 講壞了就**整張卡重錄**，不用從頭。
5. 每錄完一張，**立刻回放聽一次**（30 秒，不要省）。
6. 全部錄完，用下面的指令合併（`ffmpeg` 若沒有，先 `winget install Gyan.FFmpeg`）：

```powershell
cd "c:\Users\honok\Desktop\cis341\Project_1-Weather_Classification\_rec2"
"file '01.mp4'`nfile '02.mp4'`nfile '03.mp4'`nfile '04.mp4'`nfile '05.mp4'`nfile '06.mp4'`nfile '07.mp4'`nfile '08.mp4'`nfile '09.mp4'`nfile '10.mp4'`nfile '11.mp4'`nfile '12.mp4'`nfile '13.mp4'`nfile '14.mp4'`nfile '15.mp4'" | Out-File -Encoding ascii list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy ..\recordings\screen-recording.mp4
```

（`-c copy` 不重新編碼，所以合併只花幾秒，畫質不會掉。全部用同一組 OBS 設定錄就沒問題。）

---

## 三、講話的四個規則

1. **一句不超過 12 個字。** 超過就是句子太長，拆成兩句。
2. **講完一句停 1 秒。** 停頓可以剪掉，講太快不能補救。
3. **講錯不要道歉、不要重來。** 閉嘴 2 秒，然後把那句重講一次，剪掉前面失敗的。
4. **發音不完美沒關係。** 評分看的是內容與數字，不是口音。**不要為了發音漂亮而結巴**，講順比講對重要。

### 標明剪接：轉場 + 標籤，不是每段都要講話

> **你問過「加明顯轉場效果就夠嗎？」答案是：轉場 + 畫面標籤才夠，轉場單獨不夠。**
> 規格要的是「標明已儲存的結果與重播的片段」——轉場只表示「這裡跳過了」，
> 沒有表示「這段畫面是預先跑好的」。所以兩者要一起用。

#### 三個做法

1. **每個剪接點**：0.3–0.5 秒十字淡化或黑場。這是「有剪接」的訊號。
2. **畫面是已存好的輸出時**：右下角常駐一行小字（用 OBS 的「文字」來源，
   或在剪輯軟體加文字圖層）。這才是「標明」。
3. **只在第一次剪接講一句**，建立規則，之後全靠標籤：

> "I'm cutting the waiting time. From here on, everything is pre-executed output."

**這一句講完，後面 14 段都不用再講。** 省下約 25 秒。

#### 三個標籤（照抄，不要改字）

| 標籤文字 | 什麼時候出現 |
|---|---|
| `pre-executed output` | 畫面是 notebook 已存好的 cell 輸出 |
| `replay` | 重播剛才已經播過的片段，或播放你預先錄好的 Gradio 操作 |
| `live` | 現場按、現場跑的（卡 10–13 的 Gradio 操作） |

#### 哪一張卡掛哪個標籤（照這張表貼）

判斷原則：**標籤描述「畫面上的像素是哪來的」，不是描述「你有沒有在動滑鼠」。**
你在 notebook 裡滾動、點 cell 都是現場動作，但只要 cell 的輸出是先前跑好存下來的，
畫面就仍然是 `pre-executed output`。

| 卡 | 時間 | 畫面 | 標籤 |
|---|---|---|---|
| 1 | 0:00–0:20 | notebook 標題 + AI 聲明 | `pre-executed output` |
| 2 | 0:20–0:55 | 第 2 節資料來源表、張數表 | `pre-executed output` |
| 3 | 0:55–1:20 | 去重 summary + 分割 | `pre-executed output` |
| 4 | 1:20–1:55 | 第 3 節增強說明 + 預覽圖 | `pre-executed output` |
| 5 | 1:55–2:20 | 第 4 節模型設計 | `pre-executed output` |
| 6 | 2:20–2:50 | 第 5 節超參數表 | `pre-executed output` |
| 7 | 2:50–3:35 | 6.2 訓練曲線 + 6.5 比較表 | `pre-executed output` |
| 8 | 3:35–4:25 | 6.3 曲線解讀 + 6.3b 表 | `pre-executed output` |
| 9 | 4:25–5:00 | 6.4.1 / 6.4.2 / 6.4.3 | `pre-executed output` |
| 10 | 5:00–5:35 | 瀏覽器 7871 影像介面 | **`live`** |
| 11 | 5:35–6:15 | 上傳 + Submit + 分數 | **`live`** |
| 12 | 6:15–6:45 | 瀏覽器 7862 影片介面 | **`live`** |
| 13 | 6:45–7:00 | 瀏覽器 7863 變天介面 | **`live`** |
| 14 | 7:00–7:14 | 9.3 六類混淆矩陣 | `pre-executed output` |
| 15 | 7:14–7:22 | 6.6 部署選擇表 | `pre-executed output` |

**所以實際上只切兩次標籤**：卡 1 開始時掛 `pre-executed output`，
卡 10 開始時換成 `live`，卡 14 開始時換回 `pre-executed output`。
OBS 裡就是同一個文字來源改三次字，不用做 15 個圖層。

#### `replay` 什麼時候才會用到

只有一種情況：你決定**先把卡 10–13 的 Gradio 操作預錄一次**，
之後在正式錄影時播放那段預錄畫面。這時卡 10–13 就從 `live` 改成 `replay`。

這條路有代價：要說清楚是預錄的，而且不能把預錄講成現場。
好處是 Gradio 跑很久（影片分析要幾十秒）不會拖爆時間軸。
**如果你想走這條，先跟我說，我把卡 10–13 的稿改成 replay 版本。**

#### 兩條不能踩的線

- **不要把 replay 標成 live。** 這份作業已經因為「說法與輸出不一致」被扣分，
  這裡再被抓一次會很麻煩。
- **不要只用轉場不加標籤。** 老師只看到跳接，無法分辨你是「剪掉等待」
  還是「藏起失敗重跑」。

#### 好消息：標籤做得醜不扣分

規格第 316 行：「我們評估技術說明，不會為口音、使用網路攝影機、
**剪輯精緻度**或投影片設計單獨給分。」

所以白底黑字、不加動畫、不加音樂就好。**做得醜不扣分，做得不清楚才扣分。**

---

## 四、15 張提示卡

> **粗體 = 你要講的英文。** 英文下面的小字是中文意思。
> 每張卡的「只記一句」是萬一你緊張到全忘，講那一句就夠。

---

### 卡 1 ｜ 0:00–0:20 ｜ 畫面：notebook 最頂端（標題 + AI 使用聲明）

**畫面標籤：`pre-executed output`**

1. **This is my weather classification project.**
   （這是我的天氣分類專題。）
2. **I used GitHub Copilot. I checked the results myself.**
   （我用了 Copilot，結果我自己核對過。）
3. **The notebook below shows all the evidence.**
   （下面的 notebook 就是全部證據。）

**只記一句**：This is my weather classification project.

---

### 卡 2 ｜ 0:20–0:55 ｜ 畫面：第 2 節的資料來源表與張數表（cell 12 附近）

**畫面標籤：`pre-executed output`**

1. **My images come from public weather datasets.**
   （我的圖片來自公開的天氣資料集。）
2. **Four classes: sunny, overcast, rainy, snowy.**
   （四類：晴、陰、雨、雪。）
3. **One thousand four hundred and five unique images.**
   （1405 張不重複的圖。）
4. **Every class has more than two hundred and fifty.**
   （每一類都超過 250 張。）

**只記一句**：Four classes: sunny, overcast, rainy, snowy.
**發音**：overcast = **OH-ver-kast**（不是「歐弗卡斯特」，重音在第一節）

---

### 卡 3 ｜ 0:55–1:20 ｜ 畫面：去重 summary + 分割那一格

**畫面標籤：`pre-executed output`**

1. **Duplicates are removed by file hash.**
   （重複的圖用檔案雜湊比對移除。）
2. **The split is grouped, so copies never cross it.**
   （分割是分組的，所以副本不會跨到另一邊。）
3. **One thousand one hundred twenty-five for training.**
   （訓練 1125 張。）
4. **Two hundred and eighty for validation.**
   （驗證 280 張。）

**只記一句**：One thousand one hundred twenty-five for training, two hundred and eighty for validation.

---

### 卡 4 ｜ 1:20–1:55 ｜ 畫面：第 3 節資料增強說明 + 預覽圖（3.4b）

**畫面標籤：`pre-executed output`**

1. **Augmentation is flip, small rotation, zoom and brightness.**
   （增強是翻轉、小幅旋轉、縮放、亮度。）
2. **The rotation is small on purpose.**
   （旋轉刻意用很小。）
3. **Before, it was plus or minus fifty-four degrees.**
   （以前是正負 54 度。）
4. **Now it is plus or minus fourteen.**
   （現在是正負 14 度。）
5. **This preview shows the result.**
   （這個預覽就是結果。）

**只記一句**：Before it was plus or minus fifty-four degrees. Now it is fourteen.
**發音**：augmentation = **awg-men-TAY-shun**（重音在 TAY）

---

### 卡 5 ｜ 1:55–2:20 ｜ 畫面：第 4 節模型設計（4.1 / 4.1b）

**畫面標籤：`pre-executed output`**

1. **Two models. First, a small CNN from scratch.**
   （兩個模型。第一個是從零訓練的小 CNN。）
2. **Two hundred fifty-seven thousand parameters.**
   （25 萬 7 千個參數。）
3. **Second, MobileNetV2 with frozen layers.**
   （第二個是凍結大部分層的 MobileNetV2。）
4. **Only five thousand parameters are trained.**
   （只有 5124 個參數被訓練。）

**只記一句**：One model trains from scratch, one is MobileNetV2.
**發音**：parameters = **pa-RAM-eh-terz**；MobileNetV2 = **MOH-byle-net V two**

---

### 卡 6 ｜ 2:20–2:50 ｜ 畫面：第 5 節超參數表

**畫面標籤：`pre-executed output`**

1. **Both models use the same pipeline.**
   （兩個模型用同一套流程。）
2. **Adam. Learning rate one e minus three.**
   （Adam，學習率 1e-3。）
3. **Batch thirty-two. Early stop on validation loss.**
   （batch 32，用驗證損失早停。）
4. **Same seed, same split, same augmentation.**
   （同樣的種子、分割、增強。）

**只記一句**：Same seed, same split, same augmentation.

---

### 卡 7 ｜ 2:50–3:35 ｜ 畫面：6.2 訓練曲線 + 6.5 比較表

**畫面標籤：`pre-executed output`**

1. **The from-scratch model reaches zero point eight two.**
   （從零訓練的模型到 0.82。）
2. **MobileNetV2 reaches zero point nine four.**
   （MobileNetV2 到 0.94。）
3. **MobileNetV2 is better, but it is much bigger.**
   （MobileNetV2 更好，但大很多。）
4. **The train-validation gap is small for both.**
   （兩者的訓練／驗證落差都很小。）

**只記一句**：Zero point eight two, and zero point nine four.
**提示**：講數字時手指著畫面上的 0.8179 / 0.9393，會比念得準更有說服力。

---

### 卡 8 ｜ 3:35–4:25 ｜ 畫面：6.3 曲線解讀 + 6.3b 表 ← **最重要，慢一點**

**畫面標籤：`pre-executed output`**

1. **This is the part I got wrong before.**
   （這是我之前講錯的地方。）
2. **The two lines separate after epoch eight.**
   （兩條線在第八輪之後分開。）
3. **I used to call that overfitting.**
   （我以前把那叫過擬合。）
4. **That was wrong.**
   （那是錯的。）
5. **Validation loss still goes down, to epoch seventeen.**
   （驗證損失還在往下，到第十七輪。）
6. **Accuracy recovers after every jump.**
   （每次跳動後準確率都回來。）
7. **So it is not overfitting, and not random noise.**
   （所以不是過擬合，也不是隨機噪音。）
8. **It is the one e minus three step size.**
   （是 1e-3 的步長造成的。）
9. **Section 6.3b tests this on three runs.**
   （6.3b 用三次實驗驗證這件事。）

**只記一句**：I used to call that overfitting. That was wrong.
**發音**：epoch = **EE-pok**（不是「伊波克」）；overfitting = **OH-ver-fit-ing**

---

### 卡 9 ｜ 4:25–5:00 ｜ 畫面：6.4.1 預測表、6.4.2 表格、6.4.3 比較

**畫面標籤：`pre-executed output`**

1. **Three checks. First, two bugs together.**
   （三個檢查。第一個：兩個 bug 同時存在。）
2. **Batch norm plus double scaling.**
   （BatchNorm 加上雙重縮放。）
3. **Every image is predicted as overcast.**
   （每張圖都被判成陰天。）
4. **Accuracy zero point two one. Lower than guessing.**
   （準確率 0.21，比亂猜還低。）
5. **Second, batch norm alone breaks validation.**
   （第二個：單獨用 BatchNorm 會讓驗證崩掉。）
6. **Third, heavy rotation hurt accuracy.**
   （第三個：大幅旋轉傷害準確率。）
7. **Small rotation is better.**
   （小幅旋轉比較好。）

**只記一句**：Every image is predicted as overcast.

---

### 卡 10 ｜ 5:00–5:35 ｜ 畫面：瀏覽器 `http://127.0.0.1:7871/`（影像介面）

**畫面標籤：`live`**

> **已實測**：這支介面**沒有模型選單**，標題下方固定寫「模型：mobilenet_v2」。
> 所以不要說「選一個模型」，要說「部署的模型是 MobileNetV2」。

1. **This is the image interface.**
   （這是影像介面。）
2. **The deployed model is MobileNetV2.**
   （部署的模型是 MobileNetV2。）
3. **Model and preprocessing come from a saved config.**
   （模型與前處理都從存好的設定讀取。）
4. **So the interface cannot drift from training.**
   （所以介面不會和訓練時不一致。）

**只記一句**：This is the image interface. The deployed model is MobileNetV2.
**發音**：MobileNetV2 = **MOH-byle-net V two**

---

### 卡 11 ｜ 5:35–6:15 ｜ 畫面：**上傳並按 Submit**，讓分數跑出來

**畫面標籤：`live`**

> **用這張圖（兩邊模型都實測正確，不會翻車）**：
> `datasets\hand-filtered\sunny\shine85.jpg`
> 畫面實測：**sunny 99%｜overcast 1%｜rainy 0%｜snowy 0%**
> 後端實測：mobilenet_v2 sunny 0.984、scratch_cnn sunny 0.998
>
> **不要用雨天圖示範。** 我實測 `rainy/rain97.jpg` 在 MobileNetV2 是 rainy 100%，
> 但同一張在自制 CNN 是 **snowy**——若你現場提到另一個模型，畫面會自相矛盾。
> 晴天的圖是兩個模型都判對的少數類別。

1. **Here is a real prediction.**
   （這裡做一次真實預測。）
2. **This is one of the held-out validation images.**
   （這是驗證集留出來的圖，模型沒用它訓練。）
3. **The model says sunny, with ninety-nine percent.**
   （模型說是晴天，99%。）← **照畫面念**
4. **The other classes are almost zero.**
   （其他類別幾乎是零。）
5. **Now the video interface.**
   （接下來是影片介面。）

**只記一句**：Here is a real prediction. The model says sunny.
**注意**：數字一定照螢幕念。Gradio 會把小數顯示成整數百分比，**不要念 0.984**，念 99%。

---

### 卡 12 ｜ 6:15–6:45 ｜ 畫面：`http://127.0.0.1:7862/` 跑 `videos\main-weather-sunny.mp4`

**畫面標籤：`live`**

> **已實測**（間隔 1.0 秒、使用預設滑桿）：9 個取樣點，
> 平均 snowy **43.7%｜sunny 31.5%｜rainy 24.3%｜overcast 0.5%**，
> 摘要列顯示「取樣間隔 1.00 秒（每秒 1.00 次，共 9 個取樣點）」。

1. **Here is the video interface.**
   （這是影片介面。）
2. **The slider sets the maximum gap between samples.**
   （滑桿設定取樣的最大間隔。）
3. **It is capped at one second, so every second is sampled.**
   （上限一秒，所以每一秒都有取樣。）
4. **The model gives nine sample points, and a score for each.**
   （九個取樣點，每個都有分數。）
5. **Overcast stays under one percent.**
   （陰天一直低於 1%。）

**只記一句**：It samples every second and gives a score for each frame.
**為什麼要講第 3 句**：第 2 項扣分（−1.5%）就是這個滑桿，講出來才算回應到。

---

### 卡 13 ｜ 6:45–7:00 ｜ 畫面：`http://127.0.0.1:7863/` 跑 `videos\video2.mp4`

**畫面標籤：`live`**

> **已實測**：39 個取樣點、偵測到 **7 次**變化、最後一次 rainy→snowy 在 **5.21 秒**、
> 結論列寫「overcast 從未被選為最高（全片最高 23.0% 於 t=6.88s）」。

1. **This interface finds weather changes.**
   （這個介面找天氣變化。）
2. **It found seven changes in this clip.**
   （這段影片找到七次變化。）
3. **Overcast is never the top class here.**
   （陰天在這裡從來不是最高。）
4. **That is the known weakness.**
   （這是已知的弱點。）

**只記一句**：It found seven changes. Overcast is never the top class.

---

### 卡 14 ｜ 7:00–7:14 ｜ 畫面：9.3 六類混淆矩陣

**畫面標籤：`pre-executed output`**

1. **Six classes adds foggy and lightning.**
   （六類多了霧和閃電。）
2. **Validation accuracy is zero point nine three.**
   （驗證準確率 0.93。）
3. **Most errors go to foggy.**
   （大部分錯誤被判成霧。）

**只記一句**：Validation accuracy is zero point nine three.

---

### 卡 15 ｜ 7:14–7:22 ｜ 畫面：6.6 部署選擇那張表

**畫面標籤：`pre-executed output`**

1. **I deploy the small model. It is enough, and it is fast.**
   （我部署小模型。夠用，而且快。）
2. **Thank you.**
   （謝謝。）

**只記一句**：I deploy the small model. Thank you.

---

## 五、難字發音表

只列你真的會卡住的字。**括號內是重音節，大寫要念重一點。**

| 字 | 近似發音 | 中文 |
|---|---|---|
| overcast | **OH**-ver-kast | 陰天 |
| epoch | **EE**-pok | 訓練輪次 |
| parameters | pa-**RAM**-eh-terz | 參數 |
| augmentation | awg-men-**TAY**-shun | 資料增強 |
| accuracy | **AK**-yoo-ra-see | 準確率 |
| validation | val-i-**DAY**-shun | 驗證 |
| variance | **VAIR**-ee-uns | 變異數 |
| duplicate | **DYOO**-pli-kit | 重複 |
| scaling | **SKAY**-ling | 縮放 |
| rotation | roh-**TAY**-shun | 旋轉 |
| lightning | **LYTE**-ning | 閃電 |
| confusion | kun-**FYOO**-zhun | 混淆 |

**念不出來的字就換句話說。** 例如 `distribution shift` 太難，就說 `the input changed`。
句子的目的只有一個：讓老師知道你在講哪一格。

---

## 六、不可以說的三句話

| 不要說 | 為什麼 |
|---|---|
| "As you can see, the lines separate, so it's overfitting." | 這是被扣 2% 的原句。現在 notebook 明確否定它 |
| "The model is almost perfect." / "It works very well." | 沒有任何輸出支持這種總結，會被抓「與輸出矛盾的說法」 |
| "I think the accuracy is about…" | 不確定就不要報數字。指著螢幕說 "the number on screen" |

---

## 七、錄完的檢查清單

- [ ] 總長 **7 分 30 秒以內**（目標 7:00–7:25）
- [ ] 聲音清楚，沒有爆音，沒有鍵盤聲壓過人聲
- [ ] **實際按過 Submit**，分數有出現在畫面上（這一條之前幾乎沒有）
- [ ] 卡 8 講的是「不是過擬合」（這是最關鍵的一句）
- [ ] 卡 12 有講「上限一秒」（回應第 2 項扣分）
- [ ] 每個剪接點都有轉場（0.3–0.5 秒淡化或黑場）
- [ ] 已存好的輸出有 `pre-executed output` 標籤；重播有 `replay`；現場操作有 `live`
- [ ] 只講了一次「I'm cutting the waiting time...」，沒有每段重複
- [ ] 畫面上的數字和你念的一致（尤其卡 7、卡 11、卡 12）
- [ ] 沒有 cideo.com 之類的第三方水印
- [ ] 檔案 < 200 MB

---

## 八、時程（現在 11/21 10:50，死線 11/22 23:59）

| 時間 | 做什麼 |
|---|---|
| 今天上午 30 分鐘 | 開 `dist\project1.html`、F11 全螢幕、Ctrl+F 試跳 6.3 / 6.4 / 7 / 8 / 9 各一次。**不錄音** |
| 今天上午 20 分鐘 | 讀卡 1–15 各一次，出聲念，不錄 |
| 今天下午 | 錄卡 1–9（資料到除錯），約 45 分鐘含重錄 |
| 今天下午 | 錄卡 10–15（三個介面 + 六類 + 收尾），約 40 分鐘 |
| 今天晚上 | 合併、跑檢查清單、我幫你覆蓋 `recordings/` 並重打包 zip |
| 11/22 | 緩衝日 + Moodle 上傳並確認「Submitted for grading」 |

> 最後一天不要留給錄影。錄影一定會比預期多花時間。

---

## 九、三支介面（已啟動，可直接錄）

| 介面 | 網址 | 用途 | 實測狀態 |
|---|---|---|---|
| 影像分類 | http://127.0.0.1:7871/ | 卡 10–11 | ✅ sunny 99% on `shine85.jpg` |
| 主要天氣影片 | http://127.0.0.1:7862/ | 卡 12 | ✅ 9 取樣點，snowy 43.7% |
| 天氣變化 | http://127.0.0.1:7863/ | 卡 13 | ✅ 39 取樣點，7 次變化 |

**重開機或關掉之後要重新啟動**（這支腳本會把 notebook 的介面原樣跑起來）：

```powershell
cd "c:\Users\honok\Desktop\cis341\Project_1-Weather_Classification"
.\.venv\Scripts\python.exe tools\serve_demos.py all
```

看到 `[serve] image/video/change: READY` 三行就可以開始錄。**這個視窗不要關。**

---

## 附：怎麼在最乾淨的畫面上簡報 notebook

不要用 VS Code 直接錄（左邊檔案總管、下面終端機都會入鏡）。改用匯出的 HTML：

```powershell
cd "c:\Users\honok\Desktop\cis341\Project_1-Weather_Classification"
.\.venv\Scripts\python.exe -m nbconvert project1.ipynb --to html --output-dir dist
```

> **已驗證可執行**：產出 `dist\project1.html`（約 9.5 MB）。
> 原本這個指令會失敗（cell 102 的截圖附件名稱含大括號，nbconvert 會把大括號
> 轉成 `%7B` 之後找不到檔案），已把附件改名為 `interface-screenshot.png`，
> notebook 只動了那一行，輸出與其他 cell 完全沒變。

然後：

1. 用 Edge 開 `dist\project1.html`
2. `F11` 全螢幕
3. `Ctrl` + `F` 搜尋節號（例如打 `6.3`）直接跳到那一節
4. 字太小就 `Ctrl` + `=` 放大

好處：只有白底黑字和你的圖表，沒有 IDE 介面，字也比簡報大，
而且**每一個數字都是 notebook 的執行輸出，不可能講錯**。

如果匯出的 HTML 讓你覺得跳節不順，**退回用 VS Code 也可以**（按 `Ctrl+Shift+O`
用大綱跳到某一節），只是錄之前要把左側邊欄收起來（`Ctrl+B`）和把終端機關掉（`Ctrl+J`）。