from __future__ import annotations

from typing import Literal


AnswerScope = Literal["jiyangjia", "general"]


# Explicitly out-of-domain intents take precedence over conversational words such
# as "你们". This prevents semantic search from grounding a weather or writing
# request in an unrelated product document.
GENERAL_INTENT_TERMS = (
    "天气",
    "股市",
    "股票",
    "请假条",
    "咖啡",
    "饭店",
    "餐厅",
    "笑话",
    "翻译",
    "作文",
    "写一封",
    "写个",
    "新闻",
)

# Product and service vocabulary that identifies an 积养家 question even when
# the customer omits the brand name and says only "这个" or "你们" at the kiosk.
JIYANGJIA_DOMAIN_TERMS = (
    "积养家",
    "门店",
    "养生馆",
    "连锁店",
    "食材",
    "爱野",
    "大有谷",
    "养生茶",
    "茶油",
    "飞鸡蛋",
    "亚麻籽",
    "黄芪蜂蜜醋",
    "药食同源",
    "酱油",
    "火腿",
    "黄豆酱",
    "虎坚果油",
    "老陈醋",
    "宣莲",
    "黄酒",
    "藤茶",
    "鲜姜",
    "蜂蜜",
    "香榧油",
    "三七",
    "生姜",
    "黄芪",
    "党参",
    "茯苓",
    "当归",
    "芡实",
    "百合",
    "无花果",
    "玫瑰",
    "石斛",
    "麦冬",
    "黄精",
    "陈皮",
    "莲子",
    "枸杞",
    "山药",
    "桑葚",
    "西洋参",
    "福人",
    "尚乾",
    "盐田虾",
    "肉苁蓉",
    "4s",
    "姜茶",
    "小米",
    "玉米",
    "杂粮",
    "芥花油",
    "大米",
    "鸡汤",
    "七膳",
    "煨汤",
    "汤",
    "汤品",
    "养护",
    "按摩",
    "康养",
    "按摩椅",
    "设备",
    "产品",
    "适老化",
    "扶手",
    "二楼",
    "楼上",
    "技师",
    "会员",
    "消费记录",
    "店长",
    "员工",
    "营业额",
    "营业时间",
    "服务时间",
    "服务包",
    "价格",
    "优惠",
    "折扣",
    "免费",
    "推销",
    "预约",
    "排队",
    "等多久",
    "活动优惠",
    "活动",
    "加盟费",
    "送到家",
    "送货上门",
    "快递发外地",
    "社群活动",
    "健康讲座",
    "转人工",
    "小区",
)

# In the store interface, these phrases refer to the business even without a
# product noun. They are intentionally narrower than a blanket "你们" rule.
JIYANGJIA_BUSINESS_PHRASES = (
    "你们是什么",
    "你们这是",
    "你们和别的",
    "你们是连锁",
    "你们在哪",
    "你们有什么",
    "你们能保证",
    "你们能治",
    "你们亲自",
    "你们东西",
    "你们有",
    "你们楼上",
    "你们能帮",
    "第一次来",
    "带老人来",
    "送人送什么",
    "一个人住",
    "买了能",
    "不住这个小区",
    "进来了看看",
    "现在有什么活动",
    "现在要等多久",
    "怎么和你说话",
    "给我看后台",
    "供应商合同",
    "这个项目",
    "这个能治病",
    "这个汤",
    "这个米",
    "做一次多少钱",
    "做完要注意",
)

JIYANGJIA_SHORT_INTENTS = {"怎么体验", "怎么体验？", "怎么体验?"}


def classify_answer_scope(text: str) -> AnswerScope:
    """Classify whether a question requires approved 积养家 knowledge.

    Explicit brand/product/service references are always in-domain. General
    intents are handled by the LLM without searching the business knowledge
    base, so an unrelated semantic match cannot turn into a fabricated answer.
    """

    normalized = "".join(text.lower().split())
    if not normalized:
        return "general"
    if normalized in JIYANGJIA_SHORT_INTENTS:
        return "jiyangjia"
    if "积养家" in normalized:
        return "jiyangjia"
    if any(term in normalized for term in GENERAL_INTENT_TERMS):
        return "general"
    if any(term in normalized for term in JIYANGJIA_DOMAIN_TERMS):
        return "jiyangjia"
    if any(phrase in normalized for phrase in JIYANGJIA_BUSINESS_PHRASES):
        return "jiyangjia"
    return "general"


def has_explicit_general_intent(text: str) -> bool:
    normalized = "".join(text.lower().split())
    return bool(normalized) and any(term in normalized for term in GENERAL_INTENT_TERMS)


def latest_user_text(messages: list[dict[str, str]]) -> str:
    for message in reversed(messages):
        if message.get("role") == "user":
            return str(message.get("content") or "")
    return ""
