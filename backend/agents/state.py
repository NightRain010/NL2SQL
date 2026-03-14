"""LangGraph 全局状态与 Agent 接口类型定义。"""

from typing import TypedDict, Optional

from pydantic import BaseModel
from langchain_core.messages import BaseMessage

from backend.nlp.intent import IntentResult


class ColumnInfo(BaseModel):
    """单个字段的描述。"""

    name: str
    type: str
    comment: Optional[str] = None
    is_primary: bool = False
    is_foreign_key: bool = False
    references: Optional[str] = None


class TableInfo(BaseModel):
    """单张表的结构描述。"""

    table_name: str
    columns: list[ColumnInfo]
    row_count: Optional[int] = None


class JoinInfo(BaseModel):
    """表间关联关系。"""

    left_table: str
    right_table: str
    left_column: str
    right_column: str
    join_type: str = "INNER"


class SchemaInfo(BaseModel):
    """Schema 感知 Agent 的输出。"""

    relevant_tables: list[TableInfo]
    suggested_joins: list[JoinInfo]
    context_summary: str


class SQLGeneratorOutput(BaseModel):
    """SQL 生成 Agent 的输出。"""

    sql_query: str
    explanation: str
    is_valid: bool
    validation_errors: list[str] = []
    confidence: float = 0.0


class ColumnDef(BaseModel):
    """表格列定义。"""

    key: str
    label: str
    align: str = "left"
    sortable: bool = True


class TableData(BaseModel):
    """表格化的结果数据。"""

    columns: list[ColumnDef]
    rows: list[dict]
    total_count: int


class ChartSuggestion(BaseModel):
    """可视化建议。"""

    chart_type: str
    x_field: str
    y_field: str
    title: str


class FormattedResult(BaseModel):
    """结果格式化 Agent 的输出。"""

    summary: str
    table_data: TableData
    chart_suggestion: Optional[ChartSuggestion] = None


class AgentState(TypedDict):
    """LangGraph StateGraph 的全局共享状态。"""

    messages: list[BaseMessage]
    user_input: str
    intent: Optional[IntentResult]
    schema_info: Optional[SchemaInfo]
    generated_sql: Optional[str]
    sql_valid: Optional[bool]
    query_result: Optional[list[dict]]
    formatted_output: Optional[FormattedResult]
    error: Optional[str]
    current_step: str
