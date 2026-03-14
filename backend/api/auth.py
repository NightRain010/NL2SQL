"""认证路由：注册、登录、获取当前用户。"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from backend.db.engine import get_db
from backend.db.crud.user_crud import (
    create_user,
    get_user_by_username,
    get_user_by_email,
)
from backend.lib.security import hash_password, verify_password, create_access_token, decode_access_token
from backend.lib.response import success, error

router = APIRouter()
security = HTTPBearer()


class RegisterRequest(BaseModel):
    """注册请求。"""

    username: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class LoginRequest(BaseModel):
    """登录请求。"""

    username: str
    password: str


class UserInfo(BaseModel):
    """用户信息响应。"""

    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    """从 JWT Token 中解析当前用户 ID。"""
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token 无效或已过期")
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token 中缺少用户信息")
    return int(user_id)


@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """用户注册。"""
    if get_user_by_username(db, req.username):
        raise HTTPException(status_code=400, detail="用户名已存在")
    if get_user_by_email(db, req.email):
        raise HTTPException(status_code=400, detail="邮箱已被注册")

    hashed = hash_password(req.password)
    user = create_user(db, req.username, req.email, hashed)
    token = create_access_token({"sub": str(user.id)})

    return success(data={
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "token": token,
    })


@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    """用户登录。"""
    user = get_user_by_username(db, req.username)
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="账号已被禁用")

    token = create_access_token({"sub": str(user.id)})

    return success(data={
        "token": token,
        "expires_in": 86400,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
        },
    })


@router.get("/me")
def get_me(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """获取当前登录用户信息。"""
    from backend.db.crud.user_crud import get_user_by_id

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    return success(data={
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    })
