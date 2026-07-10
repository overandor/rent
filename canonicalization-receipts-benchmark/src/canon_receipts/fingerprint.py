from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re
import unicodedata
from typing import Any

BIDI_CONTROLS = {"\u202a", "\u202b", "\u202c", "\u202d", "\u202e", "\u2066", "\u2067", "\u2068", "\u2069", "\u200e", "\u200f"}
HOMOGLYPHS = {
    "а": "a", "А": "A", "е": "e", "Е": "E", "о": "o", "О": "O", "р": "p", "Р": "P",
    "с": "c", "С": "C", "у": "y", "У": "Y", "х": "x", "Х": "X", "і": "i", "І": "I",
    "ј": "j", "Ј": "J", "ѕ": "s", "Ѕ": "S", "ӏ": "l", "Ӏ": "I", "ρ": "p", "ο": "o", "α": "a",
}
UP_TO_DOWN = {
    "a": "ɐ", "b": "q", "c": "ɔ", "d": "p", "e": "ǝ", "f": "ɟ", "g": "ƃ", "h": "ɥ", "i": "ᴉ",
    "j": "ɾ", "k": "ʞ", "l": "ן", "m": "ɯ", "n": "u", "o": "o", "p": "d", "q": "b", "r": "ɹ",
    "s": "s", "t": "ʇ", "u": "n", "v": "ʌ", "w": "ʍ", "x": "x", "y": "ʎ", "z": "z",
    "0": "0", "1": "Ɩ", "2": "ᄅ", "3": "Ɛ", "4": "ㄣ", "5": "ϛ", "6": "9", "7": "ㄥ", "8": "8", "9": "6",
    ".": "˙", ",": "'", "'": ",", "?": "¿", "!": "¡", "(": ")", ")": "(", "[": "]", "]": "[",
}
DOWN_TO_UP = {v: k for k, v in UP_TO_DOWN.items()}
WORD_HINTS = {"hello", "world", "this", "prompt", "hash", "receipt", "canonical", "reflection", "manhattan", "api", "cost"}


@dataclass(frozen=True)
class FingerprintReceipt:
    raw_text: str
    canonical_text: str
    raw_hash: str
    canonical_hash: str
    transform_receipt: dict[str, bool]
    confidence: dict[str, float]
    arbitration_trace: list[str]
    lossless: bool
    receipt_version: str = "canonical-receipt-v0.1"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2, sort_keys=True)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def encode_upside_down(text: str) -> str:
    return "".join(UP_TO_DOWN.get(ch, ch) for ch in reversed(text))


def decode_upside_down(text: str) -> str:
    return "".join(DOWN_TO_UP.get(ch, ch) for ch in reversed(text))


def score_text(text: str) -> float:
    if not text:
        return 0.0
    words = re.findall(r"[a-zA-Z]{2,}", text.lower())
    hits = sum(1 for w in words if w in WORD_HINTS)
    ascii_letters = sum(ch.isascii() and ch.isalpha() for ch in text)
    printable = sum(ch.isprintable() for ch in text)
    return min(1.0, 0.45 * ascii_letters / max(len(text), 1) + 0.35 * printable / max(len(text), 1) + 0.20 * min(hits / 3.0, 1.0))


def compute_fingerprint(text: str) -> FingerprintReceipt:
    working = unicodedata.normalize("NFKC", text)
    trace: list[str] = []
    transforms = {"reversed": False, "upside_down": False, "bidi_override": False, "homoglyph_substitution": False}
    confidence = {k: 0.0 for k in transforms}

    bidi_count = sum(ch in BIDI_CONTROLS for ch in working)
    if bidi_count:
        working = "".join(ch for ch in working if ch not in BIDI_CONTROLS)
        transforms["bidi_override"] = True
        confidence["bidi_override"] = min(1.0, bidi_count / 2.0)
        trace.append(f"removed bidi controls confidence={confidence['bidi_override']:.3f}")

    reversed_candidate = working[::-1]
    reversed_conf = max(0.0, min(1.0, (score_text(reversed_candidate) - score_text(working)) * 2.0))
    upside_candidate = decode_upside_down(working)
    mapped_ratio = sum(ch in DOWN_TO_UP for ch in working) / max(len(working), 1)
    upside_conf = max(0.0, min(1.0, 0.60 * mapped_ratio + 0.40 * max(score_text(upside_candidate) - score_text(working), 0.0)))
    confidence["reversed"] = round(reversed_conf, 6)
    confidence["upside_down"] = round(upside_conf, 6)

    if upside_conf >= 0.25 or reversed_conf >= 0.20:
        if upside_conf >= reversed_conf:
            working = upside_candidate
            transforms["upside_down"] = True
            trace.append(f"selected upside_down confidence={upside_conf:.3f}")
        else:
            working = reversed_candidate
            transforms["reversed"] = True
            trace.append(f"selected reversed confidence={reversed_conf:.3f}")
    else:
        trace.append("orientation unchanged")

    changed = sum(ch in HOMOGLYPHS for ch in working)
    if changed:
        working = "".join(HOMOGLYPHS.get(ch, ch) for ch in working)
        transforms["homoglyph_substitution"] = True
        confidence["homoglyph_substitution"] = round(min(1.0, changed / max(len(working), 1) * 4.0), 6)
        trace.append(f"normalized homoglyphs confidence={confidence['homoglyph_substitution']:.3f}")

    canonical = re.sub(r"\s+", " ", working).strip()
    lossless = not (transforms["bidi_override"] or transforms["homoglyph_substitution"])
    return FingerprintReceipt(text, canonical, sha256(text), sha256(canonical), transforms, confidence, trace, lossless)
