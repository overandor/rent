from __future__ import annotations

import argparse
from pathlib import Path

from .fingerprint import compute_fingerprint


def main() -> None:
    parser = argparse.ArgumentParser(description="Canonicalize weird text and emit a transform receipt.")
    parser.add_argument("text", nargs="*")
    parser.add_argument("--file", type=Path)
    parser.add_argument("--canonical-only", action="store_true")
    args = parser.parse_args()

    text = args.file.read_text(encoding="utf-8") if args.file else " ".join(args.text)
    receipt = compute_fingerprint(text)
    print(receipt.canonical_text if args.canonical_only else receipt.to_json())


if __name__ == "__main__":
    main()
