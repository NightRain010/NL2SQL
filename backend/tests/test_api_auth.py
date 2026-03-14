"""认证 API 测试。"""

import pytest


class TestRegister:
    """注册接口测试。"""

    def test_register_success(self, client):
        """正常注册应返回用户信息和 token。"""
        resp = client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        })
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["username"] == "testuser"
        assert "token" in data

    def test_register_duplicate_username(self, client):
        """重复用户名应返回 400。"""
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        }
        client.post("/api/auth/register", json=payload)
        resp = client.post("/api/auth/register", json={
            **payload,
            "email": "other@example.com",
        })
        assert resp.status_code == 400

    def test_register_short_password(self, client):
        """密码过短应返回 422。"""
        resp = client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "123",
        })
        assert resp.status_code == 422


class TestLogin:
    """登录接口测试。"""

    def test_login_success(self, client):
        """正确凭据应登录成功。"""
        client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        })
        resp = client.post("/api/auth/login", json={
            "username": "testuser",
            "password": "password123",
        })
        assert resp.status_code == 200
        assert "token" in resp.json()["data"]

    def test_login_wrong_password(self, client):
        """错误密码应返回 401。"""
        client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        })
        resp = client.post("/api/auth/login", json={
            "username": "testuser",
            "password": "wrongpassword",
        })
        assert resp.status_code == 401
