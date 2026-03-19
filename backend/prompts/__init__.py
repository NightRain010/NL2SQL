"""NL2SQL 平台所有 LLM 提示词统一管理。"""

from backend.prompts.sql import (
    SQL_SYSTEM_PROMPT,
    build_sql_user_prompt,
)
from backend.prompts.formatter import (
    FORMATTER_SUMMARY_SYSTEM_PROMPT,
    build_summary_user_prompt,
)

__all__ = [
    "SQL_SYSTEM_PROMPT",
    "build_sql_user_prompt",
    "FORMATTER_SUMMARY_SYSTEM_PROMPT",
    "build_summary_user_prompt",
]
