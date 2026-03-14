"""LangGraph StateGraph 定义与编排。"""

from langgraph.graph import StateGraph, END
from sqlalchemy.orm import Session
from sqlalchemy import text as sql_text
import time

from backend.agents.state import AgentState
from backend.nlp.intent import recognize_intent
from backend.lib.sql_validator import validate_sql


def recognize_intent_node(state: AgentState) -> dict:
    """节点：Jieba 分词 + 意图识别。"""
    result = recognize_intent(state["user_input"])
    return {
        "intent": result,
        "current_step": "recognize_intent",
        "error": None if result.is_valid else "无法识别查询意图",
    }


def validate_sql_node(state: AgentState) -> dict:
    """节点：SQL 白名单校验。"""
    sql = state.get("generated_sql", "")
    if not sql:
        return {"sql_valid": False, "error": "未生成 SQL 语句", "current_step": "validate_sql"}

    is_valid, errors = validate_sql(sql)
    return {
        "sql_valid": is_valid,
        "current_step": "validate_sql",
        "error": "; ".join(errors) if errors else None,
    }


def execute_sql_node(state: AgentState, *, db: Session) -> dict:
    """节点：通过 SQLAlchemy 执行经校验的 SELECT 语句。"""
    sql = state.get("generated_sql", "")
    if not sql:
        return {"query_result": [], "error": "无 SQL 可执行", "current_step": "execute_sql"}

    try:
        start = time.perf_counter_ns()
        result = db.execute(sql_text(sql))
        rows = [dict(row._mapping) for row in result.fetchall()]
        elapsed_ms = (time.perf_counter_ns() - start) // 1_000_000
        return {
            "query_result": rows,
            "current_step": "execute_sql",
            "error": None,
        }
    except Exception as e:
        return {
            "query_result": [],
            "current_step": "execute_sql",
            "error": f"SQL 执行失败: {str(e)}",
        }


def error_handler_node(state: AgentState) -> dict:
    """节点：统一错误处理。"""
    return {"current_step": "handle_error"}


def route_after_intent(state: AgentState) -> str:
    """条件路由：意图识别后决定是否继续。"""
    intent = state.get("intent")
    if intent and intent.is_valid:
        return "valid"
    return "invalid"


def route_after_validation(state: AgentState) -> str:
    """条件路由：SQL 校验后决定是否执行。"""
    if state.get("sql_valid"):
        return "valid"
    return "invalid"


def build_graph() -> StateGraph:
    """
    构建并返回 NL2SQL 流水线的 StateGraph。

    注意：schema_agent_node、sql_agent_node、formatter_agent_node
    需要在运行时通过 functools.partial 注入 db 会话后再注册。
    """
    from backend.agents.schema_agent import schema_agent_node
    from backend.agents.sql_agent import sql_agent_node
    from backend.agents.formatter_agent import formatter_agent_node

    graph = StateGraph(AgentState)

    graph.add_node("recognize_intent", recognize_intent_node)
    graph.add_node("fetch_schema", schema_agent_node)
    graph.add_node("generate_sql", sql_agent_node)
    graph.add_node("validate_sql", validate_sql_node)
    graph.add_node("execute_sql", execute_sql_node)
    graph.add_node("format_result", formatter_agent_node)
    graph.add_node("handle_error", error_handler_node)

    graph.set_entry_point("recognize_intent")

    graph.add_conditional_edges(
        "recognize_intent",
        route_after_intent,
        {"valid": "fetch_schema", "invalid": "handle_error"},
    )
    graph.add_edge("fetch_schema", "generate_sql")
    graph.add_edge("generate_sql", "validate_sql")
    graph.add_conditional_edges(
        "validate_sql",
        route_after_validation,
        {"valid": "execute_sql", "invalid": "handle_error"},
    )
    graph.add_edge("execute_sql", "format_result")
    graph.add_edge("format_result", END)
    graph.add_edge("handle_error", END)

    return graph
