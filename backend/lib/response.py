"""统一 API 响应格式封装。"""

from typing import TypeVar, Generic, Optional

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """统一成功响应格式。"""

    code: int = 200
    message: str = "success"
    data: Optional[T] = None


class ApiErrorResponse(BaseModel):
    """统一错误响应格式。"""

    code: int
    message: str
    detail: Optional[str] = None


def success(data=None, message: str = "success") -> dict:
    """构造成功响应。"""
    return {"code": 200, "message": message, "data": data}


def error(code: int, message: str, detail: Optional[str] = None) -> dict:
    """构造错误响应。"""
    resp = {"code": code, "message": message}
    if detail:
        resp["detail"] = detail
    return resp
