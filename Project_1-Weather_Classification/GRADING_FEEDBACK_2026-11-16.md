# CIS341 Project 1 — Weather Classification 評語回饋

- **評分日期**：2026-11-16
- **原始分數**：64 / 100
- **修訂死線**：**2026-11-22 23:59 HKT**

---

## Grading summary

Your submission includes the data, models, training records and demonstration. The models reproduce your validation results, and your notebook includes useful controlled experiments on batch normalisation and augmentation. Your image interface and its saved tests also meet the requirements.

The main weakness is performance on new scenes. The dataset mixes sky-dominated Sunny/Overcast photos with ground-level Rainy/Snowy photos, so high validation accuracy does not carry over to the independent test. Please also reconsider the strong rotation, resolve the conflicting curve explanations, and complete the video tests. Your AI disclosure is detailed, but two claims of completed checks are unsupported by the outputs.

---

## Dataset

(-1%) Sunny and Overcast are mainly stock skies and phone photos looking upwards, while Rainy and Snowy are mainly street and news photographs from separate collections. A model can learn to associate the source or scene type with a weather label. Please add ordinary sunlit and overcast streets, parks and buildings, and a comparable variety of sources and scenes for every class.

Your source records, duplicate grouping and class counts are useful. (-0.5%) However, the kept/rejected section shows only kept images and reports 0 rejected examples. Please show examples you set aside and explain why.

## Data loading and augmentation

(-0.5%, loading) Training and validation use *tf.image.resize*, while *predict_image*, *predict_frames* and *annotate_video* use PIL's default resize. The reviewer measured different validation results through these paths. Please use consistent preparation and show the direct and interface probabilities for the same image; the check claimed in your notes is not shown.

(-1%, augmentation) *RandomRotation(0.15)* allows rotations up to 54 degrees, although your explanation calls this a small handheld tilt. The preview shows strongly tilted scenes and reflected corners. Please reduce the rotation and repeat the comparison. Your augmentation-off control performs better, so the strength of the transformations is worth investigating before drawing a general conclusion about augmentation.

## Training curves and analysis

(-1.5%, scratch model) Training loss falls steadily, but validation loss jumps at epochs 6, 10 and 13. The notebook mentions these changes without investigating their cause. Please test a possible explanation, such as the learning-rate setting, while keeping the other conditions fixed.

(-2%, justification) At about 4:36–4:54, the recording calls the separation after epoch 8 overfitting. Your notebook instead says there is no divergence, and validation recovers after the jumps. Please resolve these conflicting explanations using both loss and accuracy, with the actual epochs and values. A small final accuracy gap alone does not settle the diagnosis.

(-0.5%, transfer model) The best validation loss occurs at the final epoch, 20. Please explain the stopping decision or try a longer run with early stopping to see whether the model continues improving.

Your batch-normalisation and augmentation investigations are genuine controlled comparisons. For the double-scaling investigation, please include the earlier model output if you describe its collapse to one class; the arithmetic illustration does not show the model's actual predictions.

## Independent benchmark

The four-class benchmark gives 0.5/15. Scratch scores 40.9% on ordinary cases and 40.6% on harder cases; transfer scores 54.5% and 45.3%. The transfer model never predicts Overcast on the ordinary test, and many sunlit ground-level scenes are called Rainy or Snowy. Please use these kinds of new scenes when checking your revised collection.

The six-class benchmark gives 1.5/10. Foggy and Lightning are suitable choices, and the model recognises 15 of 20 independent examples of each. However, confusion with the original classes remains substantial: it still misses Overcast and often assigns Foggy to Sunny or Overcast scenes. Please compare these mistakes with the four-class baseline when improving the extension.

## Video

- **Main-weather prediction (-1%)**: sampling and averaging are correct, but the sampled frames are not shown. The Sunny clip is labelled Snowy, narrowly ahead of Sunny, without enough investigation. Please show the sampled frames and inspect why the model makes this mistake.
- **Main-weather interface (-1.5%)**: it is tested only with the Sunny clip. Please test different conditions, including a changing-weather clip. Also fix the interval control: it allows gaps of up to 3 seconds and rejects intervals below 1 second. "At least once per second" means the gap must be no greater than 1 second.
- **Changing-weather prediction (-0.5%)**: the algorithm handles *N*, timing and held predictions correctly, but only *video2.mp4* is tested. Please also run the common changing-weather clip and explain the missed Overcast segment and incorrect labels within the snowy segment.
- **Changing-weather interface (-1%)**: the table and text list of changes are useful, but the interface does not display the annotated video or a timeline beside the original footage. Your code already produces an annotated video; please return it from the interface so the predictions can be checked against the scene.

