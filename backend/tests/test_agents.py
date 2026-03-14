"""Agent 流水线测试。"""

import pytest

from backend.nlp.intent import recognize_intent
from backend.agents.state import (
    AgentState,
    SchemaInfo,
    TableInfo,
    ColumnInfo,
    FormattedResult,
    TableData,
    ColumnDef,
)


class TestAgentState:
    """AgentState 类型定义测试。"""

    def test_create_initial_state(self):
        """测试初始状态创建。"""
        state: AgentState = {
            "messages": [],
            "user_input": "查一下张三的成绩",
            "intent": None,
            "schema_info": None,
            "generated_sql": None,
            "sql_valid": None,
            "query_result": None,
            "formatted_output": None,
            "error": None,
            "current_step": "start",
        }
        assert state["user_input"] == "查一下张三的成绩"
        assert state["current_step"] == "start"


class TestSchemaInfo:
    """SchemaInfo 数据模型测试。"""

    def test_create_schema_info(self):
        """测试 SchemaInfo 模型创建。"""
        info = SchemaInfo(
            relevant_tables=[
                TableInfo(
                    table_name="students",
                    columns=[
                        ColumnInfo(name="id", type="INTEGER", is_primary=True),
                        ColumnInfo(name="name", type="VARCHAR(64)"),
                    ],
                )
            ],
            suggested_joins=[],
            context_summary="表 students: id, name",
        )
        assert len(info.relevant_tables) == 1
        assert info.relevant_tables[0].table_name == "students"


class TestFormattedResult:
    """FormattedResult 数据模型测试。"""

    def test_create_formatted_result(self):
        """测试 FormattedResult 模型创建。"""
        result = FormattedResult(
            summary="共查询到 5 条记录",
            table_data=TableData(
                columns=[ColumnDef(key="name", label="姓名")],
                rows=[{"name": "张三"}],
                total_count=1,
            ),
        )
        assert result.summary == "共查询到 5 条记录"
        assert result.chart_suggestion is None
