# Weather Classification Notebook Review Report

- **Review time**: 2026-11-09 15:59
- **Reviewed notebook**: [project1.ipynb](../project1.ipynb)
- **Requirements**: `Project_content_requirements/`
- **Review scope**: correctness, data pipeline, model/training/evaluation, notebook quality, assignment completeness
- **Dataset status**: datasets are not prepared yet; their absence was treated as a known prerequisite, not as an independent defect

## Summary

The notebook has a reasonable staged pipeline, but it is not yet assignment-complete. The highest-priority issues concern duplicate handling, cross-label duplicate leakage, required training investigation, video probability aggregation, and six-class integration.

## Findings

### 1. Duplicate images are still used in training

- **Severity**: High
- **Location**: Cell 13; `weather_lib.py` `build_index()` / `make_split()`
- **Problem**: The notebook uses `drop_duplicates("group")` only for displayed examples:

  ```python
  kept = index.drop_duplicates("group").groupby("label").head(2)
  ```

  The original `index` is still passed to `make_split()` and then to `make_dataset()`.
- **Impact**: Duplicate copies can inflate the 250-image counts, bias training, and fail the requirement for distinct usable originals.
- **Recommendation**: Create an explicit deduplicated index, resolve cross-label groups, and use that index for counts, splitting, training, and the submitted class/split listing. Assert that each retained duplicate group has only one image unless intentionally allowed.

### 2. Cross-label duplicate conflicts can leak between training and validation

- **Severity**: High
- **Location**: Cells 13 and 17; `weather_lib.py` `make_split()`
- **Problem**: Cross-label groups are only printed:

  ```python
  print("groups filed under two classes (must be fixed by hand):", len(conflicts))
  ```

  Execution continues. The validation-coverage fallback modifies an individual row:

  ```python
  result.loc[block.index[0], "split"] = "val"
  ```

- **Impact**: Members of one duplicate group may be split across train and validation, violating the no-leakage requirement.
- **Recommendation**: Stop before splitting when cross-label groups exist, or resolve/remove those groups. Assign splits only at group level and assert that every group maps to exactly one split.

### 3. Required training investigation is not performed

- **Severity**: High
- **Location**: Cell 49
- **Problem**: The section states:

  ```python
  # Method: train nothing, just look at what the current model does
  ```

  It does not change augmentation, model architecture, or learning rate and does not compare results after a controlled change.
- **Impact**: This does not satisfy the requirement to identify an observed issue, test a change, and compare before/after results.
- **Recommendation**: Record an issue from learning curves or the confusion matrix, train a controlled variant using the same split and validation set, and report before/after metrics and representative examples.

### 4. Most-confident mistake selection is reversed

- **Severity**: Medium
- **Location**: Cell 49
- **Problem**:

  ```python
  order = np.argsort(-conf * wrong)
  worst = val_df.iloc[order[:6]]
  ```

  Ascending sort places zero-valued correct examples before the intended mistakes.
- **Impact**: The debugging section may display correctly classified images as “wrong images”.
- **Recommendation**:

  ```python
  order = np.argsort(np.where(wrong, -conf, np.inf))
  worst = val_df.iloc[order[:6]]
  ```

  Keep the selected indices aligned with the corresponding evaluation arrays.

### 5. Main-video evaluation does not expose averaged class probabilities

- **Severity**: High
- **Location**: Cells 59 and 61
- **Problem**: Cell 59 displays only the maximum probability:

  ```python
  columns=["time_s", "prediction", "probability"]
  ```

  Cell 61 returns only the modal label:

  ```python
  return str(dst), table, f"dominant weather: {dominant}"
  ```

  The available `W.mean_probability()` helper is not used.
- **Impact**: The implementation does not satisfy the requirement to sample the clip at least once per second, average class probabilities, and display all named class scores.
- **Recommendation**: Retain the full probability vector for every sampled frame, call `W.mean_probability(probs)`, display all four class averages, and derive the main label from the averaged vector.

### 6. Changing-weather sampling interval is too permissive

- **Severity**: Medium
- **Location**: Cell 65
- **Problem**:

  ```python
  gr.Slider(1, 10, value=5, step=1,
            label="max frames between samples")
  ```

- **Impact**: The interface allows values from 6 to 10 even though the requirement limits the interval to 1–5 frames.
- **Recommendation**: Set the maximum to `5` and validate `max_gap_frames` inside `analyse_change()`.

### 7. Six-class extension is not integrated into the interface

- **Severity**: High
- **Location**: Cells 71–73
- **Problem**: A six-class model is trained and evaluated, but the existing image interface remains connected to `W.CLASS_ORDER` and the four-class `deployed_model`. No updated six-class Gradio interface or complete six-class prediction demonstration is provided.
- **Impact**: Training the six-class model alone does not satisfy the requirement for updated display and actual predictions for all six classes.
- **Recommendation**: Add six-class image/video inference callbacks using `six_model` and `SIX`, display six named scores, and include representative predictions for each class plus a six-class confusion matrix.

### 8. Submission and reproducibility metadata remain placeholders

- **Severity**: High
- **Location**: Cells 0 and 9
- **Problem**: The notebook header contains placeholder links such as:

  ```text
  <...download link...>
  ```

  When `sources.csv` is absent, the notebook creates blank metadata:

  ```python
  sources["url"] = ""
  sources["licence"] = ""
  ```

- **Impact**: The submission is incomplete until actual dataset/model/file links and source/licence records are provided.
- **Recommendation**: Replace placeholders with accessible links, populate `sources.csv` with verified URLs and licences, and clearly fail or mark submission readiness when required metadata is blank.

## Recommended implementation order

1. Resolve and remove duplicate/cross-label conflicts before creating the final index.
2. Ensure group-level train/validation splitting and add leakage assertions.
3. Implement averaged class probabilities for main-video evaluation.
4. Restrict changing-weather sampling to 1–5 frames and validate the input.
5. Perform the required controlled training investigation.
6. Integrate the six-class model into image/video interfaces and demonstrations.
7. Populate dataset, model, source, and licence metadata after the datasets are prepared.

## Limitations

This was a static notebook review. Model training and video inference were not executed because the datasets are not prepared. After the data is available, rerun the notebook from a clean kernel and validate image shapes, class counts, split leakage, model output dimensions, video sampling, and Gradio callbacks.

## Overall assessment

The notebook is a useful work-in-progress, but it should not yet be treated as submission-ready. The data integrity and required interface/evaluation gaps should be fixed before final dataset preparation and final execution.
