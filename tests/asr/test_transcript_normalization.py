from __future__ import annotations

from gateway.app.transcript_normalization import normalize_transcript_text


def test_normalizes_common_jiyangjia_homophones() -> None:
    samples = [
        "您好，欢迎来到机养家。",
        "您好，欢迎来到季养家。",
        "您好，欢迎来到寄养家。",
        "您好，欢迎来到吉阳家。",
        "您好，欢迎来到积阳家。",
        "请问济氧家有什么服务？",
        "请问七养家是做什么的？",
    ]

    for sample in samples:
        result = normalize_transcript_text(sample)
        assert "积养家" in result.text
        assert result.changed is True
        assert result.replacements


def test_keeps_correct_brand_unchanged() -> None:
    result = normalize_transcript_text("您好，欢迎来到积养家。")

    assert result.text == "您好，欢迎来到积养家。"
    assert result.changed is False
    assert result.replacements == []


def test_does_not_change_unrelated_text() -> None:
    result = normalize_transcript_text("请问门店服务时间是什么？")

    assert result.text == "请问门店服务时间是什么？"
    assert result.changed is False
