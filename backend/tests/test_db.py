"""数据库操作测试。"""

import pytest
from sqlalchemy.orm import Session

from backend.db.models.user import User
from backend.db.crud.user_crud import create_user, get_user_by_username


class TestUserModel:
    """User 模型测试。"""

    def test_create_user(self, db_session: Session):
        """测试创建用户。"""
        user = create_user(db_session, "alice", "alice@example.com", "hashed_pw")
        assert user.id is not None
        assert user.username == "alice"
        assert user.is_active is True

    def test_get_user_by_username(self, db_session: Session):
        """测试按用户名查询。"""
        create_user(db_session, "bob", "bob@example.com", "hashed_pw")
        found = get_user_by_username(db_session, "bob")
        assert found is not None
        assert found.email == "bob@example.com"

    def test_get_nonexistent_user(self, db_session: Session):
        """查询不存在的用户应返回 None。"""
        found = get_user_by_username(db_session, "nobody")
        assert found is None
