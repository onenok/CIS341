# Revision change list — CIS341 Project 1 (Weather Classification)

- **Student**: S26202765
- **Reviewed submission**: 2026-11-16, 64 / 100
- **This revision**: submitted 2026-11-22 (before 23:59 HKT)
- **What changed**: `project1.ipynb` (104 cells, executed, stored outputs, 0 errors),
  `weather_lib.py`, `runs/`, `models/`, `Reports/`, `recordings/`
- **What did not change**: the image dataset, the saved model architectures, the
  four-class and six-class benchmark results, and the independent test scenes

Every number in this document is copied from an executed cell of the submitted
notebook, not from memory and not estimated. Where a number appears here, the
cell that produced it is named, so it can be checked against the stored output.

This list was drafted with GitHub Copilot and then checked line by line against
the notebook outputs, in the same way as the AI disclosure at the top of the
notebook.

---

## Summary

| # | Point raised in the review | Deduction | Status | Check it in |
|---|---|---|---|---|
| 1 | AI-disclosure claims not supported by outputs (×2) | −2% | **fixed** (evidence added) | 2.4b, 3.4b, 7.3 |
| 2 | Training/validation resize paths differ; interface probabilities not shown | −0.5% | **fixed** | 3.4b, 7.3, `weather_lib.to_model_input` |
| 3 | `RandomRotation(0.15)` = ±54°, too strong; repeat the comparison | −1% | **fixed** | 4.1b, 6.4.3 |
| 4 | Scratch-model validation jumps at epochs 6/10/13 not investigated | −1.5% | **fixed** | 6.3, 6.3b |
| 5 | Recording and notebook give conflicting curve explanations | −2% | **fixed, both sides** | 6.3, 6.3b, and the new recording |
| 6 | Transfer model: best val loss at the final epoch, no stopping argument | −0.5% | **fixed** | 6.2, 6.5 |
| 7 | Double-scaling section shows arithmetic, not the model's predictions | (part of Justification) | **fixed** | 6.4.1 |
| 8 | Sampled frames not shown; Sunny→Snowy misclassification not investigated | −1% | **fixed** | 8.1 |
| 9 | Main-weather interface tested only with the Sunny clip; interval control allows 3 s gaps and rejects <1 s | −1.5% | **fixed** | 8.2, 8.2b |
| 10 | Changing-weather prediction tested only on `video2.mp4` | −0.5% | **fixed** | 8.3, 8.3b, 8.4b |
| 11 | Changing-weather interface does not return the annotated video / timeline | −1% | **fixed** | 8.4, 8.4b |
| 12 | Kept/rejected section shows 0 rejected examples | −0.5% | **fixed** | 2.4b |
| 13 | Dataset mixes sky-dominated and ground-level scenes | −1% | **not changed** | see B1 |
| 14 | Automatic quality benchmark 0.5 / 15 | −14.5 | **not changed** | see B2 |
| 15 | Six-class classifier 1.5 / 10 | −8.5 | **partly addressed** | 9.3, see B3 |
| 16 | Screen recording | — | **re-recorded** | see C |

Three things I want to say plainly before the detail, because they are
corrections rather than improvements:

1. **The curve explanation in the previous notebook was wrong, and I can show
   why.** I had written that the validation jumps were sampling noise. The
   controlled retest in 6.3b shows that of 12 jumps, all 12 raised the loss on
   both disjoint 140-image halves simultaneously, which sampling noise cannot
   do. The previous explanation is retracted in the notebook itself.
2. **The previous notebook's account of the collapse was also unmeasured.** It
   said validation accuracy "equalled the majority-class share". It did not: the
   rebuilt pre-fix model scored 0.2071, while the majority class is 0.3821, so it
   did worse than always guessing `snowy`. 6.4.1 now reports the model's actual
   predictions on all 280 validation images.
3. **The previous recording contained numbers that no longer match the
   notebook.** It has been re-recorded from the executed outputs.

---

## A. What changed

### A1. AI-disclosure claims now have evidence (`−2%`)

The review identified two statements that the notebook did not support.

**(a) "I checked that the same image gives the same answer through direct
prediction and the interface."** Section 3.4 only saved the class order, and the
two paths really did resize differently, so the claim was not merely unshown —
it was false. Both halves are fixed:

