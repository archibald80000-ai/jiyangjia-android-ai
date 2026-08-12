from __future__ import annotations

import re
from typing import Literal


PERSONA_VERSION = "jiyangjia-neighbor-guide-v1"
ResponseMode = Literal["concise", "story", "choice"]
STORY_QUERY_PATTERN = re.compile(
    r"^(?:请|麻烦)?(?:给我)?(?:详细)?(?:讲讲|介绍一下|说说)(.+?)(?:的)?(?:故事|来历|由来)[？?。]?$"
)


PERSONA_SYSTEM_PROMPT = (
    "你是积养家门店里的数字客服，也是懂产品、愿意认真听人说话的邻里生活向导。"
    "你的气质温暖、真诚、有一点轻松的幽默感，但不油腻、不卖萌、不夸张推销，也不冒充真人。"
    "回答时先直接回应顾客真正想知道的事，再挑一个最有画面或最实用的细节讲清楚；"
    "合适时用一句自然的追问或邀请收尾，不要每次都使用同一个开场和结束语。"
    "使用适合现场播报的自然短句，不输出 Markdown、编号、链接、表格或书面报告腔。"
)

FACT_SAFETY_PROMPT = (
    "凡是积养家及其产品、服务、门店或顾客账户相关事实，只能依据下方 approved 已确认资料回答。"
    "不得编造或补全价格、库存、活动、营业状态、医疗疗效、诊断、账户结果或内部信息。"
    "资料中的健康、营养或传统食养表述，只能明确说成‘资料中提到’、‘传统食养说法’或‘传统食养里常这样搭配’，"
    "不得扩写成确定疗效、治疗建议或诊断，不得使用‘管用’、‘能治疗’、‘能治好’等承诺性措辞。"
    "可以把资料讲得生动，但生动只用于表达，绝不能增加资料之外的事实。"
)


def response_mode(question: str) -> ResponseMode:
    normalized = "".join(question.lower().split())
    if any(term in normalized for term in ("故事", "来历", "由来", "详细讲", "展开讲", "为什么叫", "讲讲")):
        return "story"
    if any(term in normalized for term in ("怎么选", "推荐", "适合我", "哪一种", "哪个好", "区别", "送人")):
        return "choice"
    return "concise"


def story_subject(question: str) -> str | None:
    normalized = "".join(question.strip().split())
    match = STORY_QUERY_PATTERN.fullmatch(normalized)
    if not match:
        return None
    subject = match.group(1).strip("，,。？?！!")
    return subject or None


def prepare_spoken_messages(messages: list[dict[str, str]]) -> list[dict[str, str]]:
    prepared = [dict(message) for message in messages]
    for index in range(len(prepared) - 1, -1, -1):
        if prepared[index].get("role") != "user":
            continue
        subject = story_subject(str(prepared[index].get("content") or ""))
        if subject:
            prepared[index]["content"] = f"请用90到140个汉字介绍{subject}的来历，并讲一个已确认资料中的真实细节。"
        break
    return prepared


def response_direction(question: str) -> str:
    mode = response_mode(question)
    if mode == "story":
        return (
            "这是一道来历介绍。用约 90 到 140 个汉字讲出一段连贯的口述内容，不要展开成长文："
            "先说核心来历，再讲一两个资料里真实的场景、工艺或人物细节，最后落到顾客能理解的产品特点。"
            "不要把资料复述成说明书，也不要为了戏剧性虚构情节。"
            "如果已确认资料只有产品规格而没有故事，就自然地说明目前没有已确认的故事资料，再介绍能确认的特点。"
        )
    if mode == "choice":
        return (
            "这是一道选择型问题。先复述顾客最关键的选择条件，再只依据资料给出一到两个清晰差异。"
            "资料不足以个性化推荐时，坦率说明还需要了解什么，不替顾客做医疗或绝对化判断。"
            "控制在 80 到 180 个汉字。"
        )
    return (
        "这是一道直接问答。第一句话就给答案，再补一个最有用或最有画面的资料细节。"
        "通常控制在 60 到 150 个汉字；信息本身很简单时不要硬凑长度。"
    )


def format_approved_context(
    context: list[dict[str, object]],
    *,
    max_items: int = 4,
    max_chars_per_item: int = 700,
) -> str:
    excerpts: list[str] = []
    for index, item in enumerate(context[:max_items], start=1):
        title = str(item.get("title") or item.get("id") or "未命名资料").strip()
        excerpt = str(item.get("excerpt") or item.get("text") or "").strip()[:max_chars_per_item]
        if not excerpt:
            continue
        source = item.get("source")
        source_uri = source.get("uri") if isinstance(source, dict) else item.get("source_uri")
        source_note = f"；来源：{source_uri}" if source_uri else ""
        excerpts.append(f"[资料{index}] {title}{source_note}\n{excerpt}")
    return "\n\n".join(excerpts)
