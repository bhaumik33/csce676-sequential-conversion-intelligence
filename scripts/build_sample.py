from __future__ import annotations

import argparse
import json
import pickle
import random
from pathlib import Path


def reservoir_sample_jsonl(path: Path, sample_size: int, seed: int) -> list[dict]:
    random.seed(seed)
    reservoir: list[dict] = []

    with path.open("r", encoding="utf-8") as handle:
        for index, line in enumerate(handle):
            if not line.strip():
                continue

            obj = json.loads(line)
            if index < sample_size:
                reservoir.append(obj)
            else:
                replacement_index = random.randint(0, index)
                if replacement_index < sample_size:
                    reservoir[replacement_index] = obj

    if len(reservoir) < sample_size:
        print(
            f"Warning: requested {sample_size} sessions but only found {len(reservoir)}."
        )

    return reservoir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reservoir-sample OTTO sessions and write a pickle cache."
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
        default=Path("otto_sample_20k.pkl"),
        help="Output path for the sampled-session pickle",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=20_000,
        help="Number of sessions to sample",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reservoir sampling",
    )
    args = parser.parse_args()

    sessions = reservoir_sample_jsonl(args.train, args.sample_size, args.seed)
    args.output.write_bytes(pickle.dumps(sessions, protocol=pickle.HIGHEST_PROTOCOL))
    print(f"Wrote {len(sessions)} sampled sessions to {args.output}")


if __name__ == "__main__":
    main()