- **The bug**: `make_dataset` resized with `tf.image.resize(..., bilinear)`
  while `predict_image`, `predict_frames` and `annotate_video` used
  `PIL.Image.resize`, whose default resampler is bicubic. One photograph
  therefore entered the model with different pixels depending on the path it
  took. All inference paths now go through `weather_lib.to_model_input()` /
  `read_model_input()`, which use `tf.image.resize` and the same decoder order
  as training.
- **The evidence**: **3.4b** measures the tensor the model actually receives
  through three paths (the loader, the new shared path, and the old PIL path)
  for three images and both preprocessing specs. Loader vs new path is
  bit-identical (max difference `0.0`, `identical = True`); the old PIL path is
  not. **7.3** then compares the deployed model's probability through the loader
  and through the Gradio callback: identical class, maximum probability
  difference `0.0` across the batch.

**(b) "I personally chose the rejected examples shown in section 2.4."**
Section 2.4 printed "0 rejected" because it scanned a folder that was never
created. **2.4b** now reads `datasets/review-sheets/decisions_*.csv` row by row,
maps each `candidate_id` back to the original file, and checks that the file is
still on disk and *absent* from the kept index `image_index.csv`. It then shows
a batch of the images that were actually set aside, with the automatic test that
flagged each one and the reason recorded at the time.

Section 2.4b now backs the second claim, and the AI-use disclosure at the top of
the notebook points at both sections instead of asserting the checks.

The disclosure also gained a section **"這次修訂（依評語重交）的 AI 使用"**. It
lists, per revision item, which code the AI drafted during this revision and which
decisions were mine — including the items where the AI's first version was wrong
(the ±54° rotation, the reversed sampling-interval guard) and the item I refused
(showing training images as unseen examples). The disclosure now covers the
revision, not only the original submission.

### A2. One resize path for training and inference (`−0.5%`)

Same fix as A1 first half. The review's specific request was "show the direct
and interface probabilities for the same image"; that is **7.3**, a table of four
images (two train, two validation) with loader argmax, callback argmax, both
maximum probabilities, and the difference. The difference column is `0.0` for
every row.

### A3. Rotation reduced from ±54° to ±14.4°, comparison repeated (`−1%`)

`RandomRotation`'s argument is a fraction of a **full turn**, not a fraction of a
half turn. `0.15` was therefore ±54°, not "a small handheld tilt".

- **4.1b** converts both settings to degrees and measures the chance of exceeding
  30° and 45°: the old `0.15` puts **44%** of samples beyond 30° and **17%**
  beyond 45°; the new `0.04` is ±14.4° with **0%** beyond 30°. The cell also
  rotates one real photo by each maximum angle so the two settings can be
  compared by eye.
- **6.4.3** repeats the augmentation on/off comparison at the new rotation, on
  the same 23-epoch budget, same seed, same split, same validation set.

The result is reported in 6.4.3 and it is **not** the answer the review might
have expected: reducing the rotation helped the augmented run (0.789 → 0.804)
but the no-augmentation run improved as well (0.861 → 0.886), so the gap widened
from 0.072 to 0.082. Section 6.4.3 states the three conclusions I can draw
("on this dataset, this 4-layer model and this 23-epoch budget, augmentation did
not pay") and the one I cannot ("augmentation is useless in image
classification"), and explains why a single seed on 280 validation images cannot
support the general claim.

### A4. The scratch-model jumps are now investigated, not mentioned (`−1.5%`, `−2%`)

**6.3** keeps the observation but the explanation is rewritten: the previous
"validation sampling noise" reading is explicitly retracted, with a forward
reference to the experiment that replaced it.

**6.3b** is the controlled retest the review asked for. Three runs differ **only**
in the learning-rate setting — `1e-3` with `ReduceLROnPlateau` (the submitted
configuration), `1e-3` constant, and `3e-4` constant. Same seed 341, same
1125/280 split, same augmenter, same batch size, same patience, same 40-epoch cap.

| run | epochs | best val loss | final val loss | best val acc | jumps | mean \|Δval loss\| | max \|Δ\| |
|---|---:|---:|---:|---:|---:|---:|---:|
| A `1e-3` + plateau | 18 | 0.5253 @ e12 | 0.7985 | 0.8214 | 5 | 0.1942 | 0.6177 |
| B `1e-3` constant | 15 | 0.6200 @ e9 | 0.7226 | 0.8071 | 3 | 0.1522 | 0.4661 |
| C `3e-4` constant | 23 | 0.5284 @ e17 | 0.6941 | 0.8179 | 4 | 0.1359 | 0.3893 |

What the experiment establishes:

- **The schedule is not the cause.** A and B both jump at e6 → e7, and A's
  plateau only first acts at e12, after it has already jumped three times.
- **The base learning rate changes the size, not the existence.** C's mean
  amplitude is 70% of A's and 89% of B's; the jumps are smaller but still there.
- **It is not sampling noise.** The validation loss was recomputed every epoch on
  two disjoint 140-image halves. Of the 12 jumps, **12 raised the loss on both
  halves at once**. Independently resampled noise would not do that. For scale,
  the mean |difference| between the two halves for a fixed model is 0.1208.
- **It is a temporary oscillation, not divergence.** In 10 of the 12 jumps the
  training loss fell while validation loss rose.
- **Keeping `1e-3` + plateau is still the right call** on this budget: B ends
  0.0948 worse, C reaches the same level but needs five more epochs, and in all
  three runs the checkpoint chosen by early stopping (e12 / e9 / e17) does not
  fall after a jump.

Two limits are stated in the section rather than hidden: run A is not a bitwise
replay of section 6.2's original run (0.5009 @ e17 there, 0.5253 @ e12 here,
because the RNG state differs), and the three runs share one seed.

