"""查询历史 CRUD 操作。"""

import logging
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.db.models.query_history import QueryHistory

logger = logging.getLogger(__name__)

_MAX_PAGE_SIZE = 100


def create_query_record(
    db: Session,
    user_id: int,
    nl_input: str,
    intent_type: Optional[str] = None,
) -> QueryHistory:
    """创建查询记录（初始状态为 pending）。"""
    record = QueryHistory(
        user_id=user_id,
        nl_input=nl_input,
        intent_type=intent_type,
        status="pending",
    )
    db.add(record)
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("创建查询记录失败: %s", e)
        raise
    db.refresh(record)
    return record


def update_query_result(
    db: Session,
    query_id: int,
    *,
    generated_sql: Optional[str] = None,
    query_result: Optional[dict] = None,
    status: str = "success",
    error_message: Optional[str] = None,
    execution_ms: Optional[int] = None,
) -> Optional[QueryHistory]:
    """更新查询记录的执行结果。"""
    record = db.query(QueryHistory).filter(QueryHistory.id == query_id).first()
    if not record:
        return None
    if generated_sql is not None:
        record.generated_sql = generated_sql
    if query_result is not None:
        record.query_result = query_result
    record.status = status
    if error_message is not None:
        record.error_message = error_message
    if execution_ms is not None:
        record.execution_ms = execution_ms
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("更新查询记录 %d 失败: %s", query_id, e)
        raise
    db.refresh(record)
    return record


def get_query_by_id(db: Session, query_id: int) -> Optional[QueryHistory]:
    """根据 ID 获取查询记录。"""
    return db.query(QueryHistory).filter(QueryHistory.id == query_id).first()


def list_queries_by_user(
    db: Session,
    user_id: int,
    *,
    status: Optional[str] = None,
    page: int = 1,
    size: int = 20,
) -> tuple[list[QueryHistory], int]:
    """分页查询用户的查询历史。返回 (记录列表, 总数)。"""
    size = min(size, _MAX_PAGE_SIZE)
    query = db.query(QueryHistory).filter(QueryHistory.user_id == user_id)
    if status:
        query = query.filter(QueryHistory.status == status)
    total = query.count()
    items = (
        query.order_by(QueryHistory.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    return items, total
