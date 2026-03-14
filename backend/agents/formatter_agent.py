"""结果格式化 Agent，将 SQL 查询结果转换为前端可展示的结构化数据。"""

from typing import Optional

from openai import OpenAI

from backend.config import settings
from backend.agents.state import (
    AgentState,
    FormattedResult,
    TableData,
    ColumnDef,
    ChartSuggestion,
)


def formatter_agent_node(state: AgentState) -> dict:
    """
    LangGraph 节点：格式化查询结果，生成摘要和可视化建议。

    Args:
        state: 当前 Agent 状态。

    Returns:
        更新后的状态字段。
    """
    raw_result: list[dict] = state.get("query_result") or []
    sql_query = state.get("generated_sql", "")
    user_input = state["user_input"]
    intent = state.get("intent")
    intent_type = intent.intent_type if intent else "query_data"

    try:
        formatted = _format_result(raw_result, sql_query, user_input, intent_type)
        return {
            "formatted_output": formatted,
            "current_step": "format_result",
        }
    except Exception as e:
        fallback = _build_fallback_result(raw_result)
        return {
            "formatted_output": fallback,
            "current_step": "format_result",
            "error": f"格式化时出现非致命错误: {str(e)}",
        }


def _format_result(
    raw_result: list[dict],
    sql_query: str,
    user_input: str,
    intent_type: str,
) -> FormattedResult:
    """格式化查询结果。"""
    table_data = _build_table_data(raw_result)
    summary = _generate_summary(raw_result, user_input)
    chart = _suggest_chart(raw_result, intent_type)

    return FormattedResult(
        summary=summary,
        table_data=table_data,
        chart_suggestion=chart,
    )


def _build_table_data(raw_result: list[dict]) -> TableData:
    """从原始查询结果构建 TableData。"""
    if not raw_result:
        return TableData(columns=[], rows=[], total_count=0)

    columns = [
        ColumnDef(
            key=key,
            label=key,
            align="right" if isinstance(raw_result[0].get(key), (int, float)) else "left",
            sortable=True,
        )
        for key in raw_result[0].keys()
    ]

    return TableData(columns=columns, rows=raw_result, total_count=len(raw_result))


def _generate_summary(raw_result: list[dict], user_input: str) -> str:
    """调用 DeepSeek 生成结果摘要。"""
    if not raw_result:
        return "查询未返回任何结果。"

    if len(raw_result) <= 3:
        preview = str(raw_result)
    else:
        preview = str(raw_result[:3]) + f"... 共 {len(raw_result)} 条记录"

    try:
        client = OpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
        )
        response = client.chat.completions.create(
            model=settings.DEEPSEEK_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个数据分析助手。请用一句简洁的中文总结以下查询结果。",
                },
                {
                    "role": "user",
                    "content": f"用户问题: {user_input}\n查询结果: {preview}",
                },
            ],
            temperature=0.3,
            max_tokens=200,
        )
        return response.choices[0].message.content or f"共返回 {len(raw_result)} 条记录。"
    except Exception:
        return f"查询完成，共返回 {len(raw_result)} 条记录。"


def _suggest_chart(
    raw_result: list[dict], intent_type: str
) -> Optional[ChartSuggestion]:
    """根据意图类型和结果结构推荐图表类型。"""
    if not raw_result or len(raw_result) < 2:
        return None

    keys = list(raw_result[0].keys())
    if len(keys) < 2:
        return None

    x_field = keys[0]
    y_field = next(
        (k for k in keys[1:] if isinstance(raw_result[0].get(k), (int, float))),
        keys[1],
    )

    chart_map = {
        "aggregate": "bar",
        "compare": "bar",
        "trend": "line",
        "query_data": "table_only",
    }
    chart_type = chart_map.get(intent_type, "bar")

    if chart_type == "table_only":
        return None

    return ChartSuggestion(
        chart_type=chart_type,
        x_field=x_field,
        y_field=y_field,
        title=f"{y_field} 分布",
    )