`runs/lr_probe.json` carries the raw record, including the per-epoch split-half
losses, so the claim can be re-derived without retraining.

### A5. Transfer model: the stopping decision is argued, not asserted (`−0.5%`)

Section 6.2 shows the stored history for both models, and 6.5 evaluates both on
the same 280 images:

| model | epochs run | best val loss (epoch) | validation accuracy | macro F1 |
|---|---:|---:|---:|---:|
| `scratch_cnn` | 23 | 0.5009 (e17) | 0.8179 | 0.791 |
| `mobilenet_v2` | 17 | 0.1871 (e11) | 0.9393 | 0.934 |

The transfer model's best validation loss now falls at **epoch 11 of 17**, not at
the final epoch, so early stopping selects a minimum that is not merely the last
step: validation loss stays in 0.187–0.210 for epochs 12–17 while training loss
keeps falling from 0.154 to 0.126, which is the start of memorisation rather than
further learning. The chosen checkpoint's validation accuracy (0.9393 at e11) is
also the highest value reached anywhere in the run (e7 and e9 reach the same
0.9393), so nothing is lost by selecting on loss rather than on accuracy.

The scratch model follows the same pattern: best validation loss 0.5009 at
epoch 17, stopped at epoch 23, training accuracy 0.850 against validation 0.804
(gap +0.046).

### A6. The collapse is now shown with the model's own predictions

**6.4.1** rebuilds the pre-fix network — the same CNN with a `Rescaling(1/255)`
inside the model **and** `BatchNormalization` after every convolution — with the
same seed, split, augmenter and patience, trains it, and runs it on the same 280
validation images.

| model | epochs | validation acc | distinct classes predicted | max prob (mean / min) |
|---|---:|---:|---:|---:|
| before the fixes | 7 (early stop) | **0.2071** | **1** | 0.4028 / 0.4014 |
| after the fixes (6.4.0) | 23 | **0.8179** | 4 | 0.8763 / 0.3321 |

All 280 validation images were predicted `overcast`; the confusion matrix has
values in one column only. Every image's maximum probability lies between 0.4014
and 0.4036 — the model saw 280 identical inputs.

The section also reports a control that keeps **only** the double scaling and
drops BatchNorm: 0.5179 with all four classes still predicted. Neither defect
alone produces the collapse; both together do. That is the substantive finding,
and it is why the two investigations are separate sections rather than one.

`runs/pre_fix.json` stores the prediction record, so the numbers can be checked
without retraining.

### A7. Video section 8.1: the sampled frames are shown, and the Snowy verdict is investigated

**8.1** now displays a 3×3 mosaic of the nine frames the model actually saw — the
same `W.sample_frames` output that feeds the probabilities, not a second decode —
each labelled with its timestamp and its own argmax and confidence.

The nine individual predictions are not stable (5 snowy, 3 sunny, 1 rainy), and
the mean is `snowy 0.4368 / sunny 0.3150 / rainy 0.2434 / overcast 0.0048`, which
is why the clip is labelled Snowy. Majority vote over the nine frames also gives
Snowy (5/9), so the label is not an artefact of averaging.

To find out why, 8.1 tests two hypotheses and **rejects the obvious one**:

