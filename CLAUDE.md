# 项目：NL2SQL 查询平台

## 技术栈
- 后端：Python + FastAPI + LangChain + LangGraph + Jieba + SQLAlchemy + MySQL
- 前端：Vue 3 + Pinia + UnoCSS + Element Plus + Axios
- AI：OpenAI 通用接口 对接 DeepSeek（model: deepseek-chat）

## 项目结构
backend/
  api/          # FastAPI 路由
  agents/       # LangGraph agent 逻辑
  chains/       # LangChain chain 定义
  nlp/          # Jieba 分词 + 意图识别
  db/           # SQLAlchemy models + migrations
  lib/          # 工具函数

frontend/
  src/
    views/      # 页面组件
    components/ # 通用组件
    stores/     # Pinia 状态管理
    api/        # Axios 请求封装
    styles/     # UnoCSS 样式

docker/
  docker-compose.yml    # 启动 MySQL 容器
  init/
    01_schema.sql       # 自动建表
    02_data.sql         # 自动插入测试数据

## 核心约束
1. 所有数据库操作通过 SQLAlchemy ORM，禁止裸 SQL（除非 agent 生成给用户展示）
2. 用户输入必须经过 Jieba 分词 + 意图校验后再进入 LangChain 流程
3. API 必须有请求参数校验（Pydantic schema）
4. 所有 AI 生成的 SQL 在执行前必须经过白名单校验（只允许 SELECT）
5. DeepSeek 调用统一走 openai 兼容接口，base_url 配置在环境变量中

## .env 文件模板（根目录创建 .env，不提交到 git）
  DEEPSEEK_API_KEY=your_api_key_here
  DEEPSEEK_BASE_URL=https://api.deepseek.com

  MYSQL_HOST=127.0.0.1
  MYSQL_PORT=3306
  MYSQL_USER=root
  MYSQL_PASSWORD=your_password
  MYSQL_DATABASE=your_database
```

---

同时 `.gitignore` 里加上：
```
.env
.env.local
.env.production

## Agent 架构
用户输入
  → Jieba 分词 + 意图识别
    → LangGraph 状态机调度
      → Schema 感知 Agent（读取 MySQL 表结构）
        → SQL 生成 Agent（DeepSeek 生成 SELECT）
          → 结果格式化 Agent
            → 前端展示

## AI 接口配置
- 使用 OpenAI Python SDK，base_url 指向 DeepSeek
- 模型：deepseek-chat
- 示例：
  client = OpenAI(
      api_key=os.environ["DEEPSEEK_API_KEY"],
      base_url="https://api.deepseek.com"
  )

## 测试要求
每个模块必须有对应测试文件（pytest），测试覆盖率 > 80%