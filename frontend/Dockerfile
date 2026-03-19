# 构建阶段：仅用于打包静态资源
FROM node:20-alpine AS builder

WORKDIR /build

# 先装依赖，利用层缓存
COPY frontend/package.json frontend/pnpm-lock.yaml* ./
RUN corepack enable pnpm && pnpm install --frozen-lockfile

COPY frontend/ ./
RUN pnpm run build

# 运行阶段：nginx 托管静态文件 + 反向代理 /api
FROM nginx:alpine

# 默认配置（部署时可通过挂载覆盖）
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /build/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
