# 后端：数据库层

## 模块位置

`backend/db/`

## 数据库连接

- `engine.py`：SQLAlchemy engine + SessionLocal
- `get_db()` 生成器用于 FastAPI 依赖注入
- 连接串：`mysql+pymysql://...?charset=utf8mb4`
- 配置来自 `.env`，端口 8306（Docker 映射，因本机 Hyper-V 占用 3306）

## ORM 模型

### 平台表
| 表 | 文件 | 说明 |
|----|------|------|
| users | user.py | 用户（username/email/password_hash/is_active） |
| query_history | query_history.py | 查询记录（nl_input/generated_sql/status/execution_ms） |
| schema_metadata | schema_meta.py | 表结构缓存（table_name/column_name/column_type） |

### 业务示例表
| 表 | 文件 | 说明 |
|----|------|------|
| students | student.py | 学生（name/gender/grade/class_name） |
| teachers | teacher.py | 教师（name/title/department） |
| courses | course.py | 课程（name/code/credit，FK→teachers） |
| scores | score.py | 成绩（score/exam_type，FK→students+courses） |

### 公共基类
- `base.py`：`Base = declarative_base()` + `TimestampMixin`（created_at/updated_at）

## CRUD

- `user_crud.py`：get_by_id / get_by_username / get_by_email / create_user
- `query_crud.py`：create_query_record / update_query_result / get_by_id / list_by_user（分页）

## 字符集规范

- MySQL 启动参数：`--character-set-client-handshake=FALSE --init-connect='SET NAMES utf8mb4'`
- 建表必须 `DEFAULT CHARSET=utf8mb4`
- SQL 初始化脚本开头加 `SET NAMES utf8mb4;`

## 测试

- `test_db.py`：3 个用例（创建用户、按用户名查询、查询不存在用户）
- 测试使用 SQLite 文件数据库（`test.db`），已加入 `.gitignore`
