# Notebook Non-Dataset Requirements Review

- **Review time**: 2026-11-09 22:06
- **Reviewed notebook**: [project1.ipynb](../project1.ipynb)
- **Scope**: non-dataset requirements and pure workflow logic
- **Explicit exclusions**:
  - Dataset availability, quantity, labels, distribution, and quality
  - Low accuracy or incorrect predictions caused by unfinished data
  - Submission links, `sources.csv`, licences, and reproducibility metadata

## Important correction

The previous review incorrectly treated low accuracy and video predictions as defects. Because the dataset is not ready, those observations cannot establish a notebook logic problem. They are excluded from this corrected report.

The preprocessing concern is also not classified as a confirmed defect until the dataset/model preprocessing contract is verified.

## Confirmed findings

### 1. Six-class section is not completed

- **Severity**: High
- **Location**: Cells 71, 73, and 75
- **Evidence**: The six-class training, validation, and prediction sections remain marked `[pending]`.
- **Impact**: The six-class requirement is not demonstrated in the current notebook execution.
- **Recommendation**: After the six-class dataset is prepared, execute training, validation, predictions, class comparison, and the updated six-class interface. This is a completeness issue, not an accuracy issue.

### 2. Gradio interfaces are not demonstrated in the notebook

- **Severity**: Medium
- **Location**: Cells 55, 61, and 65
- **Evidence**: The interface launch calls are commented out, and there are no recorded interface smoke-test outputs.
- **Impact**: The notebook does not provide execution evidence that the image, main-video, and changing-weather interfaces are wired and usable.
- **Recommendation**: After data and models are ready, execute representative smoke tests for each interface and preserve the resulting outputs or screenshots. This should verify callback wiring and display formatting rather than judge model accuracy.

### 3. Augmentation preview does not guarantee per-class coverage

- **Severity**: Medium
- **Location**: Cell 29
- **Evidence**: The preview randomly selects six training images:

  ```python
  raw_batch(train_df, ..., n=6)
  ```

  There is no per-class selection or assertion.
- **Impact**: Even with a valid dataset, a random sample may omit one or more classes, so the required demonstration may be incomplete.
- **Recommendation**: Select examples by label and assert that every required class is represented before plotting. This finding concerns demonstration logic, not the current data contents.

## Not findings

The following are intentionally not reported as defects:

- Low scratch-model or transfer-learning accuracy
- `sunny` video being predicted as `rainy`
- Changing-weather output containing no detected transitions
- Any model behavior that depends on the unfinished dataset
- Preprocessing double-application, pending confirmation of the input preprocessing contract

## Limitations

This report does not determine whether the final model will achieve a particular accuracy. Once the dataset is finalized, rerun the notebook and perform a separate data/model performance review.

## Overall assessment

The non-dataset workflow is mostly structured, but the six-class section is not completed and the Gradio interfaces lack execution evidence. The augmentation preview should be made class-complete. No dataset-dependent model-performance issue is asserted in this corrected report.
