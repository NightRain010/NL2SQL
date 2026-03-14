# NL2SQL 查询平台 — 技术架构文档

> 版本：1.0  
> 技术栈：Python + FastAPI + LangChain + LangGraph + Jieba + SQLAlchemy + MySQL | Vue 3 + Pinia + UnoCSS + Element Plus | DeepSeek (OpenAI 兼容接口)

---

## 目录

- [一、项目目录结构](#一项目目录结构)
- [二、数据库 Schema 设计](#二数据库-schema-设计)
- [三、Agent 接口定义](#三agent-接口定义)
- [四、API 路由清单](#四api-路由清单)

---

## 一、项目目录结构

```
nl2sql-platform/
│
├── .env                          # 环境变量（不提交到 git）
├── .env.example                  # 环境变量模板
├── .gitignore
├── README.md
├── CLAUDE.md                     # 项目约束与规范
├── ARCHITECTURE.md               # 本文档
│
├── backend/
│   ├── main.py                   # FastAPI 应用入口
│   ├── config.py                 # 配置加载（读取 .env）
│   ├── pyproject.toml            # uv 项目配置 & 依赖声明
│   ├── uv.lock                   # uv 锁文件（自动生成）
│   ├── requirements.txt          # 兼容 pip 的依赖清单
│   │
│   ├── api/                      # FastAPI 路由层
│   │   ├── __init__.py
│   │   ├── router.py             # 总路由注册
│   │   ├── auth.py               # 认证路由 /api/auth/*
│   │   ├── query.py              # 查询路由 /api/query/*
│   │   ├── schema.py             # Schema 路由 /api/schema/*
│   │   └── system.py             # 系统路由 /api/system/*
│   │
│   ├── agents/                   # LangGraph Agent 逻辑
│   │   ├── __init__.py
│   │   ├── graph.py              # LangGraph StateGraph 定义与编排
│   │   ├── state.py              # AgentState 类型定义
│   │   ├── schema_agent.py       # Schema 感知 Agent
│   │   ├── sql_agent.py          # SQL 生成 Agent
│   │   └── formatter_agent.py    # 结果格式化 Agent
│   │
│   ├── chains/                   # LangChain Chain 定义
│   │   ├── __init__.py
│   │   ├── sql_chain.py          # SQL 生成 Chain（Prompt + LLM + Parser）
│   │   └── summary_chain.py      # 结果摘要 Chain
│   │
│   ├── nlp/                      # Jieba 分词 + 意图识别
│   │   ├── __init__.py
│   │   ├── tokenizer.py          # Jieba 分词封装
│   │   ├── intent.py             # 意图分类器
│   │   ├── entities.py           # 实体提取
│   │   └── user_dict.txt         # 自定义分词词典
│   │
│   ├── db/                       # SQLAlchemy 数据库层
│   │   ├── __init__.py
│   │   ├── engine.py             # 数据库引擎 & 会话管理
│   │   ├── base.py               # declarative_base 定义
│   │   ├── models/               # ORM 模型
│   │   │   ├── __init__.py
│   │   │   ├── user.py           # User 模型
│   │   │   ├── query_history.py  # QueryHistory 模型
│   │   │   ├── schema_meta.py    # SchemaMetadata 模型
│   │   │   ├── student.py        # Student 业务示例模型
│   │   │   ├── course.py         # Course 业务示例模型
│   │   │   ├── score.py          # Score 业务示例模型
│   │   │   └── teacher.py        # Teacher 业务示例模型
│   │   └── crud/                 # CRUD 操作封装
│   │       ├── __init__.py
│   │       ├── user_crud.py
│   │       └── query_crud.py
│   │
│   ├── lib/                      # 工具函数
│   │   ├── __init__.py
│   │   ├── sql_validator.py      # SQL 白名单校验（仅允许 SELECT）
│   │   ├── security.py           # 密码哈希、JWT 工具
│   │   └── response.py           # 统一响应格式封装
│   │
│   └── tests/                    # pytest 测试
│       ├── __init__.py
│       ├── conftest.py           # 测试 fixtures
│       ├── test_nlp.py           # 分词 & 意图识别测试
│       ├── test_agents.py        # Agent 流水线测试
│       ├── test_api_auth.py      # 认证 API 测试
│       ├── test_api_query.py     # 查询 API 测试
│       ├── test_sql_validator.py # SQL 校验测试
│       └── test_db.py            # 数据库操作测试
│
├── frontend/
│   ├── package.json
│   ├── pnpm-lock.yaml            # pnpm 锁文件（自动生成）
│   ├── vite.config.ts            # Vite 构建配置
│   ├── tsconfig.json
│   ├── uno.config.ts             # UnoCSS 配置
│   ├── index.html
│   │
│   └── src/
│       ├── main.ts               # Vue 应用入口
│       ├── App.vue               # 根组件
│       ├── router/
│       │   └── index.ts          # Vue Router 路由配置
│       │
│       ├── views/                # 页面组件
│       │   ├── LoginView.vue     # 登录页
│       │   ├── QueryView.vue     # 主查询页（核心页面）
│       │   ├── HistoryView.vue   # 查询历史页
│       │   └── SchemaView.vue    # 数据库结构浏览页
│       │
│       ├── components/           # 通用组件
│       │   ├── QueryInput.vue    # 自然语言输入框
│       │   ├── SqlDisplay.vue    # SQL 展示 & 高亮
│       │   ├── ResultTable.vue   # 查询结果表格
│       │   ├── LoadingState.vue  # 加载状态
│       │   └── SchemaTree.vue    # 表结构树形展示
│       │
│       ├── stores/               # Pinia 状态管理
│       │   ├── user.ts           # 用户认证状态
│       │   ├── query.ts          # 查询状态（输入、SQL、结果）
│       │   └── schema.ts         # 数据库 Schema 状态
│       │
│       ├── api/                  # Axios 请求封装
│       │   ├── request.ts        # Axios 实例 & 拦截器
│       │   ├── auth.ts           # 认证 API
│       │   ├── query.ts          # 查询 API
│       │   └── schema.ts         # Schema API
│       │
│       ├── types/                # TypeScript 类型定义
│       │   └── index.ts
│       │
│       └── styles/               # UnoCSS 样式
│           └── main.css
│
└── docker/
    ├── docker-compose.yml        # MySQL 容器编排
    └── init/
        ├── 01_schema.sql         # 自动建表 DDL
        └── 02_data.sql           # 测试数据 DML
```

---

## 二、数据库 Schema 设计

### 2.1 公共基类

```python
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TimestampMixin:
    """为所有模型提供统一的时间戳字段。"""
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
```

---

### 2.2 平台表

#### users — 用户表

```python
class User(Base, TimestampMixin):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username   = Column(String(64), unique=True, nullable=False, comment="用户名")
    email      = Column(String(128), unique=True, nullable=False, comment="邮箱")
    password_hash = Column(String(256), nullable=False, comment="密码哈希值")
    is_active  = Column(Boolean, default=True, nullable=False, comment="是否激活")
```

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, AUTO_INCREMENT | 用户唯一标识 |
| username | String(64) | UNIQUE, NOT NULL | 登录用户名 |
| email | String(128) | UNIQUE, NOT NULL | 邮箱地址 |
| password_hash | String(256) | NOT NULL | bcrypt 哈希后的密码 |
| is_active | Boolean | DEFAULT TRUE | 账号是否可用 |
| created_at | DateTime | DEFAULT NOW() | 注册时间 |
| updated_at | DateTime | DEFAULT NOW(), ON UPDATE | 更新时间 |

---

#### query_history — 查询历史表

```python
class QueryHistory(Base, TimestampMixin):
    __tablename__ = "query_history"

    id            = Column(Integer, primary_key=True, autoincrement=True, comment="记录ID")
    user_id       = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="关联用户")
    nl_input      = Column(Text, nullable=False, comment="用户自然语言输入")
    intent_type   = Column(String(32), nullable=True, comment="识别到的意图类型")
    generated_sql = Column(Text, nullable=True, comment="AI 生成的 SQL 语句")
    query_result  = Column(JSON, nullable=True, comment="查询结果（JSON 序列化）")
    status        = Column(Enum("pending", "success", "failed", "rejected"), default="pending",
                           nullable=False, comment="查询状态")
    error_message = Column(Text, nullable=True, comment="错误信息")
    execution_ms  = Column(Integer, nullable=True, comment="SQL 执行耗时（毫秒）")

    user = relationship("User", backref="queries")
```

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, AUTO_INCREMENT | 记录唯一标识 |
| user_id | Integer | FK → users.id, INDEX | 提交查询的用户 |
| nl_input | Text | NOT NULL | 用户输入的自然语言 |
| intent_type | String(32) | NULLABLE | 意图分类结果 |
| generated_sql | Text | NULLABLE | 生成的 SQL |
| query_result | JSON | NULLABLE | 执行结果 |
| status | Enum | DEFAULT 'pending' | pending / success / failed / rejected |
| error_message | Text | NULLABLE | 失败时的错误信息 |
| execution_ms | Integer | NULLABLE | SQL 执行耗时 |
| created_at | DateTime | DEFAULT NOW() | 提交时间 |
| updated_at | DateTime | DEFAULT NOW(), ON UPDATE | 更新时间 |

---

#### schema_metadata — 表结构元数据缓存表

```python
class SchemaMetadata(Base, TimestampMixin):
    __tablename__ = "schema_metadata"

    id          = Column(Integer, primary_key=True, autoincrement=True, comment="元数据ID")
    table_name  = Column(String(128), nullable=False, index=True, comment="表名")
    column_name = Column(String(128), nullable=False, comment="字段名")
    column_type = Column(String(64), nullable=False, comment="字段类型")
    is_primary  = Column(Boolean, default=False, comment="是否为主键")
    is_nullable = Column(Boolean, default=True, comment="是否允许 NULL")
    comment     = Column(String(512), nullable=True, comment="字段注释")

    __table_args__ = (
        UniqueConstraint("table_name", "column_name", name="uq_table_column"),
    )
```

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, AUTO_INCREMENT | 元数据唯一标识 |
| table_name | String(128) | NOT NULL, INDEX | 数据库表名 |
| column_name | String(128) | NOT NULL | 字段名 |
| column_type | String(64) | NOT NULL | 字段数据类型 |
| is_primary | Boolean | DEFAULT FALSE | 是否为主键 |
| is_nullable | Boolean | DEFAULT TRUE | 是否可空 |
| comment | String(512) | NULLABLE | 字段中文注释 |
| created_at | DateTime | DEFAULT NOW() | 创建时间 |
| updated_at | DateTime | DEFAULT NOW(), ON UPDATE | 更新时间 |

> **唯一约束**：(table_name, column_name) 联合唯一

---

### 2.3 业务示例表（NL2SQL 演示查询目标）

#### students — 学生表

```python
class Student(Base, TimestampMixin):
    __tablename__ = "students"

    id         = Column(Integer, primary_key=True, autoincrement=True, comment="学生ID")
    name       = Column(String(64), nullable=False, comment="姓名")
    gender     = Column(Enum("男", "女"), nullable=False, comment="性别")
    birth_date = Column(Date, nullable=True, comment="出生日期")
    grade      = Column(String(32), nullable=False, comment="年级")
    class_name = Column(String(32), nullable=False, comment="班级")
    enrollment_date = Column(Date, nullable=False, comment="入学日期")
```

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer, PK | 学生唯一标识 |
| name | String(64) | 学生姓名 |
| gender | Enum("男","女") | 性别 |
| birth_date | Date | 出生日期 |
| grade | String(32) | 年级（如 "2024级"） |
| class_name | String(32) | 班级（如 "计算机1班"） |
| enrollment_date | Date | 入学日期 |

---

#### teachers — 教师表

```python
class Teacher(Base, TimestampMixin):
    __tablename__ = "teachers"

    id         = Column(Integer, primary_key=True, autoincrement=True, comment="教师ID")
    name       = Column(String(64), nullable=False, comment="姓名")
    title      = Column(String(32), nullable=True, comment="职称")
    department = Column(String(64), nullable=False, comment="所属院系")
    phone      = Column(String(20), nullable=True, comment="联系电话")
```

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer, PK | 教师唯一标识 |
| name | String(64) | 教师姓名 |
| title | String(32) | 职称（教授/副教授/讲师） |
| department | String(64) | 院系 |
| phone | String(20) | 联系电话 |

---

#### courses — 课程表

```python
class Course(Base, TimestampMixin):
    __tablename__ = "courses"

    id          = Column(Integer, primary_key=True, autoincrement=True, comment="课程ID")
    name        = Column(String(128), nullable=False, comment="课程名称")
    code        = Column(String(32), unique=True, nullable=False, comment="课程编号")
    credit      = Column(Float, nullable=False, comment="学分")
    teacher_id  = Column(Integer, ForeignKey("teachers.id"), nullable=False, comment="授课教师")
    semester    = Column(String(32), nullable=False, comment="学期")

    teacher = relationship("Teacher", backref="courses")
```

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK | 课程唯一标识 |
| name | String(128) | NOT NULL | 课程名称 |
| code | String(32) | UNIQUE | 课程编号（如 "CS101"） |
| credit | Float | NOT NULL | 学分 |
| teacher_id | Integer | FK → teachers.id | 授课教师 |
| semester | String(32) | NOT NULL | 学期（如 "2025-春"） |

---

#### scores — 成绩表

```python
class Score(Base, TimestampMixin):
    __tablename__ = "scores"

    id         = Column(Integer, primary_key=True, autoincrement=True, comment="成绩ID")
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True, comment="学生")
    course_id  = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True, comment="课程")
    score      = Column(Float, nullable=False, comment="分数")
    exam_type  = Column(Enum("期中", "期末", "平时"), nullable=False, comment="考试类型")

    student = relationship("Student", backref="scores")
    course  = relationship("Course", backref="scores")

    __table_args__ = (
        UniqueConstraint("student_id", "course_id", "exam_type", name="uq_student_course_exam"),
    )
```

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK | 成绩唯一标识 |
| student_id | Integer | FK → students.id, INDEX | 学生 |
| course_id | Integer | FK → courses.id, INDEX | 课程 |
| score | Float | NOT NULL | 分数（0-100） |
| exam_type | Enum | NOT NULL | 期中 / 期末 / 平时 |

> **唯一约束**：(student_id, course_id, exam_type) 联合唯一，防止重复录入

---

### 2.4 ER 关系总览

```
users 1 ──── N query_history       （用户 → 查询记录）
teachers 1 ──── N courses           （教师 → 课程）
students 1 ──── N scores            （学生 → 成绩）
courses  1 ──── N scores            （课程 → 成绩）
schema_metadata                     （独立表，缓存所有表结构信息）
```

---

## 三、Agent 接口定义

### 3.1 整体流水线

```
用户输入(str)
  │
  ▼
┌──────────────────────┐
│  IntentRecognizer    │  Jieba 分词 + 意图识别
│  (nlp/intent.py)     │
└──────────┬───────────┘
           │ IntentResult
           ▼
┌──────────────────────┐
│  LangGraph           │  状态机调度（graph.py）
│  StateGraph          │  管理 AgentState 在各节点间流转
└──────────┬───────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
┌─────────┐ ┌──────────────┐
│ Schema  │ │ SQL 生成     │
│ Agent   │→│ Agent        │
└─────────┘ └──────┬───────┘
                   │
                   ▼
          ┌────────────────┐
          │ 结果格式化     │
          │ Agent          │
          └────────┬───────┘
                   │ FormattedResult
                   ▼
              前端展示
```

---

### 3.2 AgentState — LangGraph 全局状态

```python
from typing import TypedDict, Optional
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """LangGraph StateGraph 的全局共享状态。"""

    messages: list[BaseMessage]
    user_input: str
    intent: Optional["IntentResult"]
    schema_info: Optional["SchemaInfo"]
    generated_sql: Optional[str]
    sql_valid: Optional[bool]
    query_result: Optional[list[dict]]
    formatted_output: Optional["FormattedResult"]
    error: Optional[str]
    current_step: str
```

| 字段 | 类型 | 说明 |
|------|------|------|
| messages | list[BaseMessage] | LLM 对话消息链 |
| user_input | str | 用户原始自然语言输入 |
| intent | IntentResult \| None | 意图识别结果 |
| schema_info | SchemaInfo \| None | 相关表结构信息 |
| generated_sql | str \| None | 生成的 SQL 语句 |
| sql_valid | bool \| None | SQL 白名单校验结果 |
| query_result | list[dict] \| None | SQL 执行的原始结果 |
| formatted_output | FormattedResult \| None | 格式化后的最终输出 |
| error | str \| None | 错误信息 |
| current_step | str | 当前执行到的步骤名 |

---

### 3.3 IntentRecognizer — 意图识别器

**位置**：`backend/nlp/intent.py`

#### 输入

```python
class IntentInput(BaseModel):
    """意图识别器的输入。"""
    raw_text: str               # 用户原始输入
```

#### 输出

```python
class IntentResult(BaseModel):
    """意图识别器的输出。"""
    tokens: list[str]           # Jieba 分词结果
    intent_type: str            # 意图分类: "query_data" | "aggregate" | "compare" | "trend" | "unknown"
    entities: list[Entity]      # 提取到的实体列表
    confidence: float           # 置信度 (0.0 ~ 1.0)
    is_valid: bool              # 是否为合法的数据查询意图


class Entity(BaseModel):
    """从用户输入中提取的实体。"""
    text: str                   # 实体原始文本（如 "张三"、"数学"）
    label: str                  # 实体类型: "person" | "course" | "time" | "metric" | "value"
    start: int                  # 在原始文本中的起始位置
    end: int                    # 在原始文本中的结束位置
```

#### 意图类型枚举

| intent_type | 说明 | 示例 |
|-------------|------|------|
| query_data | 查询具体数据 | "查一下张三的数学成绩" |
| aggregate | 聚合统计 | "全班数学平均分是多少" |
| compare | 对比分析 | "男生和女生的平均分哪个高" |
| trend | 趋势分析 | "这学期各科成绩的变化趋势" |
| unknown | 无法识别 | "今天天气怎么样" |

---

### 3.4 SchemaAgent — Schema 感知 Agent

**位置**：`backend/agents/schema_agent.py`

#### 输入

```python
class SchemaAgentInput(BaseModel):
    """Schema 感知 Agent 的输入。"""
    intent_result: IntentResult     # 意图识别结果
    user_input: str                 # 用户原始输入（辅助上下文）
```

#### 输出

```python
class SchemaInfo(BaseModel):
    """Schema 感知 Agent 的输出。"""
    relevant_tables: list[TableInfo]    # 相关表信息
    suggested_joins: list[JoinInfo]     # 建议的 JOIN 关系
    context_summary: str                # 给 SQL 生成 Agent 的上下文摘要


class TableInfo(BaseModel):
    """单张表的结构描述。"""
    table_name: str                     # 表名
    columns: list[ColumnInfo]           # 字段列表
    row_count: Optional[int]            # 估算行数


class ColumnInfo(BaseModel):
    """单个字段的描述。"""
    name: str                           # 字段名
    type: str                           # 数据类型
    comment: Optional[str]              # 中文注释
    is_primary: bool                    # 是否主键
    is_foreign_key: bool                # 是否外键
    references: Optional[str]           # 外键引用（如 "teachers.id"）


class JoinInfo(BaseModel):
    """表间关联关系。"""
    left_table: str                     # 左表
    right_table: str                    # 右表
    left_column: str                    # 左表关联字段
    right_column: str                   # 右表关联字段
    join_type: str                      # "INNER" | "LEFT" | "RIGHT"
```

---

### 3.5 SQLGeneratorAgent — SQL 生成 Agent

**位置**：`backend/agents/sql_agent.py`

#### 输入

```python
class SQLGeneratorInput(BaseModel):
    """SQL 生成 Agent 的输入。"""
    user_input: str                     # 用户自然语言
    intent_result: IntentResult         # 意图识别结果
    schema_info: SchemaInfo             # 相关表结构信息
```

#### 输出

```python
class SQLGeneratorOutput(BaseModel):
    """SQL 生成 Agent 的输出。"""
    sql_query: str                      # 生成的 SQL（仅 SELECT）
    explanation: str                    # SQL 逻辑的自然语言解释
    is_valid: bool                      # 经白名单校验后是否合法
    validation_errors: list[str]        # 校验不通过的原因列表
    confidence: float                   # 生成置信度 (0.0 ~ 1.0)
```

#### 安全约束

- 生成的 SQL **必须且仅能是 SELECT 语句**
- 经过 `lib/sql_validator.py` 白名单校验
- 禁止包含子查询修改数据的操作（如 `SELECT ... INTO`）
- 禁止调用存储过程或函数修改数据

---

### 3.6 ResultFormatterAgent — 结果格式化 Agent

**位置**：`backend/agents/formatter_agent.py`

#### 输入

```python
class FormatterInput(BaseModel):
    """结果格式化 Agent 的输入。"""
    raw_result: list[dict]              # SQL 执行的原始查询结果
    sql_query: str                      # 执行的 SQL 语句
    user_input: str                     # 用户原始问题（用于生成摘要）
    intent_type: str                    # 意图类型（影响展示方式）
```

#### 输出

```python
class FormattedResult(BaseModel):
    """结果格式化 Agent 的输出。"""
    summary: str                        # 结果的自然语言摘要
    table_data: TableData               # 格式化的表格数据
    chart_suggestion: Optional[ChartSuggestion]  # 可视化建议


class TableData(BaseModel):
    """表格化的结果数据。"""
    columns: list[ColumnDef]            # 列定义
    rows: list[dict]                    # 行数据
    total_count: int                    # 总行数


class ColumnDef(BaseModel):
    """表格列定义。"""
    key: str                            # 字段标识
    label: str                          # 中文列名
    align: str                          # 对齐方式: "left" | "center" | "right"
    sortable: bool                      # 是否支持排序


class ChartSuggestion(BaseModel):
    """可视化建议。"""
    chart_type: str                     # "bar" | "line" | "pie" | "table_only"
    x_field: str                        # X 轴字段
    y_field: str                        # Y 轴字段
    title: str                          # 图表标题
```

---

### 3.7 LangGraph 状态机节点与边

```python
from langgraph.graph import StateGraph, END

graph = StateGraph(AgentState)

# 节点注册
graph.add_node("recognize_intent", recognize_intent_node)
graph.add_node("fetch_schema",     schema_agent_node)
graph.add_node("generate_sql",     sql_generator_node)
graph.add_node("validate_sql",     sql_validator_node)
graph.add_node("execute_sql",      sql_executor_node)
graph.add_node("format_result",    formatter_agent_node)
graph.add_node("handle_error",     error_handler_node)

# 边定义
graph.set_entry_point("recognize_intent")

graph.add_conditional_edges("recognize_intent", route_after_intent, {
    "valid":   "fetch_schema",
    "invalid": "handle_error",
})

graph.add_edge("fetch_schema",  "generate_sql")
graph.add_edge("generate_sql",  "validate_sql")

graph.add_conditional_edges("validate_sql", route_after_validation, {
    "valid":   "execute_sql",
    "invalid": "handle_error",
})

graph.add_edge("execute_sql",   "format_result")
graph.add_edge("format_result", END)
graph.add_edge("handle_error",  END)
```

#### 节点说明

| 节点 | 职责 | 出边条件 |
|------|------|----------|
| recognize_intent | 调用 Jieba 分词 + 意图识别 | valid → fetch_schema / invalid → handle_error |
| fetch_schema | 读取 schema_metadata，匹配相关表 | → generate_sql |
| generate_sql | 调用 DeepSeek 生成 SELECT SQL | → validate_sql |
| validate_sql | 白名单校验 SQL 安全性 | valid → execute_sql / invalid → handle_error |
| execute_sql | 通过 SQLAlchemy 执行 SQL，获取结果 | → format_result |
| format_result | 调用 DeepSeek 生成摘要 + 格式化输出 | → END |
| handle_error | 封装错误信息返回前端 | → END |

---

## 四、API 路由清单

### 4.1 认证模块 — `/api/auth`

| 方法 | 路径 | 描述 | 请求体 | 响应 |
|------|------|------|--------|------|
| POST | `/api/auth/register` | 用户注册 | `{ username, email, password }` | `{ id, username, email, token }` |
| POST | `/api/auth/login` | 用户登录 | `{ username, password }` | `{ token, expires_in, user }` |
| GET | `/api/auth/me` | 获取当前用户信息 | — (Header: Authorization) | `{ id, username, email, is_active, created_at }` |

#### 请求/响应 Schema

```python
class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)

class LoginRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    token: str
    expires_in: int
    user: UserInfo

class UserInfo(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
```

---

### 4.2 查询模块 — `/api/query`

| 方法 | 路径 | 描述 | 请求体/参数 | 响应 |
|------|------|------|-------------|------|
| POST | `/api/query/ask` | 提交自然语言查询 | `{ question }` | `{ query_id, sql, result, summary, chart }` |
| GET | `/api/query/history` | 获取查询历史列表 | `?page=1&size=20&status=` | `{ items[], total, page, size }` |
| GET | `/api/query/{query_id}` | 获取查询详情 | — | `{ id, nl_input, sql, result, status, ... }` |

#### 请求/响应 Schema

```python
class AskRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=500, description="自然语言查询")

class AskResponse(BaseModel):
    query_id: int
    nl_input: str
    generated_sql: Optional[str]
    explanation: Optional[str]
    result: Optional[TableData]
    summary: Optional[str]
    chart_suggestion: Optional[ChartSuggestion]
    status: str
    execution_ms: Optional[int]
    error_message: Optional[str]

class HistoryQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)
    status: Optional[str] = None

class HistoryResponse(BaseModel):
    items: list[QueryHistoryItem]
    total: int
    page: int
    size: int

class QueryHistoryItem(BaseModel):
    id: int
    nl_input: str
    intent_type: Optional[str]
    status: str
    created_at: datetime
    execution_ms: Optional[int]
```

---

### 4.3 Schema 模块 — `/api/schema`

| 方法 | 路径 | 描述 | 请求体/参数 | 响应 |
|------|------|------|-------------|------|
| GET | `/api/schema/tables` | 获取所有业务表列表 | — | `{ tables: [{ name, comment, column_count }] }` |
| GET | `/api/schema/tables/{table_name}` | 获取指定表的详细结构 | — | `{ table_name, columns[], row_count }` |
| POST | `/api/schema/refresh` | 重新扫描数据库并刷新元数据缓存 | — | `{ refreshed_tables, total_columns }` |

#### 请求/响应 Schema

```python
class TableListResponse(BaseModel):
    tables: list[TableSummary]

class TableSummary(BaseModel):
    name: str
    comment: Optional[str]
    column_count: int

class TableDetailResponse(BaseModel):
    table_name: str
    columns: list[ColumnDetail]
    row_count: Optional[int]

class ColumnDetail(BaseModel):
    name: str
    type: str
    comment: Optional[str]
    is_primary: bool
    is_nullable: bool
    is_foreign_key: bool
    references: Optional[str]

class RefreshResponse(BaseModel):
    refreshed_tables: int
    total_columns: int
```

---

### 4.4 系统模块 — `/api/system`

| 方法 | 路径 | 描述 | 请求体/参数 | 响应 |
|------|------|------|-------------|------|
| GET | `/api/system/health` | 健康检查 | — | `{ status, db_connected, ai_available }` |
| GET | `/api/system/version` | 获取系统版本信息 | — | `{ version, build_time, env }` |

#### 请求/响应 Schema

```python
class HealthResponse(BaseModel):
    status: str              # "healthy" | "degraded" | "unhealthy"
    db_connected: bool
    ai_available: bool
    uptime_seconds: float

class VersionResponse(BaseModel):
    version: str             # 如 "1.0.0"
    build_time: Optional[str]
    env: str                 # "development" | "production"
```

---

### 4.5 统一响应格式

所有 API 统一使用以下信封格式：

```python
class ApiResponse(BaseModel, Generic[T]):
    """统一 API 响应格式。"""
    code: int = 200              # 业务状态码
    message: str = "success"     # 提示信息
    data: Optional[T] = None     # 业务数据

class ApiErrorResponse(BaseModel):
    """统一错误响应格式。"""
    code: int                    # 错误码
    message: str                 # 错误描述
    detail: Optional[str] = None # 详细错误信息（仅开发环境）
```

#### 错误码约定

| code | 含义 |
|------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 / Token 过期 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 422 | 意图识别失败 / SQL 校验不通过 |
| 500 | 服务器内部错误 |
| 503 | AI 服务不可用 |

---

> **文档维护说明**：本文档随项目迭代持续更新，所有接口变更需同步修改此文档。
