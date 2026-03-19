# NL2SQL 查询平台

## 项目简介

**NL2SQL 查询平台** 是一个将自然语言转换为 SQL 的智能查询系统。用户使用中文提问，系统通过 Jieba 分词与意图识别，经由 LangGraph Agent 流水线，调用 DeepSeek 大模型生成 SQL，执行后返回格式化结果。

适用于业务人员、数据分析师等非技术人员，通过自然语言快速查询数据库，降低 SQL 使用门槛。

## 核心特性

- **中文自然语言输入**：支持中文问题，自动分词与意图识别
- **AI 驱动 SQL 生成**：基于 DeepSeek 大模型，结合 Schema 感知生成准确 SQL
- **安全可控**：仅允许 SELECT 查询，白名单校验，防止注入与误操作
- **结果可视化**：支持表格展示、图表建议与智能摘要
- **查询历史**：记录历史查询，便于回溯与复用

## 技术栈

| 层级 | 技术选型 |
|------|----------|
| **后端** | Python 3.12 + FastAPI + SQLAlchemy + LangChain + LangGraph + Jieba |
| **前端** | Vue 3 + Pinia + Element Plus + UnoCSS + Axios + Vitest |
| **AI** | DeepSeek (deepseek-chat)，通过 OpenAI 兼容接口调用 |
| **数据库** | MySQL 8.0 (Docker)，全链路 utf8mb4 |
| **工具链** | 后端 uv，前端 pnpm |

## 项目结构

```
ai/
├── backend/                 # Python 后端
│   ├── api/                 # FastAPI 路由（auth/query/schema/system），全部需认证
│   ├── agents/              # LangGraph Agent（schema_agent/sql_agent/formatter_agent）
│   ├── nlp/                 # Jieba 分词 + 意图识别 + 实体提取
│   ├── db/                  # SQLAlchemy ORM（models/ + crud/）
│   ├── lib/                 # 工具函数（sql_validator/security/response）
│   └── tests/               # pytest 测试
├── frontend/                # Vue 3 前端
│   └── src/
│       ├── views/           # 页面（Login/Query/History/Schema）
│       ├── components/      # 组件（QueryInput/SqlDisplay/ResultTable 等）
│       ├── stores/          # Pinia Store（user/query/schema）
│       └── api/             # Axios 请求封装
├── docker/                  # MySQL 容器编排 + 初始化 SQL
└── .env.example             # 环境变量示例
```

## Agent 流水线

```
用户输入
    ↓
Jieba 分词 + 意图识别
    ↓
LangGraph StateGraph 调度
    ↓
Schema 感知 Agent（匹配相关表）
    ↓
SQL 生成 Agent（DeepSeek 生成 SELECT）
    ↓
SQL 白名单校验（仅允许 SELECT）
    ↓
SQLAlchemy 执行 SQL
    ↓
结果格式化 Agent（摘要 + 图表建议）
    ↓
前端展示
```

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- Docker（用于 MySQL）
- [uv](https://github.com/astral-sh/uv)（Python 包管理）
- pnpm

### 1. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填写 DEEPSEEK_API_KEY、MySQL 密码、JWT 密钥等
```

### 2. 启动 MySQL

```bash
cd docker && docker compose up -d
```

### 3. 启动后端

```bash
uv run --project backend uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### 4. 启动前端

```bash
cd frontend && pnpm install && pnpm dev
```

访问 http://localhost:5173 即可使用。

### 5. 运行测试

```bash
# 后端测试
uv run --project backend pytest backend/tests/ -v

# 前端测试
cd frontend && pnpm test
```

## 核心约束

1. 数据库操作通过 SQLAlchemy ORM，禁止裸 SQL
2. 用户输入必须经过 Jieba 分词与意图校验
3. API 必须有 Pydantic 参数校验
4. AI 生成的 SQL 仅允许 SELECT，经白名单校验
5. MySQL 全链路 utf8mb4，禁止 latin1
6. 每个功能必须有对应测试

## 许可证

本项目仅供学习与内部使用。
