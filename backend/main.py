"""FastAPI 应用入口。"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.router import api_router

app = FastAPI(
    title="NL2SQL 查询平台",
    description="自然语言转 SQL 查询平台，基于 DeepSeek + LangGraph",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    """根路径健康探针。"""
    return {"message": "NL2SQL 查询平台运行中"}
