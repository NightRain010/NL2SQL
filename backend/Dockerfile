# 多阶段构建，仅安装生产依赖，减小镜像体积
FROM python:3.12-slim AS builder

WORKDIR /build

# 只复制依赖列表，利用层缓存减少重建时的流量
COPY backend/requirements-prod.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements-prod.txt

# 运行阶段：仅保留运行时
FROM python:3.12-slim

WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app" \
    PYTHONUNBUFFERED=1

COPY --from=builder /opt/venv /opt/venv
COPY backend/ ./backend/

# 非 root 运行
RUN useradd -m -u 1000 app && chown -R app:app /app
USER app

EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
