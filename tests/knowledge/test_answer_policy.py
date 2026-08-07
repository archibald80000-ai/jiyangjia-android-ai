from __future__ import annotations

import pytest
from pydantic import ValidationError

from gateway.app.answer_policy import classify_answer_scope
from gateway.app.schemas import KnowledgeSearchRequest


@pytest.mark.parametrize(
    "question",
    [
        "积养家是做什么的？",
        "你们是什么门店？",
        "你们有小米吗？",
        "这个汤喝了能降血压吗？",
        "做一次多少钱？",
        "能帮我查一下我的会员卡吗？",
        "现在有什么优惠折扣？",
        "积养家有榴莲吗？",
    ],
)
def test_jiyangjia_and_related_product_questions_require_approved_knowledge(question: str) -> None:
    assert classify_answer_scope(question) == "jiyangjia"


@pytest.mark.parametrize(
    "question",
    [
        "今天天气怎么样？",
        "附近哪里可以买咖啡？",
        "帮我写个请假条。",
        "最近股市怎么样？",
        "你们会讲笑话吗？",
        "高血压平时应该注意什么？",
    ],
)
def test_general_questions_do_not_use_business_knowledge(question: str) -> None:
    assert classify_answer_scope(question) == "general"


def test_public_search_request_cannot_enable_draft_visibility() -> None:
    with pytest.raises(ValidationError):
        KnowledgeSearchRequest(query="积养家有小米吗？", include_draft=True)
