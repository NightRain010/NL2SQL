"""Schema 感知 Agent，根据意图识别结果查找相关表结构。"""

from sqlalchemy.orm import Session

from backend.agents.state import AgentState, SchemaInfo, TableInfo, ColumnInfo, JoinInfo
from backend.db.models.schema_meta import SchemaMetadata
from backend.nlp.intent import IntentResult


def schema_agent_node(state: AgentState, *, db: Session) -> dict:
    """
    LangGraph 节点：读取 schema_metadata 表，返回与用户查询相关的表结构信息。

    Args:
        state: 当前 Agent 状态。
        db: 数据库会话。

    Returns:
        更新后的状态字段。
    """
    intent: IntentResult = state["intent"]  # type: ignore[assignment]
    schema_info = _fetch_schema_info(db, intent)
    return {"schema_info": schema_info, "current_step": "fetch_schema"}


def _fetch_schema_info(db: Session, intent: IntentResult) -> SchemaInfo:
    """根据意图中的实体匹配相关表和字段。"""
    entity_texts = {e.text for e in intent.entities}

    all_meta = db.query(SchemaMetadata).all()

    relevant_table_names: set[str] = set()
    for meta in all_meta:
        if meta.comment and any(et in meta.comment for et in entity_texts):
            relevant_table_names.add(meta.table_name)
        if meta.table_name in entity_texts or meta.column_name in entity_texts:
            relevant_table_names.add(meta.table_name)

    if not relevant_table_names:
        relevant_table_names = {m.table_name for m in all_meta}

    tables: list[TableInfo] = []
    for table_name in sorted(relevant_table_names):
        columns = [
            ColumnInfo(
                name=m.column_name,
                type=m.column_type,
                comment=m.comment,
                is_primary=m.is_primary,
                is_nullable=m.is_nullable,
            )
            for m in all_meta
            if m.table_name == table_name
        ]
        tables.append(TableInfo(table_name=table_name, columns=columns))

    joins = _infer_joins(all_meta, relevant_table_names)

    context_summary = _build_context_summary(tables, joins)

    return SchemaInfo(
        relevant_tables=tables,
        suggested_joins=joins,
        context_summary=context_summary,
    )


def _infer_joins(
    all_meta: list[SchemaMetadata], table_names: set[str]
) -> list[JoinInfo]:
    """从外键命名约定中推断 JOIN 关系（字段名以 _id 结尾）。"""
    joins: list[JoinInfo] = []
    table_set = table_names

    for meta in all_meta:
        if meta.table_name not in table_set:
            continue
        if meta.column_name.endswith("_id"):
            ref_table = meta.column_name[:-3] + "s"
            if ref_table in table_set:
                joins.append(
                    JoinInfo(
                        left_table=meta.table_name,
                        right_table=ref_table,
                        left_column=meta.column_name,
                        right_column="id",
                        join_type="INNER",
                    )
                )
    return joins


def _build_context_summary(tables: list[TableInfo], joins: list[JoinInfo]) -> str:
    """构建给 SQL 生成 Agent 的上下文摘要文本。"""
    parts: list[str] = []
    for t in tables:
        col_names = ", ".join(c.name for c in t.columns)
        parts.append(f"表 {t.table_name}: {col_names}")
    for j in joins:
        parts.append(
            f"关联: {j.left_table}.{j.left_column} → {j.right_table}.{j.right_column}"
        )
    return "\n".join(parts)
