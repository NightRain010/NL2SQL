"""端到端流程测试：注册 → 登录 → 查询历史 → 系统检查。"""

import pytest


class TestFullFlow:
    """完整业务流程集成测试。"""

    def test_register_login_flow(self, client):
        """注册后用同一账号登录应成功并返回有效 token。"""
        reg = client.post("/api/auth/register", json={
            "username": "e2euser",
            "email": "e2e@test.com",
            "password": "test123456",
        })
        assert reg.status_code == 200
        assert reg.json()["data"]["username"] == "e2euser"
        reg_token = reg.json()["data"]["token"]
        assert reg_token

        login = client.post("/api/auth/login", json={
            "username": "e2euser",
            "password": "test123456",
        })
        assert login.status_code == 200
        login_data = login.json()["data"]
        assert login_data["token"]
        assert login_data["user"]["username"] == "e2euser"

    def test_auth_me_with_token(self, client):
        """用 token 访问 /auth/me 应返回用户信息。"""
        reg = client.post("/api/auth/register", json={
            "username": "meuser",
            "email": "me@test.com",
            "password": "test123456",
        })
        token = reg.json()["data"]["token"]

        me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me.status_code == 200
        assert me.json()["data"]["username"] == "meuser"
        assert me.json()["data"]["email"] == "me@test.com"

    def test_query_history_empty_then_ask(self, client):
        """新用户查询历史为空，提交查询后历史应有记录。"""
        reg = client.post("/api/auth/register", json={
            "username": "queryuser2",
            "email": "q2@test.com",
            "password": "test123456",
        })
        token = reg.json()["data"]["token"]
        headers = {"Authorization": f"Bearer {token}"}

        history = client.get("/api/query/history", headers=headers)
        assert history.status_code == 200
        assert history.json()["data"]["total"] == 0
        assert history.json()["data"]["items"] == []

        ask = client.post("/api/query/ask", json={"question": "查一下张三的成绩"}, headers=headers)
        assert ask.status_code == 200
        ask_data = ask.json()["data"]
        assert ask_data["query_id"] is not None
        assert ask_data["nl_input"] == "查一下张三的成绩"
        assert ask_data["status"] in ("success", "failed", "rejected")

        history2 = client.get("/api/query/history", headers=headers)
        assert history2.json()["data"]["total"] >= 1

    def test_query_detail_access_control(self, client):
        """用户只能访问自己的查询记录。"""
        reg1 = client.post("/api/auth/register", json={
            "username": "user_a",
            "email": "a@test.com",
            "password": "test123456",
        })
        token_a = reg1.json()["data"]["token"]

        reg2 = client.post("/api/auth/register", json={
            "username": "user_b",
            "email": "b@test.com",
            "password": "test123456",
        })
        token_b = reg2.json()["data"]["token"]

        ask = client.post(
            "/api/query/ask",
            json={"question": "全班平均分是多少"},
            headers={"Authorization": f"Bearer {token_a}"},
        )
        query_id = ask.json()["data"]["query_id"]

        detail_owner = client.get(
            f"/api/query/{query_id}",
            headers={"Authorization": f"Bearer {token_a}"},
        )
        assert detail_owner.status_code == 200

        detail_other = client.get(
            f"/api/query/{query_id}",
            headers={"Authorization": f"Bearer {token_b}"},
        )
        assert detail_other.status_code == 403

    def test_unknown_intent_rejected(self, client):
        """无法识别意图的查询应返回 rejected。"""
        reg = client.post("/api/auth/register", json={
            "username": "rejectuser",
            "email": "reject@test.com",
            "password": "test123456",
        })
        token = reg.json()["data"]["token"]

        ask = client.post(
            "/api/query/ask",
            json={"question": "今天天气怎么样呢"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert ask.status_code == 200
        assert ask.json()["data"]["status"] == "rejected"


class TestSystemEndpoints:
    """系统接口测试。"""

    def test_health_check(self, client):
        """健康检查应返回状态信息。"""
        resp = client.get("/api/system/health")
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["status"] in ("healthy", "degraded", "unhealthy")
        assert "db_connected" in data
        assert "ai_available" in data
        assert "uptime_seconds" in data

    def test_version_info(self, client):
        """版本接口应返回版本号。"""
        resp = client.get("/api/system/version")
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["version"] == "1.0.0"
        assert data["env"] == "development"
