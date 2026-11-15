"""Shared helpers for the CIS341 Project 1 weather-classification notebook.

The notebook keeps the parts the rubric asks to see (model definitions, training
calls, plots, evaluation) inline. Everything repetitive lives here: folder
scanning, near-duplicate grouping, the train/validation split, tf.data pipelines,
evaluation summaries and video sampling/annotation.

Design notes
------------
* Nothing here touches the network at import time, so the notebook stays usable
  while the dataset is still being collected.
* Functions raise a short `DataNotReady` error (or print a hint) instead of a
  bare traceback when their inputs are missing, because the dataset is filled
  in over several days. Notebook cells guard on `require()` first, so the
  normal path through the notebook is a printed hint, not an exception.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from PIL import Image

def _project_root(start: Path) -> Path:
    """Locate the folder that holds the notebook, so nothing depends on where
    the submission is unzipped. Set WEATHER_ROOT to override."""
    for candidate in (start, *start.parents):
        if (candidate / "project1.ipynb").is_file():
            return candidate
    return start


ROOT = Path(os.environ.get("WEATHER_ROOT")
            or _project_root(Path(__file__).resolve().parent))
DATA_ROOT = ROOT / "datasets" / "hand-filtered"
META_ROOT = ROOT / "datasets" / "metadata"
SPLIT_ROOT = ROOT / "datasets" / "splits"
MODEL_ROOT = ROOT / "models"
REPORT_ROOT = ROOT / "Reports"
VIDEO_ROOT = ROOT / "videos"
CACHE_ROOT = ROOT / "datasets" / "review-sheets" / "cache"

CLASS_ORDER = ["sunny", "overcast", "rainy", "snowy"]
EXTRA_CLASSES = ["foggy", "lightning"]      # six-class extension
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

CLASS_MEANING = {
    "sunny": "A visibly sunlit, mostly clear scene. Scattered clouds are acceptable.",
    "overcast": "Extensive cloud cover with mainly diffuse light.",
    "rainy": "Visible rain or convincing combined evidence of rain. "
             "A wet road alone is insufficient.",
    "snowy": "Substantial snow cover or snowfall, including snow in sunshine. "
             "Small distant patches or frost alone are insufficient.",
    "foggy": "Visibility clearly reduced by suspended droplets: washed-out "
             "distant landmarks, no rain streaks.",
    "lightning": "A visible bolt, or a sky visibly lit by a flash. "
                     "A dark sky on its own is insufficient.",
    }


class DataNotReady(RuntimeError):
    """The inputs the notebook needs are not on disk (yet).

    Raised in five situations, all of which mean "collect or curate first":
    no images at all under DATA_ROOT, one picture filed under two classes,
    a class with no validation group, a missing split file, or a video that
    cv2 cannot open. Callers in the notebook catch nothing: the message tells
    the reader what to do next, which is why it is a short sentence and not a
    traceback.
    """


# ---------------------------------------------------------------------------
# folder scanning
# ---------------------------------------------------------------------------
def class_dir(label: str) -> Path:
    return DATA_ROOT / label


def list_images(label: str) -> list[Path]:
    folder = class_dir(label)
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.iterdir()
                  if p.is_file() and p.suffix.lower() in IMAGE_EXT)


def scan_counts(labels: list[str] | None = None,
                index: pd.DataFrame | None = None) -> pd.DataFrame:
    """Per-class image counts.

    Pass `index` (from build_index) to get distinct counts as well. The brief
    counts *distinct usable originals*, so `meets_250` is based on the distinct
    number whenever it is known - a class can look full while being full of
    copies.
    """
    labels = labels or CLASS_ORDER
    rows = []
    for label in labels:
        files = list_images(label)
        sizes = {}
        for p in files:
            try:
                with Image.open(p) as im:
                    sizes[im.size] = sizes.get(im.size, 0) + 1
            except Exception:
                sizes["unreadable"] = sizes.get("unreadable", 0) + 1
        if index is not None:
            sub = index.loc[index["label"] == label]
            distinct = int(sub["group"].nunique())
            basis = "distinct"
        else:
            distinct = len(files)
            basis = "raw files (no dedupe)"
        rows.append({
            "label": label,
            "count": len(files),
            "distinct": distinct,
            "duplicates": len(files) - distinct,
            "distinct_sizes": len(sizes),
            "unreadable": sizes.get("unreadable", 0),
            "meets_250": distinct >= 250,
            "basis": basis,
        })
    return pd.DataFrame(rows)


def counts_table(index: pd.DataFrame,
                 labels: list[str] | None = None) -> pd.DataFrame:
    """Raw vs distinct per class, with a TOTAL row - the table for the report."""
    labels = labels or CLASS_ORDER
    table = scan_counts(labels, index=index)
    table = table[["label", "count", "distinct", "duplicates", "meets_250"]]
    total = pd.DataFrame([{
        "label": "TOTAL",
        "count": int(table["count"].sum()),
        "distinct": int(table["distinct"].sum()),
        "duplicates": int(table["duplicates"].sum()),
        "meets_250": bool(table["meets_250"].all()),
    }])
    return pd.concat([table, total], ignore_index=True)


# ---------------------------------------------------------------------------
# near-duplicate grouping
# ---------------------------------------------------------------------------
def _ahash(path: Path, size: int = 8) -> str:
    """Average hash: robust for overall brightness / colour layout."""
    with Image.open(path) as im:
        im = im.convert("L").resize((size, size), Image.Resampling.BILINEAR)
        arr = np.asarray(im, dtype=np.float32)
    return "".join("1" if b else "0" for b in (arr > arr.mean()).flatten())


def _dhash(path: Path, size: int = 8) -> str:
    """Difference hash: keeps the left-to-right gradient, i.e. the structure."""
    with Image.open(path) as im:
        im = im.convert("L").resize((size + 1, size), Image.Resampling.BILINEAR)
        arr = np.asarray(im, dtype=np.float32)
    return "".join("1" if b else "0" for b in (arr[:, 1:] > arr[:, :-1]).flatten())


def pixel_diff(a: Path, b: Path, size: int = 64) -> float:
    """Mean absolute difference of two greyscale thumbnails, 0-255 scale.

    Hash comparison alone groups different night photos together: a dark sky
    with one bright light produces almost the same 64-bit a/d hash whichever
    street it was taken on. Genuine duplicates in this dataset sit near 1-2;
    the false pairs measured 20-90, so this second test is decisive.
    """
    with Image.open(a) as im:
        ga = np.asarray(im.convert("L").resize((size, size),
                                              Image.Resampling.LANCZOS),
                        dtype=np.float32)
    with Image.open(b) as im:
        gb = np.asarray(im.convert("L").resize((size, size),
                                              Image.Resampling.LANCZOS),
                        dtype=np.float32)
    return float(np.abs(ga - gb).mean())


def _md5(path: Path, chunk: int = 1 << 20) -> str:
    digest = hashlib.md5()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            digest.update(block)
    return digest.hexdigest()


def _hash_cache_path() -> Path:
    CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    return CACHE_ROOT / "image_hashes.json"


def hash_all(paths: list[Path]) -> dict[str, dict]:
    """md5 + average hash + difference hash per image, cached by path+mtime."""
    cache_file = _hash_cache_path()
    cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}
    out: dict[str, dict] = {}
    changed = False
    for p in paths:
        key = str(p)
        stamp = f"{p.stat().st_mtime_ns}"
        entry = cache.get(key)
        if not (entry and entry.get("mtime") == stamp and entry.get("md5")):
            try:
                entry = {"mtime": stamp, "md5": _md5(p),
                         "ahash": _ahash(p), "dhash": _dhash(p)}
            except Exception:
                entry = {"mtime": stamp, "md5": "", "ahash": "", "dhash": ""}
            cache[key] = entry
            changed = True
        out[key] = entry
    if changed:
        cache_file.write_text(json.dumps(cache))
    return out


def _hamming(a: str, b: str) -> int:
    return sum(1 for x, y in zip(a, b) if x != y)


def build_index(labels: list[str] | None = None, dup_threshold: int = 6,
                dup_threshold_d: int | None = None,
                pixel_threshold: float = 12.0) -> pd.DataFrame:
    """One row per image with its label and a near-duplicate group id.

    Two images share a group when their bytes match exactly (md5) or when both
    their average hash and their difference hash are within `dup_threshold` bits
        of a group representative AND their greyscale thumbnails differ by no more
        than `pixel_threshold` per pixel. Requiring both hashes keeps flat-sky
        photos with similar brightness from collapsing into one giant group, which
        would throw away most of a class; the pixel test then rejects the remaining
        hash-only matches, which are mostly different night photos.

    Group ids are allocated globally (not per label) so a picture that was filed
    under two classes still lands in one group and can never be split across
    train and validation.
    """
    labels = labels or CLASS_ORDER
    dup_threshold_d = dup_threshold if dup_threshold_d is None else dup_threshold_d
    paths: list[tuple[Path, str]] = []
    for label in labels:
        paths.extend((p, label) for p in list_images(label))
    if not paths:
        raise DataNotReady(
            f"no images found under {DATA_ROOT} - collect the classes first")
    hashes = hash_all([p for p, _ in paths])

    rows: list[dict] = []
    by_md5: dict[str, str] = {}
    reps: list[dict] = []          # {"a": ahash, "d": dhash, "group": gid}
    counters: dict[str, int] = {}
    for path, label in paths:
        info = hashes.get(str(path), {})
        group = None
        if info.get("md5"):
            group = by_md5.get(info["md5"])
        if group is None and info.get("ahash"):
            for rep in reps:
                if (_hamming(info["ahash"], rep["a"]) <= dup_threshold
                                and _hamming(info["dhash"], rep["d"]) <= dup_threshold_d
                                and pixel_diff(path, rep["path"]) <= pixel_threshold):
                    group = rep["group"]
                    break
        how = "new"
        if group is not None:
            how = "md5" if info.get("md5") in by_md5 else "near"
        else:
            counters[label] = counters.get(label, 0) + 1
            group = f"{label}_{counters[label]:04d}"
            reps.append({"a": info.get("ahash", ""), "d": info.get("dhash", ""),
                                     "group": group, "path": path})
            if info.get("md5"):
                by_md5[info["md5"]] = group
        rows.append({"path": str(path), "label": label, "group": group,
                     "group_of": how, "md5": info.get("md5", ""),
                     "bytes": path.stat().st_size})
    return pd.DataFrame(rows)


def duplicate_report(index: pd.DataFrame) -> pd.DataFrame:
    """Rows that share a group with at least one other image."""
    grouped = index.groupby("group").size()
    dup_groups = grouped[grouped > 1]
    return (index[index["group"].isin(dup_groups.index)]
            .sort_values(["group", "path"])
            .assign(group_size=lambda d: d["group"].map(grouped)))


def duplicate_summary(index: pd.DataFrame) -> pd.DataFrame:
    """Counts for the 'removed duplicates' part of the report."""
    exact = index[index["md5"].duplicated(keep="first")]
    grouped = index.groupby("group").size()
    near_only = index[index["group"].isin(grouped[grouped > 1].index)
                      & ~index["md5"].duplicated(keep="first")]
    cross = cross_label_groups(index)
    return pd.DataFrame([
        {"kind": "exact duplicates (md5)", "images": int(len(exact))},
        {"kind": "near duplicates (hash group > 1)", "images": int(len(near_only))},
        {"kind": "groups spanning two classes", "images": int(len(cross))},
        {"kind": "images after removing exact duplicates",
         "images": int(len(index) - len(exact))},
    ])


def cross_label_groups(index: pd.DataFrame) -> pd.DataFrame:
    """Same/near-identical picture filed under more than one class - fix by hand."""
    span = index.groupby("group")["label"].nunique()
    bad = span[span > 1].index
    return index[index["group"].isin(bad)].sort_values(["group", "label", "path"])


def dedupe(index: pd.DataFrame, enforce_distinct: bool = True) -> pd.DataFrame:
    """One row per near-duplicate group, i.e. only distinct usable originals.

    The largest file of a group is kept as the representative, because the same
    picture often appears once at full resolution and once downscaled.

    Nothing is moved or deleted on disk: this only filters the index, so the
    folders you curated stay exactly as they are and `image_index.csv` can show
    both the original and the kept rows.

    Raises `DataNotReady` when one group is filed under two classes, because
    that is a labelling decision only a human can make.
    """
    conflicts = cross_label_groups(index)
    if len(conflicts) and enforce_distinct:
        pairs = conflicts.groupby("group")["label"].apply(
            lambda s: " vs ".join(sorted(set(s)))).head(5)
        raise DataNotReady(
            "one picture is filed under different classes; resolve these first:\n"
            + "\n".join(f"  {gid}: {pair}" for gid, pair in pairs.items())
            + "\n  rows: " + ", ".join(conflicts["path"].head(5)))

    ordered = index.sort_values(["group", "bytes", "path"],
                                ascending=[True, False, True])
    return ordered.drop_duplicates("group").reset_index(drop=True)


# ---------------------------------------------------------------------------
# train / validation split
# ---------------------------------------------------------------------------
def make_split(index: pd.DataFrame, val_fraction: float = 0.2,
               seed: int = 341) -> pd.DataFrame:
    """Group-aware stratified split: a whole duplicate group lands in one side."""
    rng = np.random.default_rng(seed)
    sizes = index.groupby("group").size()
    primary = index.groupby("group")["label"].agg(lambda s: s.mode().iat[0])

    side_of: dict[str, str] = {}
    for label, names in primary.groupby(primary):
        names = list(names.index)
        order = rng.permutation(len(names))
        target = max(1, round(int(sizes[names].sum()) * val_fraction))
        taken = 0
        for i in order:
            name = names[i]
            side = "val" if taken < target else "train"
            side_of[name] = side
            if side == "val":
                taken += int(sizes[name])

    result = index.assign(split=index["group"].map(side_of)).copy()
    # Every label gets at least one group on the validation side because the
    # first group of each label is taken with `taken == 0 < target`. If that
    # ever stops holding, fail loudly instead of moving a single row, which
    # would split a duplicate group across the two sets.
    uncovered = [label for label, block in result.groupby("label")
                 if not (block["split"] == "val").any()]
    if uncovered:
        raise DataNotReady(
            f"no validation images for: {uncovered} - each class needs at "
            "least two duplicate groups")
    return result.sort_values(["label", "split", "path"]).reset_index(drop=True)


def save_split(split: pd.DataFrame, name: str = "four_class_split.csv") -> Path:
    SPLIT_ROOT.mkdir(parents=True, exist_ok=True)
    path = SPLIT_ROOT / name
    # 寫成相對於 ROOT 的路徑，換一台機器解壓縮後才不會全部指向原本的磁碟。
    out = split.copy()
    out["path"] = [str(Path(p).resolve().relative_to(ROOT)) if _under(p)
                   else str(p) for p in split["path"]]
    out.to_csv(path, index=False)
    return path


def _under(raw) -> bool:
    try:
        Path(raw).resolve().relative_to(ROOT)
        return True
    except (ValueError, OSError):
        return False


def _anchor(raw) -> str:
    """Normalise one stored path to a single spelling and base folder."""
    p = Path(raw)
    if not p.is_absolute():
        p = ROOT / p
    try:
        return str(ROOT / p.resolve().relative_to(ROOT))
    except (ValueError, OSError):
        return str(p)


def load_split(name: str = "four_class_split.csv") -> pd.DataFrame:
    path = SPLIT_ROOT / name
    if not path.exists():
        raise DataNotReady(f"split file missing: {path} - run make_split first")
    split = pd.read_csv(path)
    split["path"] = [_anchor(p) for p in split["path"]]
    return split


# ---------------------------------------------------------------------------
# preprocessing contracts
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class PreprocessSpec:
    name: str
    image_size: tuple[int, int]
    scale: str
    # float32 array/tensor in 0..255 -> model input. Typed as Callable so
    # Pylance does not treat the field as plain `object` and flag every
    # call site with "object is not callable".
    fn: Callable[[Any], Any]
    note: str


def _identity(x):
    return x


def _rescale(x):
    return x / 255.0


def _mobilenet_v2(x):
    """mobilenet_v2.preprocess_input, but never mutating the caller's array.

    Keras implements this as ``x /= 127.5; x -= 1.0`` and returns the *same*
    object, so a numpy argument is modified in place. Copying first keeps
    ``spec.fn`` a pure function: passing the same array twice must not change
    the answer, and callers that reuse a frame buffer stay correct.
    """
    import tensorflow as tf

    if isinstance(x, np.ndarray):
        x = x.copy()
    return tf.keras.applications.mobilenet_v2.preprocess_input(x)


def _efficientnet(x):
    import tensorflow as tf
    return tf.keras.applications.efficientnet.preprocess_input(x)


def spec_for(kind: str) -> PreprocessSpec:
    if kind == "scratch":
        return PreprocessSpec(
            name="scratch",
            image_size=(128, 128),
            scale="float32, divided by 255 -> [0, 1]",
            fn=_rescale,
            note="RGB channel order. The models contain no scaling layer, so "
                 "this function is the only place pixels are divided by 255; "
                 "make_dataset, predict_frames and the Gradio callbacks all "
                 "call it and nothing else may repeat the division.",
        )
    if kind == "mobilenet_v2":
        return PreprocessSpec(
            name="mobilenet_v2",
            image_size=(224, 224),
            scale="float32, mobilenet_v2.preprocess_input -> [-1, 1]",
            fn=_mobilenet_v2,
            note="The backbone does NOT include scaling. This function is the "
                 "only place preprocess_input is applied - the model itself "
                 "starts at the backbone input, because applying it twice maps "
                 "every pixel to about -1.0.",
        )
    if kind == "efficientnet":
        return PreprocessSpec(
            name="efficientnet",
            image_size=(224, 224),
            scale="float32, efficientnet.preprocess_input (no manual /255)",
            fn=_efficientnet,
            note="EfficientNet rescales inside the model; do not divide by 255 twice.",
        )
    raise ValueError(f"unknown preprocessing kind: {kind}")


# ---------------------------------------------------------------------------
# tf.data pipelines
# ---------------------------------------------------------------------------
def make_dataset(df: pd.DataFrame, spec: PreprocessSpec, batch_size: int = 32,
                 shuffle: bool = False, augment=None, seed: int = 341,
                 labels: list[str] | None = None):
    """Build a batched tf.data pipeline from a split dataframe.

    `spec.fn` is the single place where pixels are scaled. The Keras models in
    the notebook deliberately contain no Rescaling or preprocess_input layer, so
    the preprocessing happens exactly once and training, video inference and the
    Gradio callbacks all see identical input.
    """
    import tensorflow as tf

    labels = labels or CLASS_ORDER
    label_to_id = {name: i for i, name in enumerate(labels)}
    paths = df["path"].astype(str).to_numpy()
    y = np.array([label_to_id[label] for label in df["label"]], dtype=np.int32)

    ds = tf.data.Dataset.from_tensor_slices((paths, y))

    def _load(path, label):
        raw = tf.io.read_file(path)
        img = tf.io.decode_image(raw, channels=3, expand_animations=False)
        img = tf.image.resize(img, spec.image_size, method="bilinear")
        img = tf.cast(img, tf.float32)
        return img, label

    ds = ds.map(_load, num_parallel_calls=tf.data.AUTOTUNE)
    if shuffle:
        ds = ds.shuffle(min(len(df), 2000), seed=seed,
                        reshuffle_each_iteration=True)
    if augment is not None:
        # tf.data hands us single images; the Keras preprocessing layers need a
        # batch axis, so add one, run the augmenter, then squeeze it back.
        def _augment(x, y_):
            batched = tf.expand_dims(x, 0)
            out = augment(batched, training=True)
            return tf.squeeze(out, 0), y_

        ds = ds.map(_augment, num_parallel_calls=tf.data.AUTOTUNE)
    ds = ds.map(lambda x, y_: (spec.fn(x), y_),
                num_parallel_calls=tf.data.AUTOTUNE)
    return ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)


def dataset_summary(ds) -> pd.DataFrame:
    """Peek one batch and report shape / dtype / range for the record."""
    import tensorflow as tf
    images, labels = next(iter(ds))
    images = tf.convert_to_tensor(images)
    return pd.DataFrame([{
        "images_shape": tuple(images.shape),
        "images_dtype": str(images.dtype.name),
        "images_min": float(tf.reduce_min(images)),
        "images_max": float(tf.reduce_max(images)),
        "labels_shape": tuple(labels.shape),
        "labels_dtype": str(labels.dtype.name),
        "labels_seen": sorted({int(v) for v in np.asarray(labels).ravel()}),
    }])


# ---------------------------------------------------------------------------
# augmentation
# ---------------------------------------------------------------------------
def make_augmenter(seed: int = 341, strength: float = 0.15):
    """Plausible weather-photo variation only: no vertical flip, no hue swap.

    * horizontal flip     - cameras are held either way; weather is symmetric
    * small rotation/zoom - handheld framing
    * brightness/contrast - exposure differences between cameras and days
    * saturation jitter    - sensor and white-balance differences

    Cropping is kept gentle (<=10%) so snow cover and rain streaks stay visible.
    Keras 3.1 has no RandomSaturation layer, so the jitter is our own layer.
    """
    import keras
    from keras import layers

    class SaturationJitter(layers.Layer):
        """Multiply saturation by a random factor; no-op outside training."""

        def __init__(self, low: float = 0.85, high: float = 1.15, **kwargs):
            super().__init__(**kwargs)
            self.low, self.high = low, high

        def build(self, input_shape):
            super().build(input_shape)

        def call(self, inputs, training=None):
            import tensorflow as tf
            if not training:
                return inputs
            factor = tf.random.uniform((), self.low, self.high)
            return tf.clip_by_value(tf.image.adjust_saturation(inputs, factor),
                                    0.0, 255.0)

        def get_config(self):
            return {**super().get_config(), "low": self.low, "high": self.high}

    return keras.Sequential(
        [
            layers.RandomFlip("horizontal", seed=seed),
            layers.RandomRotation(strength, fill_mode="reflect", seed=seed),
            layers.RandomZoom((-0.10, 0.10), fill_mode="reflect", seed=seed),
            layers.RandomBrightness(0.12, value_range=(0, 255), seed=seed),
            layers.RandomContrast(0.15, seed=seed),
            SaturationJitter(0.85, 1.15),
        ],
        name="weather_augmenter",
    )


def raw_batch(df: pd.DataFrame, image_size: tuple[int, int] = (128, 128),
              n: int = 8, seed: int = 341):
    """A small batch of float32 images in 0..255, i.e. before any scaling.

    The augmenter is defined in pixel units so brightness/contrast changes mean
    the same thing for every model; the preview therefore reads raw pixels.
    """
    import tensorflow as tf

    sub = df.sample(min(n, len(df)), random_state=seed) if len(df) > n else df
    images = []
    for path in sub["path"]:
        raw = tf.io.read_file(str(path))
        img = tf.io.decode_image(raw, channels=3, expand_animations=False)
        img = tf.image.resize(img, image_size, method="bilinear")
        images.append(tf.cast(img, tf.float32))
    return tf.stack(images), sub.reset_index(drop=True)


def sample_per_class(df: pd.DataFrame, per_class: int = 1,
                     labels: list[str] | None = None,
                     seed: int = 341) -> pd.DataFrame:
    """Take up to `per_class` rows from every class, in class order.

    The brief asks for augmentation previews *from every class*, so a plain
    `df.sample(n)` is not enough: with four balanced classes a six-image draw
    misses at least one class about 62% of the time. Sampling per group makes
    the coverage deterministic, and the caller can assert it.
    """
    if df is None or df.empty:
        return df
    order = labels or [c for c in CLASS_ORDER if c in set(df["label"])]
    picks = []
    for label in order:
        block = df[df["label"] == label]
        if block.empty:
            continue
        picks.append(block.sample(min(per_class, len(block)), random_state=seed))
    if not picks:
        return df.iloc[0:0]
    return pd.concat(picks).reset_index(drop=True)


def augment_preview(images, augmenter, rounds: int = 1):
    """Original batch plus `rounds` independent augmented draws of it.

    Two draws from the same picture show what the random augmentation actually
    varies (crop, flip, brightness) instead of implying it is deterministic.
    """
    originals = np.asarray(images)
    draws = [np.asarray(augmenter(images, training=True))
             for _ in range(max(1, rounds))]
    return originals, draws


# ---------------------------------------------------------------------------
# evaluation
# ---------------------------------------------------------------------------
def evaluate_model(model, ds, labels: list[str] | None = None) -> dict:
    from sklearn.metrics import (classification_report, confusion_matrix,
                                 accuracy_score)
    labels = labels or CLASS_ORDER
    y_true, y_prob = [], []
    for images, y in ds:
        y_prob.append(np.asarray(model.predict(images, verbose=0)))
        y_true.append(np.asarray(y))
    prob = np.concatenate(y_prob)
    true = np.concatenate(y_true)
    pred = prob.argmax(axis=1)
    cm = confusion_matrix(true, pred, labels=range(len(labels)))
    return {
        "accuracy": float(accuracy_score(true, pred)),
        "confusion_matrix": cm,
        "report": classification_report(true, pred,
                                        labels=range(len(labels)),
                                        target_names=labels, digits=3,
                                        zero_division=0),
        "y_true": true,
        "y_pred": pred,
        "y_prob": prob,
    }


def confusion_table(cm, labels: list[str] | None = None) -> pd.DataFrame:
    labels = labels or CLASS_ORDER
    df = pd.DataFrame(cm, index=[f"true_{l}" for l in labels],
                      columns=[f"pred_{l}" for l in labels])
    df["row_total"] = df.sum(axis=1)
    return df


# ---------------------------------------------------------------------------
# video helpers
# ---------------------------------------------------------------------------
def video_info(path: str | Path) -> dict:
    import cv2
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise DataNotReady(f"cannot open video: {path}")
    info = {
        "path": str(path),
        "fps": cap.get(cv2.CAP_PROP_FPS),
        "frames": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    }
    info["duration_s"] = (info["frames"] / info["fps"]) if info["fps"] else 0.0
    cap.release()
    return info


def sample_frames(path: str | Path, every_seconds: float = 1.0,
                  max_frames: int | None = None) -> list[tuple[float, np.ndarray]]:
    """Sample the whole clip at a fixed interval; returns (timestamp, RGB frame)."""
    import cv2
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise DataNotReady(f"cannot open video: {path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    step = max(1, int(round(fps * every_seconds)))
    frames, idx = [], 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % step == 0:
            frames.append((idx / fps, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            if max_frames and len(frames) >= max_frames:
                break
        idx += 1
    cap.release()
    return frames


def predict_frames(model, frames: list[tuple[float, np.ndarray]],
                   spec: PreprocessSpec, batch_size: int = 8
                   ) -> tuple[np.ndarray, list[float]]:
    """Return per-frame probabilities and their timestamps."""
    if not frames:
        return np.zeros((0, 1)), []
    batch = np.stack([np.asarray(Image.fromarray(f).resize(spec.image_size))
                      for _, f in frames]).astype("float32")
    batch = np.asarray(spec.fn(batch))
    probs = model.predict(batch, batch_size=batch_size, verbose=0)
    return probs, [t for t, _ in frames]


def mean_probability(probs: np.ndarray) -> np.ndarray:
    return probs.mean(axis=0) if len(probs) else np.zeros(0)


def mean_scores(labels: list[str], probs: np.ndarray) -> dict[str, float]:
    """Average probability per named class - what the brief asks us to report."""
    mean = mean_probability(probs)
    if len(mean) != len(labels):
        return {}
    return {name: float(p) for name, p in zip(labels, mean)}


def dominant_from_mean(labels: list[str], probs: np.ndarray) -> tuple[str, dict]:
    """Class with the largest mean probability, plus all averaged scores."""
    scores = mean_scores(labels, probs)
    if not scores:
        return "n/a", {}
    # Index the dict directly: dict.get returns float | None, which is not a
    # type max() can compare. Same fix as the notebook's Gradio callbacks.
    return max(scores, key=lambda k: scores[k]), scores


# class colours (BGR for OpenCV)
CLASS_BGR = {
    "sunny": (60, 180, 245),
    "overcast": (200, 200, 200),
    "rainy": (240, 130, 60),
    "snowy": (255, 255, 255),
    "foggy": (200, 170, 130),
        "lightning": (30, 240, 255),
}


def _open_video_writer(out_path: Path, fps: float, size: tuple[int, int]):
    """Open a VideoWriter that produces a browser-playable H.264 file.

    OpenCV's default `mp4v` fourcc writes MPEG-4 Part 2, which VS Code and every
    browser refuse to play. H.264 (`avc1`) is the format the brief's sample clips
    use, so we ask for it first. Two fallbacks keep the function total:

    1. `H264` via the MSMF backend (uses the Windows Media Foundation encoder).
    2. `avc1` via the default backend (works when a system H.264 encoder exists).
    3. `mp4v` as a last resort, so the notebook still produces a file.

    The returned writer is already released-safe; callers only need `release()`.
    """
    import cv2
    fourcc = getattr(cv2, "VideoWriter_fourcc")
    attempts = (
        ("H264", cv2.CAP_MSMF),
        ("avc1", cv2.CAP_ANY),
        ("mp4v", cv2.CAP_ANY),
    )
    for tag, backend in attempts:
        writer = cv2.VideoWriter(str(out_path), backend, fourcc(*tag),
                                 fps, size)
        if writer.isOpened():
            if tag == "mp4v":
                print(f"[warn] {out_path.name}: H.264 encoder unavailable, "
                      f"fell back to mp4v (may not play in browsers)")
            return writer
        writer.release()
    raise DataNotReady(f"no usable video encoder for {out_path}")


def annotate_video(src: str | Path, dst: str | Path, model, spec: PreprocessSpec,
                   labels: list[str] | None = None, every_seconds: float = 1.0,
                   hold_note: str = "held") -> dict:
    """Write an annotated copy of `src`.

    Every output frame is preserved with the original timing. Between model calls
    the most recent prediction stays on screen ("held"), which is what the brief
    asks for. Returns a summary dict for the notebook to display.
    """
    import cv2
    labels = labels or CLASS_ORDER
    cap = cv2.VideoCapture(str(src))
    if not cap.isOpened():
        raise DataNotReady(f"cannot open video: {src}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    step = max(1, int(round(fps * every_seconds)))

    out_path = Path(dst)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    writer = _open_video_writer(out_path, fps, (w, h))

    current = None          # (label, prob)
    timeline: list[tuple[float, str, float]] = []
    sampled: list[np.ndarray] = []
    idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % step == 0:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            arr = np.asarray(Image.fromarray(rgb).resize(spec.image_size),
                             dtype="float32")[None, ...]
            probs = model.predict(np.asarray(spec.fn(arr)), verbose=0)[0]
            sampled.append(np.asarray(probs, dtype="float64"))
            k = int(np.argmax(probs))
            current = (labels[k], float(probs[k]))
            timeline.append((idx / fps, labels[k], float(probs[k])))
        if current is not None:
            name, prob = current
            colour = CLASS_BGR.get(name, (255, 255, 255))
            cv2.rectangle(frame, (0, 0), (w, 46), (25, 25, 25), -1)
            cv2.putText(frame, f"{name}  {prob * 100:.1f}%  ({hold_note})",
                        (12, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.9, colour, 2,
                        cv2.LINE_AA)
            bar_w = int((w - 24) * prob)
            cv2.rectangle(frame, (12, 40), (12 + bar_w, 44), colour, -1)
            cv2.putText(frame, f"t={idx / fps:5.2f}s", (w - 130, 32),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1,
                        cv2.LINE_AA)
        writer.write(frame)
        idx += 1
    cap.release()
    writer.release()
    prob_matrix = (np.vstack(sampled) if sampled
                   else np.zeros((0, len(labels))))
    main_label, scores = dominant_from_mean(labels, prob_matrix)
    return {
        "output": str(out_path),
        "frames_written": idx,
        "fps": fps,
        "predictions": len(timeline),
        "interval_s": every_seconds,
        "timeline": timeline,          # kept for the changing-weather cells
        "class_order": list(labels),
        "prob_matrix": prob_matrix,    # one row per sampled frame
        "timestamps": [t for t, _, _ in timeline],
        "mean_scores": scores,
        "main_label": main_label,
    }


# ---------------------------------------------------------------------------
# misc
# ---------------------------------------------------------------------------
def ensure_dirs() -> None:
    for path in (META_ROOT, SPLIT_ROOT, MODEL_ROOT, REPORT_ROOT, CACHE_ROOT):
        path.mkdir(parents=True, exist_ok=True)


def save_json(obj, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, default=str))
    return path


def load_json(path: str | Path):
    return json.loads(Path(path).read_text())


def human_time(seconds: float) -> str:
    m, s = divmod(int(round(seconds)), 60)
    return f"{m}m {s}s" if m else f"{s}s"


def bits_of_training(histories: dict) -> pd.DataFrame:
    """Compare two Keras History objects on the metrics the rubric asks about."""
    rows = []
    for name, hist in histories.items():
        h = hist.history
        best_epoch = int(np.argmin(h["val_loss"])) + 1
        rows.append({
            "model": name,
            "epochs_run": len(h["loss"]),
            "best_epoch": best_epoch,
            "train_loss@best": round(float(h["loss"][best_epoch - 1]), 4),
            "val_loss@best": round(float(h["val_loss"][best_epoch - 1]), 4),
            "val_acc@best": round(float(h["val_accuracy"][best_epoch - 1]), 4),
            "final_train_acc": round(float(h["accuracy"][-1]), 4),
            "overfit_gap": round(float(h["accuracy"][-1]
                                       - h["val_accuracy"][-1]), 4),
        })
    return pd.DataFrame(rows)