- *Hypothesis A — the model reads the lower half (wet asphalt, pale gravel) and
  mistakes it for snow.* **Rejected.** Fed only the bottom 60%, the frame is
  classified `rainy 0.7459`, `snowy 0.2199`, `sunny 0.0246`. Fed only the top
  40%, it is `sunny 0.3499` / `snowy 0.3300` — a draw, and no snowy peak. **No
  horizontal band on its own produces Snowy.**
- *Hypothesis B — Snowy comes from the overall composition, not from any local
  patch.* **Supported.** Removing only the middle 20% strip (the dark tree line
  on the far bank) and joining the top 40% to the bottom 60% raises snowy from
  0.4368 to **0.7709** while sunny falls to 0.0838.

One strip of dark pixels nearly doubles the Snowy score, while neither half alone
can produce it, so the verdict is composition-driven: bright sky on top, bright
speckled water below, a dark line between them — the same layout as the snowy
scenes in the training data. The pixel census agrees: blue sky is only
**17.2%–22.7%** of the frame (median 21.9%), and near-white pixels are 1.5%–2.5%,
of which 2.4%–4.1% lie below the 40% line. The most direct evidence of "sunny",
a blue sky, is under a quarter of this clip, and what remains resembles winter.

Section 8.1 states this as a measured, falsifiable result and links it to the
dataset limitation in B1, rather than concluding that the model is simply wrong.

### A8. Main-weather interface: interval control fixed, and three clips tested

**The control.** The previous slider accepted 1.0–3.0 s, which contradicts "at
least once per second", and rejected anything below 1.0 s, which is exactly
backwards. `MAX_INTERVAL_S = 1.0` now, the slider runs `0.25 … 1.0` in 0.25 steps,
and the guard is `if not 0 < interval <= MAX_INTERVAL_S: raise gr.Error(...)`.
**8.2b** exercises it: `0.5` and `1.0` are accepted, and `3.0`, `1.5` and `0.0`
are each rejected with the error message shown.

**The clips.** **8.2b** now runs the interface on three clips — the Sunny clip,
`video2.mp4`, and `common-changing-weather.mp4` — and checks that the returned
annotated video exists and is decodable, that the table has one row per sampled
frame, and that the reported interval matches the request.

### A9. Changing-weather prediction: the missed Overcast explained, and both clips run

**8.3b** addresses the two specific questions in the review on `video2.mp4`, using
measurements rather than assumption. (The first explanation I wrote for this
section was refuted by its own numbers — the note at the top of 8.3b says so.)

- **Why Overcast is missed.** Over the whole clip none of the 39 sampling points
  is classified `overcast` (rainy 21, snowy 14, sunny 4). The highest `overcast`
  probability anywhere is 0.2301 at t = 6.88 s, which falls in the *snowy*
  segment; across the genuinely overcast 1.88–4.38 s it averages 0.0051. Band
  crops show the model can see the overcast sky but reads it as snow: keeping
  only the top 40% raises `overcast` 27× (0.0051 → 0.1387), yet 11 of those 12
  sky-only crops are classified **snowy** — flat grey-white cloud read as a snow
  field. The bottom 60% alone is `rainy` on 12 of 12 at a mean 0.9857, so it
  outvotes the weak sky signal when the frame is whole (rainy 0.8349).
- **The incorrect labels inside the snowy segment.** In the version that was
  marked, the label changed three times between 5.2 s and 8.0 s
  (snowy → sunny → snowy → overcast). After the retrain for item A3,
  14 consecutive sampling points from 5.21 s to 7.92 s are all `snowy` at
  0.8082–0.9940, and the top-40% and bottom-60% crops are both snowy there too.
  Nothing was tuned for this segment; it is a side effect of the rotation change.
- **The cost of that change, reported rather than hidden.** The opening sunny
  frames (0.00–0.83 s) are now predicted `rainy` (previously sunny 0.84). Band
  decomposition gives the same pattern as 8.1: at t = 0.00 s the top 40% alone is
  sunny 0.745 and the bottom 60% alone is rainy 0.833, and the whole frame follows
  the ground. One set of weights made the snowy segment stable and the sunny
  segment worse; the section says so instead of showing only the improvement.
- **No temporal smoothing is applied to make the output look better.** Averaging
  or majority voting would stabilise the annotation, but it would no longer be
  the model's per-point output, which is what this section is meant to test.

