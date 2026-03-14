"""总路由注册，将各模块子路由挂载到 /api 前缀下。"""

from fastapi import APIRouter

from backend.api.auth import router as auth_router
from backend.api.query import router as query_router
from backend.api.schema import router as schema_router
from backend.api.system import router as system_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["认证"])
api_router.include_router(query_router, prefix="/query", tags=["查询"])
api_router.include_router(schema_router, prefix="/schema", tags=["Schema"])
api_router.include_router(system_router, prefix="/system", tags=["系统"])
