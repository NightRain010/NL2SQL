"""查询 API 测试。"""

import pytest


def _register_and_get_token(client) -> str:
    """辅助函数：注册用户并返回 token。"""
    resp = client.post("/api/auth/register", json={
        "username": "queryuser",
        "email": "query@example.com",
        "password": "password123",
    })
    return resp.json()["data"]["token"]


class TestQueryHistory:
    """查询历史接口测试。"""

    def test_get_history_unauthorized(self, client):
        """未认证应返回 401。"""
        resp = client.get("/api/query/history")
        assert resp.status_code in (401, 403)

    def test_get_history_empty(self, client):
        """新用户的查询历史应为空。"""
        token = _register_and_get_token(client)
        resp = client.get(
            "/api/query/history",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["items"] == []
        assert data["total"] == 0


class TestAskQuestion:
    """自然语言查询接口测试。"""

    def test_ask_question_too_short(self, client):
        """问题过短应返回 422。"""
        token = _register_and_get_token(client)
        resp = client.post(
            "/api/query/ask",
            json={"question": "a"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 422
