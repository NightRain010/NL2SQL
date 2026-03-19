# 后端：API 路由层

## 模块位置

`backend/api/`

## 路由清单

### 认证 `/api/auth`
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /register | 注册（username + email + password） |
| POST | /login | 登录，返回 JWT token |
| GET | /me | 获取当前用户信息（需 Bearer token） |

### 查询 `/api/query`
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /ask | 提交自然语言查询，返回 SQL + 结果 |
| GET | /history | 分页获取查询历史（?page=&size=&status=） |
| GET | /{query_id} | 获取查询详情（仅本人可查看） |

### Schema `/api/schema`
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /tables | 获取所有表列表 |
| GET | /tables/{name} | 获取表字段详情 |
| POST | /refresh | 刷新 schema_metadata 缓存 |

### 系统 `/api/system`
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /health | 健康检查（db_connected + ai_available） |
| GET | /version | 版本信息 |

## 统一响应格式

```python
{"code": 200, "message": "success", "data": {...}}
```

错误码：400（参数错误）、401（未认证）、403（无权限）、404（不存在）、422（校验不通过）、500（服务器错误）、503（AI 不可用）

## 认证机制

- JWT Token，通过 `Authorization: Bearer <token>` 传递
- `get_current_user_id()` 依赖注入解析 token
- 密码使用 bcrypt 直接哈希（注意：不用 passlib，因为 passlib 与 bcrypt>=5.0 不兼容）

## 测试

- `test_api_auth.py`：5 个用例（注册/登录/重复用户名/短密码/错误密码）
- `test_api_query.py`：3 个用例（未认证/空历史/短问题）
- `test_e2e_flow.py`：7 个用例（完整注册→登录→查询→权限控制流程）