## AI disclosure (-2%)

Your disclosure identifies GitHub Copilot agent mode and clearly describes the boundary between its drafts and your decisions, experiments and changes. The deduction concerns these two statements:

- In the AI note for Section 3, you say you personally checked that the same image gives the same answer through direct prediction and the interface. Section 3.4 only saves the class order; it does not show that comparison, and the two paths resize differently.
- In the AI note for Section 2, you say you personally chose the rejected examples shown in Section 2.4. That section reports 0 rejected images and shows none.

Please check AI-drafted statements against the work actually shown. Add the missing evidence if the checks were performed, or correct the statements if they were not. You may explain this in the revised notebook; a new recording is not required solely to clarify these statements.

---

## What to try

- Please diversify the scenes and sources in every class, retaining your duplicate-grouping approach.
- Reduce the rotation, investigate the scratch swings with a controlled retest, and resolve the conflicting explanations.
- Complete the video tests and display, correct the sampling-interval control, and support or correct the two AI-disclosure claims.
- Please submit your revision by **2026-11-22 23:59 HKT**, and confirm that Moodle shows "Submitted for grading".

---

## Marks

| 項目 | 得分 |
| :--- | :--- |
| Data collection and inspection | 3.5 / 5 |
| Data loading, labels and preprocessing | 7 / 7.5 |
| Augmentation | 6.5 / 7.5 |
| Scratch model | 6 / 7.5 |
| Transfer model | 7 / 7.5 |
| Justification | 13 / 15 |
| Automatic quality benchmark | 0.5 / 15 |
| Image interface | 5 / 5 |
| Video — Main-weather prediction | 4 / 5 |
| Video — Main-weather interface | 3.5 / 5 |
| Video — Changing-weather prediction | 4.5 / 5 |
| Video — Changing-weather interface | 4 / 5 |
| Six-class classifier | 1.5 / 10 |
| AI disclosure | −2 |
| **Total** | **64 / 100** |

---

## 扣分優先序（依「每小時可回收分數」排序）

| 順位 | 問題 | 可回收 | 預估工時 | 每小時得分 | 難度 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | AI disclosure 兩項聲明無證據 | **+2.0** | 1.0 h | 2.00 | 極低（改文字或補圖） |
| 2 | 影片取樣間隔控制 bug（允許 3 秒空窗、拒絕 <1 秒） | +1.5 | 1.0 h | 1.50 | 低（改驗證條件） |
| 3 | 主天氣介面只測 Sunny clip | 併入上列 | 0.5 h | — | 低 |
| 4 | 變天介面沒回傳標註影片 | +1.0 | 1.0 h | 1.00 | 低（程式已產生，只需回傳） |
| 5 | 旋轉幅度過大 0.15（54°）→ 調降重跑 | +1.0 | 1.5 h | 0.67 | 低 |
| 6 | 曲線說明矛盾（錄影 vs 筆記本） | +2.0 | 2.0 h | 1.00 | 中（需算實際數值） |
| 7 | Scratch 震盪未查因（學習率假設） | +1.5 | 2.0 h | 0.75 | 中 |
| 8 | 雙路徑 resize 不一致 ＋ 缺同圖機率對照 | +0.5 | 2.0 h | 0.25 | 中 |
| 9 | 顯示抽樣幀 ＋ 解釋 Sunny→Snowy | +1.0 | 1.5 h | 0.67 | 低 |
| 10 | rejected 範例 0 張，需補實際被剔除樣本 | +0.5 | 1.5 h | 0.33 | 中 |
| 11 | 變天預測只測 video2.mp4 | +0.5 | 1.0 h | 0.50 | 低 |
| 12 | Transfer 最佳 loss 在最後 epoch，需早停或延長 | +0.5 | 2.0 h | 0.25 | 中 |
| 13 | 四類 benchmark 0.5/15（資料集根本問題） | +14.5 | 20 h+ | 0.7 | **極高** |
| 14 | 六類 classifier 1.5/10 | +8.5 | 15 h+ | 0.57 | **極高** |

**結論**：13、14 兩項共佔 23 分，但要重做整個資料集（新增實景 street / park / building 照片、重新分組去重、重跑全部模型與 benchmark），3 天內不可能完成。目標應鎖定 **1~12 項**，理論可回收約 **+9.5 分**（64 → 約 73）。