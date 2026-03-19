# 后端：Agent 流水线

## 模块位置

`backend/agents/`

## 架构

LangGraph StateGraph 编排 7 个节点（定义在 `graph.py`，`query.py` 通过 `build_graph()` 调用）：

```
recognize_intent ─(valid)─→ fetch_schema → generate_sql → validate_sql ─(valid)─→ execute_sql → format_result → END
       │                                                        │
       └─(invalid)─→ handle_error → END                        └─(invalid)─→ handle_error → END
```

## 全局状态 AgentState

定义在 `state.py`，TypedDict 类型：

| 字段 | 类型 | 说明 |
|------|------|------|
| messages | list[BaseMessage] | LLM 消息链 |
| user_input | str | 用户原始输入 |
| intent | IntentResult | 意图识别结果 |
| schema_info | SchemaInfo | 相关表结构 |
| generated_sql | str | 生成的 SQL |
| sql_valid | bool | 校验结果 |
| query_result | list[dict] | 执行结果 |
| formatted_output | FormattedResult | 格式化输出 |
| error | str | 错误信息 |
| current_step | str | 当前步骤 |

## 各 Agent 说明

### SchemaAgent (`schema_agent.py`)
- 输入：intent + entities
- 从 schema_metadata 表匹配相关表，推断 JOIN 关系
- 输出：SchemaInfo（tables + joins + context_summary）

### SQLGeneratorAgent (`sql_agent.py`)
- 输入：user_input + schema_info（None 时直接返回错误）
- 调用 DeepSeek 生成 SELECT SQL，含指数退避重试（最多 3 次，timeout=30s）
- 经 `sql_validator.py` 白名单校验
- 输出：SQLGeneratorOutput（sql + explanation + is_valid）

### FormatterAgent (`formatter_agent.py`)
- 输入：raw_result + sql_query + user_input + intent_type
- 调用 DeepSeek 生成自然语言摘要，含指数退避重试（最多 3 次，timeout=30s）
- 根据意图类型推荐图表（bar/line/pie）
- 输出：FormattedResult（summary + table_data + chart_suggestion）

## 数据模型

所有接口类型（SchemaInfo、TableInfo、ColumnInfo、JoinInfo、SQLGeneratorOutput、FormattedResult、TableData、ColumnDef、ChartSuggestion）均定义在 `state.py`，使用 Pydantic BaseModel。

## 注意事项

- `backend/chains/` 已删除（原有 sql_chain.py / summary_chain.py 未被引用的死代码）
- DeepSeek 调用统一加了 timeout 和重试机制
- SQL 校验增强：禁止 UNION、INFORMATION_SCHEMA、系统表、多语句、超长 SQL

## 测试

- `test_agents.py`：3 个用例（AgentState 创建、SchemaInfo 模型、FormattedResult 模型）