**8.4b** then runs the changing-weather interface on **both** clips — `video2.mp4`
and `common-changing-weather.mp4` — and checks that the returned annotated video
decodes, that its width and height match the source, that the gap parameter is
rejected at 0 and 6 frames and accepted for 1…5, and that the timeline, table and
text outputs are consistent with each other on both clips.

### A10. Changing-weather interface now returns the annotated video

The review's point was that the code already produced an annotated video but the
interface did not return it. `analyse_change` now returns a 4-tuple
`(clip_path, timeline_figure, table, text)`, the video is written to
`Reports/change-annotated-<stem>.mp4`, and the interface displays it next to the
original footage with a timeline figure of the changes. **8.4b** verifies the
returned file decodes and has the same dimensions as the source.

### A11. Kept/rejected: 2.4b

Described under A1(b). The section shows actual set-aside images with the
automatic threshold that flagged them and the decision recorded at the time, and
asserts that none of them appear in the kept index.

---

## B. What I did not change, and why

### B1. Scene diversity in the dataset (`−1%`) — not changed

The review is right and I have not fixed it. Sunny and Overcast are still mostly
sky-dominated stock and phone photos looking upwards, while Rainy and Snowy are
street-level and news photographs from separate collections.

Why not: fixing it means collecting several hundred **new** photographs of
ordinary sunlit and overcast streets, parks and buildings, hand-checking every
one against the class boundaries in 2.1, re-running duplicate grouping, and then
re-training both models and re-running both benchmarks. I judged that adding
unverified images would damage the parts of section 2 that currently hold up
(the duplicate grouping and the per-class source records) more than the added
scenes would help, and I could not hand-check that many new images to the same
standard before the deadline.

What I did instead: I stopped describing validation accuracy as if it carried
over to new scenes, and I wrote the limitation into the notebook where it
matters — 6.6 when choosing the deployment model, 8.1 when explaining the
Sunny→Snowy verdict, and 9.3 when comparing the six-class result with the
four-class baseline.

I also kept the evidence that shows the problem from the inside: the rainy/snowy
confusion (25 of 52 rainy images predicted snowy, 6.4.0) is the same failure the
independent benchmark punishes, and it is measured on data the model was not
trained on.

### B2. Automatic quality benchmark (`0.5 / 15`) — not re-run

That score comes from the grader's own independent test scenes. It can only move
if the training data changes, so re-submitting with the same dataset leaves it
where it is. Re-running it myself would not produce a different number, and
reporting a self-measured version of a grader-run benchmark would not be
comparable. Nothing in this revision claims that benchmark has improved.

### B3. Six-class classifier (`1.5 / 10`) — partly addressed

The classifier itself is unchanged, so the benchmark score should be unchanged.
What I could do within the deadline was the comparison the review asked for
("compare these mistakes with the four-class baseline"). **9.3** now reports:

- six-class validation accuracy **0.9314**, macro F1 **0.926** on 525 images;
- the 0.8-point difference from the four-class 0.9393 is **not** evidence that
  adding classes costs nothing — the split is different (525 vs 280 validation
  images) and the new classes are easier (foggy F1 0.942, lightning F1 0.959);
- 36 errors of 525, of which **17 (47%) are pushed into `foggy`**, class by
  class: snowy→foggy 7, rainy→foggy 5, sunny→foggy 2, lightning→foggy 2,
  overcast→foggy 1. `foggy`'s precision is 0.913 (178/195) for the same reason;
- the misses are weighted towards recall rather than accuracy (sunny 0.873,
  snowy 0.897), because foggy is the largest class in the training data
  (732 images, against 209 for rainy).

The review noted the six-class model "still misses Overcast". In this split
Overcast recall is 0.948 (55/58), so on the current split that specific failure
does not reproduce; the dominant failure is now the pull towards `foggy`. I am
reporting what the current run shows rather than repeating the earlier claim.

### B4. Things I tested and deliberately did not change

These are written into the notebook because the review asks for the rejected
proposals as well as the accepted ones:

- **Adding BatchNorm everywhere** — tested in 6.4.2, made validation worse
  (0.271 against 0.807 without). Rejected.
- **Fixing BatchNorm by lowering `momentum`** — 6.4.2 explains why the stored
  moving statistics are the problem at this update count and why tuning the
  momentum would hide it rather than fix it. Rejected.
- **Deleting `spec.fn` to fix the double preprocessing** — three inference paths
  go through `spec.fn`, so deleting it would break all three. The model-internal
  layer was deleted instead. Rejected.
