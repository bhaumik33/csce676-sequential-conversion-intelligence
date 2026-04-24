from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np


def scan_train_file(train_path: Path) -> dict:
    event_type_counts: Counter[str] = Counter()
    item_counts: Counter[int] = Counter()
    session_lengths: list[int] = []
    n_sessions = 0
    n_events = 0

    with train_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue

            try:
                session = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}") from exc

            events = session.get("events", [])
            session_lengths.append(len(events))
            n_sessions += 1
            n_events += len(events)

            for event in events:
                event_type_counts[event["type"]] += 1
                item_counts[int(event["aid"])] += 1

    if not session_lengths:
        raise ValueError("No sessions were read from the training file.")

    lengths = np.asarray(session_lengths, dtype=np.int64)
    n_items = len(item_counts)
    top_10_count = sum(count for _, count in item_counts.most_common(10))
    top_1pct_k = max(1, math.ceil(n_items * 0.01))
    top_1pct_count = sum(count for _, count in item_counts.most_common(top_1pct_k))

    return {
        "n_sessions": int(n_sessions),
        "n_events": int(n_events),
        "n_items": int(n_items),
        "event_type_counts": dict(event_type_counts),
        "event_type_props": {
            key: value / n_events for key, value in event_type_counts.items()
        },
        "session_length_summary": {
            "mean": float(lengths.mean()),
            "median": float(np.median(lengths)),
            "p25": float(np.percentile(lengths, 25)),
            "p75": float(np.percentile(lengths, 75)),
            "p95": float(np.percentile(lengths, 95)),
            "p99": float(np.percentile(lengths, 99)),
            "max": int(lengths.max()),
        },
        "top10_share": top_10_count / n_events,
        "top1pct_share": top_1pct_count / n_events,
        "top20_items": [[aid, count] for aid, count in item_counts.most_common(20)],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stream the OTTO training file and write summary statistics."
    )
    parser.add_argument(
        "--train",
        required=True,
        type=Path,
        help="Path to otto-recsys-train.jsonl",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("otto_full_scan_summary.json"),
        help="Output path for the summary JSON cache",
    )
    args = parser.parse_args()

    summary = scan_train_file(args.train)
    args.output.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote full-scan summary to {args.output}")


if __name__ == "__main__":
    main()
