from __future__ import annotations

import re
from dataclasses import dataclass


CANONICAL_BRAND_NAME = "积养家"
BRAND_ALIAS_PATTERN = re.compile(r"[积机季寄吉济记纪鸡极急级七][养阳氧样杨羊][家佳]")
CANONICAL_SEVEN_MEAL = "七膳"
SEVEN_MEAL_SOUP_ALIAS_PATTERN = re.compile(r"(?:漆扇|七扇|柒扇|七善|柒善)(?=(?:鸡汤|煨汤|汤))")


@dataclass(frozen=True)
class TranscriptNormalizationResult:
    text: str
    changed: bool
    replacements: list[dict[str, str]]


def normalize_transcript_text(text: str) -> TranscriptNormalizationResult:
    """Normalize high-value ASR homophones while preserving raw text upstream."""

    if not text:
        return TranscriptNormalizationResult(text=text, changed=False, replacements=[])

    replacements: list[dict[str, str]] = []

    def replace_brand(match: re.Match[str]) -> str:
        raw = match.group(0)
        if raw != CANONICAL_BRAND_NAME:
            replacements.append({"from": raw, "to": CANONICAL_BRAND_NAME, "type": "brand"})
        return CANONICAL_BRAND_NAME

    normalized = BRAND_ALIAS_PATTERN.sub(replace_brand, text)

    def replace_seven_meal(match: re.Match[str]) -> str:
        raw = match.group(0)
        replacements.append({"from": raw, "to": CANONICAL_SEVEN_MEAL, "type": "product"})
        return CANONICAL_SEVEN_MEAL

    normalized = SEVEN_MEAL_SOUP_ALIAS_PATTERN.sub(replace_seven_meal, normalized)
    return TranscriptNormalizationResult(
        text=normalized,
        changed=normalized != text,
        replacements=replacements,
    )
