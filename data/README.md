# Data

This project uses the **OTTO Recommender System** dataset from Kaggle:

- Kaggle competition page: <https://www.kaggle.com/competitions/otto-recommender-system/data>

## How to download

1. Sign in to Kaggle.
2. Open the OTTO competition data page.
3. Download the training file `otto-recsys-train.jsonl`.

## Where to place the file

For the notebook to run without any path edits, place the downloaded file in the **repo root**:

```text
./otto-recsys-train.jsonl
```

The file is intentionally excluded from version control because it is about 11 GB.

## Cached artifacts included in this repo

This repository already includes two cached artifacts so reviewers can open and run the notebook without downloading the full training file:

- `otto_full_scan_summary.json` — full-dataset summary statistics
- `otto_sample_20k.pkl` — 20,000-session sample used for the notebook analyses

If you do download the raw training file, you can regenerate those caches with:

```bash
python scripts/full_scan.py --train otto-recsys-train.jsonl
python scripts/build_sample.py --train otto-recsys-train.jsonl
```
