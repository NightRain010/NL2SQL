"""SQL 生成 Agent，调用 DeepSeek 生成 SELECT 语句。"""

import logging
import time

from openai import OpenAI

from backend.config import settings
from backend.agents.state import AgentState, SQLGeneratorOutput, SchemaInfo
from backend.lib.sql_validator import validate_sql

logger = logging.getLogger(__name__)

_MAX_RETRIES = 3
_RETRY_BASE_DELAY = 1.0
_REQUEST_TIMEOUT = 30


_SYSTEM_PROMPT = """你是一个专业的 SQL 生成助手。根据用户的自然语言问题和数据库表结构信息，生成准确的 MySQL SELECT 查询语句。

规则：
1. 只能生成 SELECT 语句，禁止任何修改数据的操作
2. 使用标准 MySQL 语法
3. 字段名和表名使用反引号包裹
4. 对中文值使用 UTF-8 编码
5. 仅输出 SQL 语句，不要输出任何解释文字"""


def sql_agent_node(state: AgentState) -> dict:
    """
    LangGraph 节点：调用 DeepSeek 根据意图和表结构生成 SQL。

    Args:
        state: 当前 Agent 状态。

    Returns:
        更新后的状态字段。
    """
    user_input = state["user_input"]
    schema_info: SchemaInfo | None = state.get("schema_info")  # type: ignore[assignment]

    if schema_info is None:
        return {
            "generated_sql": None,
            "sql_valid": False,
            "current_step": "generate_sql",
            "error": "未获取到表结构信息，无法生成 SQL",
        }

    try:
        output = _generate_sql(user_input, schema_info)
        return {
            "generated_sql": output.sql_query,
            "sql_valid": output.is_valid,
            "current_step": "generate_sql",
            "error": None if output.is_valid else "; ".join(output.validation_errors),
        }
    except Exception as e:
        return {
            "generated_sql": None,
            "sql_valid": False,
            "current_step": "generate_sql",
            "error": f"SQL 生成失败: {str(e)}",
        }


def _generate_sql(user_input: str, schema_info: SchemaInfo) -> SQLGeneratorOutput:
    """调用 DeepSeek API 生成 SQL 并校验，含指数退避重试。"""
    client = OpenAI(
        api_key=settings.DEEPSEEK_API_KEY,
        base_url=settings.DEEPSEEK_BASE_URL,
        timeout=_REQUEST_TIMEOUT,
    )

    user_prompt = (
        f"用户问题: {user_input}\n\n"
        f"数据库结构:\n{schema_info.context_summary}\n\n"
        f"请生成对应的 SELECT 查询语句。"
    )

    last_error: Exception | None = None
    for attempt in range(_MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=settings.DEEPSEEK_MODEL,
                messages=[
                    {"role": "system", "content": _SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.1,
                max_tokens=1024,
            )
            break
        except Exception as e:
            last_error = e
            if attempt < _MAX_RETRIES - 1:
                delay = _RETRY_BASE_DELAY * (2 ** attempt)
                logger.warning("DeepSeek SQL 生成第 %d 次重试，等待 %.1fs: %s", attempt + 1, delay, e)
                time.sleep(delay)
    else:
        raise last_error  # type: ignore[misc]

    raw_sql = response.choices[0].message.content or ""
    sql_query = _extract_sql(raw_sql)

    is_valid, validation_errors = validate_sql(sql_query)

    explanation = f"根据您的问题「{user_input}」生成的查询语句"

    return SQLGeneratorOutput(
        sql_query=sql_query,
        explanation=explanation,
        is_valid=is_valid,
        validation_errors=validation_errors,
        confidence=0.85 if is_valid else 0.3,
    )


def _extract_sql(raw_response: str) -> str:
    """从 LLM 响应中提取纯 SQL 语句（去除 markdown 代码块标记）。"""
    text = raw_response.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text
