# 提示词目录

本目录集中管理 NL2SQL 平台所有 LLM 提示词，便于统一维护与调优。

## 结构

| 文件 | 用途 |
|------|------|
| `sql.py` | SQL 生成 Agent 的系统提示词与用户提示词模板 |
| `formatter.py` | 结果格式化 Agent 的摘要生成提示词 |
| `__init__.py` | 统一导出，供 agents 使用 |

## 提示词列表

### SQL 生成 (`sql.py`)

- **SQL_SYSTEM_PROMPT**：系统角色，定义 SQL 生成规则与约束
- **build_sql_user_prompt(user_input, schema_context)**：构建用户提示词，包含问题与数据库结构

### 结果格式化 (`formatter.py`)

- **FORMATTER_SUMMARY_SYSTEM_PROMPT**：系统角色，定义摘要生成风格
- **build_summary_user_prompt(user_input, preview)**：构建用户提示词，包含问题与结果预览

## 使用示例

```python
from backend.prompts import (
    SQL_SYSTEM_PROMPT,
    build_sql_user_prompt,
    FORMATTER_SUMMARY_SYSTEM_PROMPT,
    build_summary_user_prompt,
)

# SQL 生成
user_prompt = build_sql_user_prompt("有多少学生？", "表 students: id, name, ...")

# 结果摘要
summary_prompt = build_summary_user_prompt("有多少学生？", "[{'count': 100}]")
```

## 修改提示词

编辑对应 `.py` 文件中的常量或函数即可，无需改动 agents 逻辑。修改后需运行相关测试确保行为正确。
