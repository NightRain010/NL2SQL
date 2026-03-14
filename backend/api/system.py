"""系统路由：健康检查、版本信息。"""

import time

from fastapi import APIRouter
from sqlalchemy import text as sql_text

from backend.db.engine import engine
from backend.config import settings
from backend.lib.response import success

router = APIRouter()

_START_TIME = time.time()


@router.get("/health")
def health_check():
    """健康检查，验证数据库和 AI 服务可用性。"""
    db_connected = _check_db()
    ai_available = _check_ai()
    uptime = time.time() - _START_TIME

    if db_connected and ai_available:
        status = "healthy"
    elif db_connected or ai_available:
        status = "degraded"
    else:
        status = "unhealthy"

    return success(data={
        "status": status,
        "db_connected": db_connected,
        "ai_available": ai_available,
        "uptime_seconds": round(uptime, 2),
    })


@router.get("/version")
def version_info():
    """获取系统版本信息。"""
    return success(data={
        "version": "1.0.0",
        "build_time": None,
        "env": "development",
    })


def _check_db() -> bool:
    """测试数据库连接。"""
    try:
        with engine.connect() as conn:
            conn.execute(sql_text("SELECT 1"))
        return True
    except Exception:
        return False


def _check_ai() -> bool:
    """检测 DeepSeek API Key 是否已配置。"""
    return bool(settings.DEEPSEEK_API_KEY and settings.DEEPSEEK_API_KEY != "your_api_key_here")
