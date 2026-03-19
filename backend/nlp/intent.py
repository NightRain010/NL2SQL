"""意图分类器，基于规则与关键词匹配识别用户查询意图。"""

from pydantic import BaseModel

from backend.nlp.tokenizer import tokenize
from backend.nlp.entities import Entity, extract_entities


class IntentInput(BaseModel):
    """意图识别器的输入。"""

    raw_text: str


class IntentResult(BaseModel):
    """意图识别器的输出。"""

    tokens: list[str]
    intent_type: str
    entities: list[Entity]
    confidence: float
    is_valid: bool


_AGGREGATE_KEYWORDS = {"平均", "平均分", "总分", "最高", "最低", "统计", "多少", "几个", "人数", "及格率", "合计", "汇总"}
_COMPARE_KEYWORDS = {"比较", "对比", "哪个高", "哪个低", "谁更", "高于", "低于", "差距", "排名"}
_TREND_KEYWORDS = {"趋势", "变化", "走势", "增长", "下降", "波动", "历年", "每学期", "逐年"}
_QUERY_KEYWORDS = {"查", "查询", "看看", "告诉我", "找", "显示", "列出", "是什么", "是多少"}

_NEGATION_WORDS = {"不", "没有", "没", "未", "非", "别", "无", "不要", "不是"}


def recognize_intent(raw_text: str) -> IntentResult:
    """
    对用户输入进行分词 + 意图识别。

    Args:
        raw_text: 用户的自然语言输入。

    Returns:
        包含分词结果、意图类型、实体和置信度的 IntentResult。
    """
    tokens = tokenize(raw_text)
    entities = extract_entities(raw_text, tokens)
    token_set = set(tokens)

    intent_type, confidence = _classify_intent(token_set, raw_text)

    is_valid = intent_type != "unknown"

    return IntentResult(
        tokens=tokens,
        intent_type=intent_type,
        entities=entities,
        confidence=confidence,
        is_valid=is_valid,
    )


def _classify_intent(token_set: set[str], raw_text: str) -> tuple[str, float]:
    """基于关键词命中进行意图分类，返回 (intent_type, confidence)。"""
    scores = {
        "aggregate": _keyword_score(token_set, raw_text, _AGGREGATE_KEYWORDS),
        "compare": _keyword_score(token_set, raw_text, _COMPARE_KEYWORDS),
        "trend": _keyword_score(token_set, raw_text, _TREND_KEYWORDS),
        "query_data": _keyword_score(token_set, raw_text, _QUERY_KEYWORDS),
    }

    best_intent = max(scores, key=scores.get)  # type: ignore[arg-type]
    best_score = scores[best_intent]

    if best_score == 0:
        return "unknown", 0.3

    total = sum(scores.values())
    confidence = min(best_score / max(total, 1) + 0.4, 0.95)
    return best_intent, round(confidence, 2)


def _keyword_score(token_set: set[str], raw_text: str, keywords: set[str]) -> int:
    """计算关键词在 token 集合和原文中的命中次数，被否定词修饰的不计入。"""
    score = 0
    for kw in keywords:
        hit = kw in token_set or (kw in raw_text and kw not in token_set)
        if hit and not _is_negated(raw_text, kw):
            score += 1
    return score


def _is_negated(text: str, keyword: str) -> bool:
    """检测关键词前方是否紧邻否定词（如"不平均"→True）。"""
    idx = text.find(keyword)
    if idx <= 0:
        return False
    for neg in _NEGATION_WORDS:
        nlen = len(neg)
        if idx >= nlen and text[idx - nlen:idx] == neg:
            return True
    return False
