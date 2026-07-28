from __future__ import annotations

import json
import time
from pathlib import Path

from canon_receipts import compute_fingerprint

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "benchmarks" / "cases.jsonl"
OUT_PATH = ROOT / "receipts" / "benchmark_receipt.json"


def main() -> None:
    start = time.perf_counter()
    total = 0
    passed = 0
    rows = []
    for line in CASES_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        case = json.loads(line)
        total += 1
        receipt = compute_fingerprint(case["input"])
        ok = receipt.canonical_text == case["expected"]
        passed += int(ok)
        rows.append({
            "id": case["id"],
            "ok": ok,
            "input": case["input"],
            "expected": case["expected"],
            "canonical": receipt.canonical_text,
            "raw_hash": receipt.raw_hash,
            "canonical_hash": receipt.canonical_hash,
            "transform_receipt": receipt.transform_receipt,
            "confidence": receipt.confidence,
            "lossless": receipt.lossless,
        })
    result = {
        "benchmark": "canonicalization_receipts_reproducibility",
        "total": total,
        "passed": passed,
        "accuracy": passed / total if total else 0,
        "elapsed_ms": round((time.perf_counter() - start) * 1000, 3),
        "rows": rows,
    }
    OUT_PATH.parent.mkdir(exist_ok=True)
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: result[k] for k in ["benchmark", "total", "passed", "accuracy", "elapsed_ms"]}, indent=2))
    if passed != total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
