"""实体提取模块，从分词结果中识别关键实体。"""

import re
from typing import Optional

from pydantic import BaseModel


class Entity(BaseModel):
    """从用户输入中提取的实体。"""

    text: str
    label: str
    start: int
    end: int


_METRIC_KEYWORDS = {"平均分", "最高分", "最低分", "总分", "人数", "及格率", "成绩", "分数", "学分"}

_TIME_PATTERN = re.compile(
    r"(\d{4})\s*[年-]\s*(春|秋|上|下)?|"
    r"(上学期|下学期|这学期|本学期|期中|期末)"
)

_COURSE_KEYWORDS = {"数学", "语文", "英语", "物理", "化学", "生物", "计算机", "编程", "数据库", "算法"}


def extract_entities(text: str, tokens: list[str]) -> list[Entity]:
    """
    从原始文本和分词结果中提取实体。

    Args:
        text: 原始输入文本。
        tokens: 分词后的 token 列表。

    Returns:
        提取到的实体列表。
    """
    entities: list[Entity] = []
    pos = 0

    for token in tokens:
        start = text.find(token, pos)
        if start == -1:
            continue
        end = start + len(token)

        label = _classify_token(token, text)
        if label:
            entities.append(Entity(text=token, label=label, start=start, end=end))

        pos = end

    time_entities = _extract_time_entities(text)
    existing_spans = {(e.start, e.end) for e in entities}
    for te in time_entities:
        if (te.start, te.end) not in existing_spans:
            entities.append(te)

    return entities


def _classify_token(token: str, context: str) -> Optional[str]:
    """根据 token 内容判断其实体类型。"""
    if token in _METRIC_KEYWORDS:
        return "metric"

    if token in _COURSE_KEYWORDS:
        return "course"

    if re.fullmatch(r"\d+(\.\d+)?", token):
        return "value"

    if len(token) >= 2 and not re.search(r"\d", token) and token not in _METRIC_KEYWORDS:
        if any(kw in context for kw in ["的", "同学", "老师", "学生"]):
            if _looks_like_person_name(token):
                return "person"

    return None


def _looks_like_person_name(token: str) -> bool:
    """粗略判断 token 是否像人名（2-4 字，不含数字和标点）。"""
    return bool(re.fullmatch(r"[\u4e00-\u9fff]{2,4}", token))


def _extract_time_entities(text: str) -> list[Entity]:
    """正则匹配时间类实体。"""
    entities = []
    for match in _TIME_PATTERN.finditer(text):
        entities.append(
            Entity(text=match.group(), label="time", start=match.start(), end=match.end())
        )
    return entities
