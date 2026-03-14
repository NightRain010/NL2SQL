"""用户 CRUD 操作。"""

from typing import Optional

from sqlalchemy.orm import Session

from backend.db.models.user import User


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """根据 ID 获取用户。"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """根据用户名获取用户。"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """根据邮箱获取用户。"""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, username: str, email: str, password_hash: str) -> User:
    """创建新用户。"""
    user = User(username=username, email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
