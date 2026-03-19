"""查询路由：提交自然语言查询、查询历史、查询详情。"""

import logging
import time
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from functools import partial

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import text as sql_text

from backend.db.engine import get_db
from backend.db.crud.query_crud import (
    create_query_record,
    update_query_result,
    get_query_by_id,
    list_queries_by_user,
)
from backend.api.auth import get_current_user_id
from backend.agents.schema_agent import schema_agent_node
from backend.agents.sql_agent import sql_agent_node
from backend.agents.formatter_agent import formatter_agent_node
from backend.lib.sql_validator import validate_sql
from backend.lib.response import success, error

router = APIRouter()
logger = logging.getLogger(__name__)


def _serialize_row(row: dict) -> dict:
    """将 SQL 结果行中的非 JSON 原生类型转为可序列化值。"""
    out: dict = {}
    for key, value in row.items():
        if isinstance(value, datetime):
            out[key] = value.isoformat()
        elif isinstance(value, date):
            out[key] = value.isoformat()
        elif isinstance(value, Decimal):
            out[key] = float(value)
        elif isinstance(value, bytes):
            out[key] = value.decode("utf-8", errors="replace")
        else:
            out[key] = value
    return out


class AskRequest(BaseModel):
    """自然语言查询请求。"""

    question: str = Field(..., min_length=2, max_length=500, description="自然语言查询")


@router.post("/ask")
def ask_question(
    req: AskRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """提交自然语言查询，走 LangGraph 流水线返回 SQL 和执行结果。"""
    from backend.nlp.intent import recognize_intent

    intent_result = recognize_intent(req.question)
    record = create_query_record(
        db, user_id, req.question, intent_type=intent_result.intent_type
    )

    if not intent_result.is_valid:
        update_query_result(
            db, record.id, status="rejected", error_message="无法识别查询意图"
        )
        return success(data={
            "query_id": record.id,
            "nl_input": req.question,
            "status": "rejected",
            "error_message": "无法识别查询意图，请尝试更具体的描述",
        })

    state = {
        "messages": [],
        "user_input": req.question,
        "intent": intent_result,
        "schema_info": None,
        "generated_sql": None,
        "sql_valid": None,
        "query_result": None,
        "formatted_output": None,
        "error": None,
        "current_step": "start",
    }

    # 1) Schema 感知
    schema_update = schema_agent_node(state, db=db)
    state.update(schema_update)

    # 2) SQL 生成
    sql_update = sql_agent_node(state)
    state.update(sql_update)

    if not state.get("sql_valid"):
        update_query_result(
            db, record.id,
            generated_sql=state.get("generated_sql"),
            status="rejected",
            error_message=state.get("error", "SQL 校验未通过"),
        )
        return success(data={
            "query_id": record.id,
            "nl_input": req.question,
            "generated_sql": state.get("generated_sql"),
            "status": "rejected",
            "error_message": state.get("error"),
        })

    generated_sql = state.get("generated_sql", "")
    rows: list[dict] = []

    # 3) SQL 执行
    try:
        start_time = time.perf_counter_ns()
        result = db.execute(sql_text(generated_sql))
        rows = [_serialize_row(dict(row._mapping)) for row in result.fetchall()]
        execution_ms = (time.perf_counter_ns() - start_time) // 1_000_000
        state["query_result"] = rows
    except Exception as e:
        logger.exception("SQL 执行失败: %s", generated_sql)
        update_query_result(
            db, record.id,
            generated_sql=generated_sql,
            status="failed",
            error_message="SQL 执行失败，请稍后重试",
        )
        return success(data={
            "query_id": record.id,
            "nl_input": req.question,
            "generated_sql": generated_sql,
            "status": "failed",
            "error_message": "SQL 执行失败，请稍后重试",
        })

    # 4) 结果格式化
    format_update = formatter_agent_node(state)
    state.update(format_update)

    formatted = state.get("formatted_output")
    update_query_result(
        db, record.id,
        generated_sql=generated_sql,
        query_result={"rows": rows, "count": len(rows)},
        status="success",
        execution_ms=execution_ms,
    )

    return success(data={
        "query_id": record.id,
        "nl_input": req.question,
        "generated_sql": generated_sql,
        "explanation": None,
        "result": formatted.table_data.model_dump() if formatted else None,
        "summary": formatted.summary if formatted else None,
        "chart_suggestion": formatted.chart_suggestion.model_dump() if formatted and formatted.chart_suggestion else None,
        "status": "success",
        "execution_ms": execution_ms,
    })


_VALID_STATUSES = {"pending", "success", "failed", "rejected"}


@router.get("/history")
def get_history(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页条数"),
    status: Optional[str] = Query(None, description="状态过滤"),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """获取当前用户的查询历史列表。"""
    if status and status not in _VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"无效的 status 值，可选: {', '.join(_VALID_STATUSES)}")

    items, total = list_queries_by_user(db, user_id, status=status, page=page, size=size)
    return success(data={
        "items": [
            {
                "id": item.id,
                "nl_input": item.nl_input,
                "intent_type": item.intent_type,
                "status": item.status,
                "created_at": item.created_at.isoformat() if item.created_at else None,
                "execution_ms": item.execution_ms,
            }
            for item in items
        ],
        "total": total,
        "page": page,
        "size": size,
    })


@router.get("/{query_id}")
def get_query_detail(
    query_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """获取单条查询记录详情。"""
    record = get_query_by_id(db, query_id)
    if not record:
        raise HTTPException(status_code=404, detail="查询记录不存在")
    if record.user_id != user_id:
        raise HTTPException(status_code=403, detail="无权访问该记录")

    return success(data={
        "id": record.id,
        "nl_input": record.nl_input,
        "intent_type": record.intent_type,
        "generated_sql": record.generated_sql,
        "query_result": record.query_result,
        "status": record.status,
        "error_message": record.error_message,
        "execution_ms": record.execution_ms,
        "created_at": record.created_at.isoformat() if record.created_at else None,
    })
