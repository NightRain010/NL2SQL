"""用户模型。"""

from sqlalchemy import Column, Integer, String, Boolean

from backend.db.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """用户表，存储平台注册用户信息。"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username = Column(String(64), unique=True, nullable=False, comment="用户名")
    email = Column(String(128), unique=True, nullable=False, comment="邮箱")
    password_hash = Column(String(256), nullable=False, comment="密码哈希值")
    is_active = Column(Boolean, default=True, nullable=False, comment="是否激活")
