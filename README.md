# Beyond Baskets: Sequence-Aware Conversion Intelligence in OTTO E-Commerce Sessions

[YouTube link — https://youtu.be/UotgMGpr-zM]

👉 Start here: `main_notebook.ipynb`

**Author:** Bhaumik Patel · UIN 737002364 · CSCE 676 · Spring 2026 · Texas A&M University

## 1. Project Overview

This project compares basket-based co-occurrence methods with sequence-aware pattern mining on the OTTO e-commerce dataset. Specifically, it studies how **FP-Growth** and **association rules** differ from **PrefixSpan** when the same shopping sessions are treated either as unordered baskets or as ordered behavioral sequences. The central finding is that preserving session order reveals high-intent behavioral structure that basket-based views miss, especially around directional item relationships and purchase-funnel behavior.

## 2. Main Notebook

The main deliverable for this repository is `main_notebook.ipynb`.

## 3. Research Questions

**Primary question**

- Do sequence-aware methods reveal high-intent behavioral structure that basket-based methods fail to capture?

**Supporting analyses**

- How do different minimum support thresholds change the frequent itemsets recovered by FP-Growth?
- How do confidence and lift emphasize different kinds of association rules in OTTO session baskets?

## 4. Project Video

- Video walkthrough: [YouTube link — TODO]

## 5. Data

This project uses the **OTTO Recommender System** dataset from Kaggle:

- <https://www.kaggle.com/competitions/otto-recommender-system/data>

The raw training file is too large to commit, so download instructions and placement details live in `data/README.md`. Cached artifacts are already included in the repo so the notebook can still be reviewed without the 11 GB training file.

## 6. How to Reproduce

This work was developed in **Google Colab (Python 3.11)**.

1. Create a Python 3.11 environment locally or open the notebook in Colab.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Optional: download `otto-recsys-train.jsonl` from Kaggle and place it in the repo root as described in `data/README.md`.
4. Optional: regenerate the cached artifacts:
   ```bash
   python scripts/full_scan.py --train otto-recsys-train.jsonl
   python scripts/build_sample.py --train otto-recsys-train.jsonl
   ```
5. Open `main_notebook.ipynb` and run the notebook. If the raw training file is absent, the notebook uses the committed cache files when available.

## 7. Key Dependencies and Versions

| Dependency | Version |
| --- | --- |
| Python | 3.11 |
| numpy | >=1.26.0 |
| pandas | >=2.2.0 |
| matplotlib | >=3.8.0 |
| scipy | >=1.11.0 |
| mlxtend | >=0.23.0 |
| prefixspan | >=0.5.2 |
| ipython | >=8.18.0 |

The complete environment specification is in `requirements.txt`.

## 8. Repo Structure

```text
.
├── README.md
├── .gitignore
├── requirements.txt
├── main_notebook.ipynb
├── otto_full_scan_summary.json
├── otto_sample_20k.pkl
├── data/
│   └── README.md
├── checkpoints/
│   ├── checkpoint_1.ipynb
│   └── checkpoint_2.ipynb
└── scripts/
    ├── build_sample.py
    └── full_scan.py
```

## 9. Results Summary

The sequence-aware view adds meaningful structure beyond what basket-based mining can show. In the top basket pairs, **66.7%** are directional rather than symmetric, and **4 of 12** tested top pairs show statistically significant directional imbalance. Sessions that end in orders are enriched for purchase-funnel subsequences such as `clicks -> carts -> orders`, and PrefixSpan recovers **100%** of the top FP-Growth item pairs while also exposing the directional ordering those baskets hide.
