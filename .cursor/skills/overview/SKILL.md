# NL2SQL 查询平台 — 项目总览

## 项目简介

自然语言转 SQL 查询平台。用户输入中文问题，系统通过 Jieba 分词 + 意图识别 → LangGraph Agent 流水线 → DeepSeek 生成 SQL → 执行并返回格式化结果。

## 技术栈

| 层 | 技术 |
|---|------|
| 后端 | Python 3.12 + FastAPI + SQLAlchemy + LangChain + LangGraph + Jieba |
| 前端 | Vue 3 + Pinia + Element Plus + UnoCSS + Axios + Vitest |
| AI | DeepSeek (deepseek-chat) 通过 OpenAI 兼容接口 |
| 数据库 | MySQL 8.0 (Docker)，全链路 utf8mb4 |
| 工具链 | 后端 uv，前端 pnpm |

## 项目结构

```
backend/          Python 后端
  api/            FastAPI 路由（auth/query/schema/system），全部需认证
  agents/         LangGraph Agent（schema_agent/sql_agent/formatter_agent），含重试机制
  prompts/       所有 LLM 提示词（sql/formatter），统一管理
  nlp/            Jieba 分词 + 意图识别（含否定词处理）+ 实体提取
  db/             SQLAlchemy ORM（models/ + crud/），含异常处理
  lib/            工具函数（sql_validator 增强版/security/response）
  tests/          pytest 测试

frontend/         Vue 3 前端
  src/views/      4 个页面（Login/Query/History/Schema）
  src/components/ 6 个组件（QueryInput/SqlDisplay/ResultTable/LoadingState/SchemaTree/ChartDisplay）
  src/stores/     3 个 Pinia Store（user/query/schema）
  src/api/        Axios 请求封装（request/auth/query/schema），具体泛型类型
  src/__tests__/  Vitest 测试

docker/           MySQL 容器编排 + 初始化 SQL
```

## Agent 流水线

```
用户输入 → Jieba 分词 + 意图识别 → LangGraph StateGraph 调度
  → Schema 感知 Agent（匹配相关表）
  → SQL 生成 Agent（DeepSeek 生成 SELECT）
  → SQL 白名单校验（仅允许 SELECT）
  → SQLAlchemy 执行 SQL
  → 结果格式化 Agent（生成摘要 + 图表建议）
  → 前端展示
```

## 启动方式

```bash
# 数据库
cd docker && docker compose up -d

# 后端（端口 8000）
cd 项目根目录 && uv run --project backend uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

# 前端（端口 5173）
cd frontend && pnpm dev

# 测试
uv run --project backend pytest backend/tests/ -v   # 后端
cd frontend && pnpm test                              # 前端
```

## 核心约束

1. 数据库操作通过 SQLAlchemy ORM，禁止裸 SQL
2. 用户输入必须经过 Jieba 分词 + 意图校验
3. API 必须有 Pydantic 参数校验
4. AI 生成的 SQL 仅允许 SELECT，经白名单校验
5. MySQL 全链路 utf8mb4，禁止 latin1
6. 每个功能必须有对应测试
