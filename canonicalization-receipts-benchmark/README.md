# Canonicalization Receipts + Reproducibility Benchmark

Concrete repo for the gap:

```text
receipt(upside_down, raw_hash, canonical_hash, confidence)
```

The previous receipt shape kept transform booleans but dropped the confidence value. This package surfaces confidence in the public receipt.

## Detects

- reversed text
- upside-down / mirrored-style text
- Unicode bidi override controls
- homoglyph substitutions
- mixed cases

## Public receipt shape

```text
raw_text
canonical_text
raw_hash
canonical_hash
transform_receipt
confidence
arbitration_trace
lossless
receipt_version
```

## Why it matters

This is a pre-tokenization instrumentation layer. Weird raw input becomes canonical context before expensive LLM inference, while raw weirdness remains auditable through the raw hash and transform receipt.

It is useful for token-cost reduction, prompt-cache stability, anti-spoofing receipts, reproducible canonicalization, multimodal text cleanup, and forensic handling of reversed/upside-down/bidi/homoglyph input.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
python benchmarks/run_benchmark.py
```

## CLI

```bash
canon-receipt "dlrow olleh"
canon-receipt "plɹoʍ ollǝɥ"
canon-receipt "abc\u202edef"
canon-receipt "раураl account"
```

## Prototype appraisal

Target prototype appraisal: **$3,000** replacement-cost / sellable-MVP estimate. This is not guaranteed market price.

## Boundary

This is not GPT and not a universal OCR/vision solver. It is a canonicalization receipt engine for text-like inputs before tokenization.
