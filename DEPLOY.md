# 生产环境 Docker 部署说明

镜像内**不包含**任何密钥，所有敏感配置通过服务器上的 `.env` 在运行时注入。

## 0. 服务器部署完整流程（从云端拉代码）

### 前置要求

- 服务器已安装 **Docker** 和 **Docker Compose**
- 可访问 GitHub（或你的代码仓库）

### 步骤一：拉取代码

```bash
# 克隆仓库（替换为你的仓库地址）
git clone https://github.com/NightRain010/NL2SQL.git
cd NL2SQL
```

### 步骤二：配置环境变量

```bash
cp .env.example .env
# 用 vim/nano 等编辑 .env，填写真实值（见下方「必须配置的项」）
```

### 步骤三：启动服务

**方式 A：应用 + MySQL 一起部署**（推荐，首次部署）

1. 编辑 `docker-compose.prod.yml`，取消注释其中的 `mysql` 服务、`depends_on`、`volumes` 相关行
2. 确保 `.env` 中 `MYSQL_HOST=mysql`（或不填，默认即为 mysql），`MYSQL_PORT=3306`（或不填）
3. 执行：

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

**方式 B：仅应用**（MySQL 已在其它地方部署）

确保 `.env` 中 `MYSQL_HOST`、`MYSQL_PORT` 指向你的 MySQL 地址，然后：

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

### 步骤四：访问

浏览器打开 `http://服务器IP:10080` 或 `http://你的域名:10080`。

### 后续更新代码

```bash
git pull
docker compose -f docker-compose.prod.yml up -d --build
```

---

## 1. 构建与流量优化

- **多阶段构建**：后端只保留运行时；前端用 Node 构建，用 nginx 托管静态资源，最终镜像不含 Node。
- **小基础镜像**：`python:3.12-slim`、`node:20-alpine`、`nginx:alpine`。
- **`.dockerignore`**：排除 `.git`、`node_modules`、`.venv`、测试文件等，减小构建上下文，节省上传流量。
- **pip/安装**：使用 `--no-cache-dir`、`--frozen-lockfile`，减少层体积。

## 2. 在服务器上配置密钥

在项目根目录创建 `.env`（不要提交到 Git），按需修改：

```bash
cp .env.example .env
# 编辑 .env，填写真实值
```

必须配置的项：

| 变量 | 说明 |
|------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥，从 [DeepSeek 开放平台](https://platform.deepseek.com) 获取 |
| `DEEPSEEK_BASE_URL` | 一般为 `https://api.deepseek.com` |
| `MYSQL_HOST` | 同 compose 部署填 `mysql`，否则填 MySQL 的 IP 或主机名 |
| `MYSQL_PORT` | 同 compose 部署填 `3306`，宿主机映射填 `8306` 等 |
| `MYSQL_USER` | 数据库用户名，如 `root` |
| `MYSQL_PASSWORD` | 数据库密码 |
| `MYSQL_DATABASE` | 数据库名，默认 `nl2sql_platform` |
| `JWT_SECRET_KEY` | 生产环境务必改为随机强密钥，可用 `openssl rand -hex 32` 生成 |

## 3. 启动方式

### 仅应用（前端 + 后端，MySQL 已另有部署）

```bash
docker compose -f docker-compose.prod.yml up -d
```

访问：`http://服务器IP或域名:10080`。

### 应用 + MySQL 一起部署

1. 编辑 `docker-compose.prod.yml`，取消注释其中的 `mysql` 服务及相关 `depends_on`、`volumes`。
2. 确保 `.env` 中 `MYSQL_HOST` 不填或设为 `mysql`，`MYSQL_PORT` 不填或设为 `3306`。
3. 执行：

```bash
docker compose -f docker-compose.prod.yml up -d
```

### 仅构建镜像（用于推送到仓库）

```bash
docker compose -f docker-compose.prod.yml build
# 可选：打 tag 并推送
# docker tag nl2sql-backend:latest 你的仓库/nl2sql-backend:latest
# docker push 你的仓库/nl2sql-backend:latest
```

## 4. 端口说明

| 服务   | 容器内端口 | 宿主机映射 | 说明           |
|--------|------------|------------|----------------|
| 前端   | 80         | 10080      | 对外提供页面   |
| 后端   | 8000       | 不暴露     | 仅由前端 nginx 反向代理 `/api` |
| MySQL（可选） | 3306 | 按需映射   | 仅后端访问     |

## 5. MySQL 在宿主机或其它机器时

- 后端容器需能访问该 MySQL（网络可达）。
- `.env` 中 `MYSQL_HOST` 填该机 IP 或主机名；若 MySQL 在宿主机，Linux 可填 `host.docker.internal`（Docker 20.10+）或宿主机内网 IP。