- **Claiming "augmentation is harmful"** — 6.4.3 lists three reasons the current
  evidence cannot support that general claim. Rejected.
- **Using training images as "unseen examples" in 9.4** — replaced with
  validation-split images only. Rejected.
- **Colour-space grouping, or re-labelling ambiguous cases** — the class
  boundaries in 2.1 are unchanged; every ambiguous image was still decided by
  hand rather than by an automatic rule.

---

## C. The screen recording

**Re-recorded.** The previous recording (7:22) contained several numbers that no
longer match the notebook and, at 4:36–4:54, the curve explanation this revision
retracts (§A4). Leaving it in place would have left the same conflict the review
identified, so it was replaced rather than annotated.

What the new recording does differently:

- **Every number spoken is read from an executed cell of the submitted
  notebook**, and the numbers that moved since the marked submission are listed
  here so they can be checked: `scratch_cnn` 0.811 → **0.8179**; the BatchNorm
  run's validation accuracy 0.346 → **0.271** (val loss 3.403); the no-BatchNorm
  control 0.800 → **0.807**; the BatchNorm variance ratio 3.3–6.8× →
  **5.78 / 5.93 / 4.98 / 4.43**; the augmentation comparison 0.789 → 0.861 →
  **0.804 → 0.886**; six-class 0.922 / 0.918 → **0.9314 / 0.926**; the
  deployment comparison 0.914 vs 0.811 → **0.9393 vs 0.8179**; and the epoch
  reading "separation after epoch 8, early stop at 14" → **best val loss 0.5009
  at epoch 17, stopped at epoch 23**.
- **The curve reading is corrected on camera**, using both loss and accuracy with
  the actual epochs and values, and the sampling-noise reading is retracted —
  the same conclusion as 6.3 and 6.3b.
- **The interface is driven live**: one image prediction whose score is read off
  the screen, one deliberately rejected slider value so the corrected interval
  control can be seen working (penalty item 2), and one video run showing the
  per-frame results. The previous recording spent about 15 seconds outside of
  slides; this one operates the app instead of describing it.
- **Narration is my own voice** (no synthesised track, no watermark), in English,
  and the total length is within the 7:30 limit.

Where waiting time was cut out, the edit is announced in the narration as the
specification requires.

---

## D. Where to look for the new evidence

| Section | What is new |
|---|---|
| 2.4b | set-aside images, the CSV decisions behind them, and the check that none are in the kept index |
| 3.4b | the model input through three resize paths, with the difference to the loader |
| 4.1b | rotation in degrees, the probability of exceeding 30° / 45°, and worst-case rotations |
| 6.3 | the curve explanation rewritten; the sampling-noise reading retracted |
| 6.3b | the controlled learning-rate retest, the split-half test, and the five conclusions |
| 6.4.1 | the pre-fix model, its actual predictions on 280 images, and the single-defect control |
| 6.4.2 | BatchNorm moving statistics against the measured batch variance (figures as before, section unchanged in substance) |
| 6.4.3 | the augmentation comparison repeated at ±14.4°, with the conclusions it does and does not support |
| 7.3 | loader vs Gradio callback probabilities for the same images |
| 8.1 | sampled-frame mosaic, per-frame confidences, the band-crop experiment, the blue-sky share |
| 8.2b, 8.4b | interface smoke tests, including rejected parameters and the returned annotated video |
| 8.3b | both change clips, the missed Overcast segment, and the snowy-segment labels |
| 9.3 | six-class errors compared with the four-class baseline |

## E. Files

| Path | Contents |
|---|---|
| `project1.ipynb` | the executed notebook, 104 cells, all outputs stored |
| `weather_lib.py` | shared helpers; `to_model_input` / `read_model_input` are new, `ROTATION` is 0.04 |
| `datasets/` | 1 479 four-class files (1 405 distinct after de-duplication), 2 703 across six classes, metadata index, source records, four- and six-class splits |
| `models/` | the four- and six-class weights plus `class_order.json` |
| `runs/history.json` | per-epoch history for every run in the notebook |
| `runs/lr_probe.json` | the 6.3b controlled retest, including the split-half losses |
| `runs/pre_fix.json` | the 6.4.1 pre-fix predictions, confusion matrix and history |
| `runs/double_scale.json` | the 6.4.1 single-defect control |
| `Reports/` | the annotated video outputs and the interface screenshots |
| `recordings/screen-recording.mp4` | the narration, 7 min 30 s limit |