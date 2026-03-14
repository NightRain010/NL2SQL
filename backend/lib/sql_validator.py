"""SQL 白名单校验器，确保 AI 生成的 SQL 仅包含 SELECT 操作。"""

import re
from typing import Optional


_FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "TRUNCATE",
    "REPLACE",
    "GRANT",
    "REVOKE",
    "EXEC",
    "EXECUTE",
    "CALL",
    "INTO OUTFILE",
    "INTO DUMPFILE",
    "LOAD_FILE",
    "LOAD DATA",
]

_FORBIDDEN_PATTERN = re.compile(
    r"\b(" + "|".join(_FORBIDDEN_KEYWORDS) + r")\b",
    re.IGNORECASE,
)


def validate_sql(sql: str) -> tuple[bool, list[str]]:
    """
    校验 SQL 是否仅为安全的 SELECT 语句。

    Returns:
        (is_valid, errors): 校验结果和错误原因列表。
    """
    errors: list[str] = []
    stripped = sql.strip().rstrip(";").strip()

    if not stripped:
        errors.append("SQL 语句为空")
        return False, errors

    if not re.match(r"^\s*SELECT\b", stripped, re.IGNORECASE):
        errors.append("SQL 必须以 SELECT 开头")

    forbidden_matches = _FORBIDDEN_PATTERN.findall(stripped)
    if forbidden_matches:
        unique_matches = sorted(set(m.upper() for m in forbidden_matches))
        errors.append(f"包含禁止的关键词: {', '.join(unique_matches)}")

    if _detect_select_into(stripped):
        errors.append("禁止使用 SELECT ... INTO 语法")

    is_valid = len(errors) == 0
    return is_valid, errors


def _detect_select_into(sql: str) -> bool:
    """检测 SELECT ... INTO 模式。"""
    return bool(re.search(r"\bSELECT\b.*\bINTO\b", sql, re.IGNORECASE | re.DOTALL))


def sanitize_sql(sql: str) -> Optional[str]:
    """
    清理 SQL：去除尾部分号、多余空白。校验不通过时返回 None。
    """
    cleaned = sql.strip().rstrip(";").strip()
    is_valid, _ = validate_sql(cleaned)
    return cleaned if is_valid else None
