# 项目：NL2SQL 查询平台

## 技术栈

- 后端：Python + FastAPI + LangChain + LangGraph + Jieba + SQLAlchemy + MySQL
- 前端：Vue 3 + Pinia + UnoCSS + Element Plus + Axios
- AI：OpenAI 兼容接口对接 DeepSeek（model: deepseek-chat）
- 工具链：后端 uv，前端 pnpm，数据库 Docker

## 项目结构

```
backend/
  api/          # FastAPI 路由（auth/query/schema/system），全部需认证
  agents/       # LangGraph Agent（schema_agent/sql_agent/formatter_agent），含重试机制
  nlp/          # Jieba 分词 + 意图识别（含否定词处理）+ 实体提取
  db/           # SQLAlchemy ORM（models/ + crud/），含异常处理
  lib/          # 工具函数（sql_validator 增强版/security/response）
  tests/        # pytest 测试

frontend/
  src/
    views/      # 页面组件（Login/Query/History/Schema）
    components/ # 通用组件（QueryInput/SqlDisplay/ResultTable/LoadingState/SchemaTree/ChartDisplay）
    stores/     # Pinia 状态管理（user/query/schema）
    api/        # Axios 请求封装（request/auth/query/schema），具体泛型类型
    __tests__/  # Vitest 测试

docker/
  docker-compose.yml    # MySQL 容器编排（开发）
  init/
    01_schema.sql       # 自动建表
    02_data.sql         # 自动插入测试数据

# 生产 Docker 部署（镜像不含密钥，密钥通过 .env 注入）
docker-compose.prod.yml # 前端 + 后端生产编排
backend/Dockerfile      # 后端多阶段构建
frontend/Dockerfile     # 前端构建 + nginx 托管
DEPLOY.md               # 部署说明
```

## .env 文件模板

根目录创建 `.env`，不提交到 git：

```env
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com

MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=your_database
```

## 模块文档索引（Skills）

开发前请先阅读对应模块的 Skill 文档，了解已有实现和设计约定：

| Skill | 路径 | 内容 |
|-------|------|------|
| 项目总览 | `.cursor/skills/overview/SKILL.md` | 架构、启动方式、Agent 流水线 |
| 后端 API | `.cursor/skills/backend-api/SKILL.md` | 路由清单、认证机制、响应格式 |
| 后端 Agent | `.cursor/skills/backend-agents/SKILL.md` | LangGraph 编排、AgentState、各 Agent 职责 |
| 后端 NLP | `.cursor/skills/backend-nlp/SKILL.md` | Jieba 分词、意图分类、实体提取 |
| 后端 DB | `.cursor/skills/backend-db/SKILL.md` | ORM 模型、CRUD、字符集规范 |
| 前端页面 | `.cursor/skills/frontend-pages/SKILL.md` | 4 个页面、路由、UI 设计体系 |
| 前端组件 | `.cursor/skills/frontend-components/SKILL.md` | 6 个组件、3 个 Store、API 层、测试 |
