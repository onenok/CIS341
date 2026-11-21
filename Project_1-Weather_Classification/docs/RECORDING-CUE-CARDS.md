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

**這次的目標是 6 分 45 秒左右，正常語速，不做任何後製加速。**
下面的提示卡就是照這個長度設計的。

---

## 二、錄法：一段一段錄，最後接起來

作業允許剪接，原文第 197 行：「**你可以剪掉等待時間，但須標明**已儲存的結果與重播的片段。」
所以一段一段錄完全合規，只要你講一句「I've cut the waiting time here.」

### 步驟

1. **OBS 設定**照 [RECORDING-PLAN.md](./RECORDING-PLAN.md) 第二節（1080p / 30 fps / CQP 22）。
2. **手機打開本文件**（或印出來），放在鏡頭旁邊。螢幕上只放 notebook。
3. **一次只錄一張卡**，檔名 `01.mp4`、`02.mp4`……共 14 個檔。
4. 講壞了就**整張卡重錄**，不用從頭。
5. 每錄完一張，**立刻回放聽一次**（30 秒，不要省）。
6. 全部錄完，用下面的指令合併（`ffmpeg` 若沒有，先 `winget install Gyan.FFmpeg`）：

```powershell
cd "c:\Users\honok\Desktop\cis341\Project_1-Weather_Classification\_rec2"
"file '01.mp4'`nfile '02.mp4'`nfile '03.mp4'`nfile '04.mp4'`nfile '05.mp4'`nfile '06.mp4'`nfile '07.mp4'`nfile '08.mp4'`nfile '09.mp4'`nfile '10.mp4'`nfile '11.mp4'`nfile '12.mp4'`nfile '13.mp4'`nfile '14.mp4'" | Out-File -Encoding ascii list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy ..\recordings\screen-recording.mp4
```

（`-c copy` 不重新編碼，所以合併只花幾秒，畫質不會掉。全部用同一組 OBS 設定錄就沒問題。）

---

## 三、講話的四個規則

1. **一句不超過 12 個字。** 超過就是句子太長，拆成兩句。
2. **講完一句停 1 秒。** 停頓可以剪掉，講太快不能補救。
3. **講錯不要道歉、不要重來。** 閉嘴 2 秒，然後把那句重講一次，剪掉前面失敗的。
4. **發音不完美沒關係。** 評分看的是內容與數字，不是口音。**不要為了發音漂亮而結巴**，講順比講對重要。

### 標明剪接的那句話（作業要求，必須說）

在任何剪接點講其中一句：

> "I've cut the waiting time here."
> "This result was already saved, so I'm not running it again."

---

## 四、14 張提示卡

> **粗體 = 你要講的英文。** 英文下面的小字是中文意思。
> 每張卡的「只記一句」是萬一你緊張到全忘，講那一句就夠。

---

### 卡 1 ｜ 0:00–0:20 ｜ 畫面：notebook 最頂端（標題 + AI 使用聲明）

1. **This is my weather classification project.**
   （這是我的天氣分類專題。）
2. **I used GitHub Copilot. I checked the results myself.**
   （我用了 Copilot，結果我自己核對過。）
3. **The notebook below shows all the evidence.**
   （下面的 notebook 就是全部證據。）

**只記一句**：This is my weather classification project.

---

### 卡 2 ｜ 0:20–0:55 ｜ 畫面：第 2 節的資料來源表與張數表（cell 12 附近）

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

### 卡 10 ｜ 5:00–5:30 ｜ 畫面：7 節介面截圖或直接切到瀏覽器的影像介面

1. **This is the interface. Choose a model, then upload an image.**
   （這是介面。選模型，然後上傳圖片。）
2. **It shows the top classes and their scores.**
   （它顯示最可能的類別與分數。）
3. **Model and preprocessing come from a saved config.**
   （模型與前處理都從存好的設定讀取。）
4. **So the interface cannot drift from training.**
   （所以介面不會和訓練時不一致。）

**只記一句**：Choose a model, then upload an image.

---

### 卡 11 ｜ 5:30–6:10 ｜ 畫面：**實際按一次送出**，讓分數跑出來

> **先用這張圖（我已經實測過，分數很高、不會出錯）**：
> 介面選 **MobileNetV2**，上傳
> `datasets\hand-filtered\rainy\rain97.jpg`
> 實測輸出：**rainy 0.9998**，其他三類 0.0000 / 0.0000 / 0.0002
>
> 備用（分數第二高、同樣安全）：`datasets\hand-filtered\rainy\rain47.jpg` → rainy **0.9997**
> 想示範小模型就用 `datasets\hand-filtered\rainy\rain155.jpg` → rainy **0.9861**
>
> **不要用** `overcast\cuaca_rainy_0105.jpg` 這種檔名和標籤不一致的圖，會多出一個要解釋的畫面。

1. **Here is a real prediction.**
   （這裡做一次真實預測。）
2. **This is one of the held-out validation images.**
   （這是驗證集裡留出來的圖，模型沒用它訓練。）
3. **The model says rainy, with a score of zero point nine nine.**
   （模型說是雨天，分數 0.99。）← **照著畫面上的數字念，四捨五入到兩位就好**
4. **The other classes are almost zero.**
   （其他類別幾乎是零。）
5. **Now I'll run a video.**
   （現在跑一段影片。）

**只記一句**：Here is a real prediction. The model says rainy.
**注意**：第 3 句的數字**一定要照螢幕上顯示的念**。若臨時換了圖、分數低於 0.6，
就誠實說 "The model says rainy, but the score is low."——誠實比好看安全。

---

### 卡 12 ｜ 6:10–6:40 ｜ 畫面：8.3 影片輸出的逐幀結果圖或表格

1. **This is the video result.**
   （這是影片結果。）
2. **The model scores every sampled frame.**
   （模型對每個取樣幀打分數。）
3. **It finds the snow in the second half.**
   （它在後半段找到雪。）
4. **Overcast is still the weakest class.**
   （陰天仍然是最弱的一類。）

**只記一句**：It finds the snow in the second half.

---

### 卡 13 ｜ 6:40–7:00 ｜ 畫面：9.3 六類混淆矩陣

1. **Six classes adds foggy and lightning.**
   （六類多了霧和閃電。）
2. **Validation accuracy is zero point nine three.**
   （驗證準確率 0.93。）
3. **Most errors go to foggy.**
   （大部分錯誤被判成霧。）

**只記一句**：Validation accuracy is zero point nine three.

---

### 卡 14 ｜ 7:00–7:15 ｜ 畫面：6.6 部署選擇那張表

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

- [ ] 總長 **7 分 30 秒以內**（目標 6:45–7:15）
- [ ] 聲音清楚，沒有爆音，沒有鍵盤聲壓過人聲
- [ ] **實際按過一次送出**，分數有出現在畫面上（這一條之前幾乎沒有）
- [ ] 卡 8 講的是「不是過擬合」（這是最關鍵的一句）
- [ ] 有講到剪接（"I've cut the waiting time here."）
- [ ] 畫面上的數字和你念的一致（尤其卡 7、卡 11、卡 13）
- [ ] 沒有 cideo.com 之類的第三方水印
- [ ] 檔案 < 200 MB

---

## 八、時程（現在 11/20 22:25，死線 11/22 23:59）

| 時間 | 做什麼 |
|---|---|
| 今晚 30 分鐘 | 只做一件事：把 notebook 開好、`nbconvert --to html`、F11 全螢幕、Ctrl+F 試跳每一節。**不錄音** |
| 今晚 20 分鐘 | 讀卡 1–14 各一次，出聲念，不錄 |
| 明天上午 | 錄卡 1–7（資料到訓練比較），約 40 分鐘含重錄 |
| 明天下午 | 錄卡 8–14（分析、介面、影片、六類），約 50 分鐘 |
| 明天晚上 | 合併、檢查清單、更新 README、重打包 zip |
| 11/22 | 緩衝日 + Moodle 上傳並確認「Submitted for grading」 |

> 最後一天不要留給錄影。錄影一定會比預期多花時間。

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