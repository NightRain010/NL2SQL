"""SQL 白名单校验器测试。"""

from backend.lib.sql_validator import validate_sql, sanitize_sql


class TestValidateSQL:
    """validate_sql 函数测试。"""

    def test_valid_select(self):
        """正常 SELECT 语句应通过校验。"""
        is_valid, errors = validate_sql("SELECT * FROM students")
        assert is_valid is True
        assert errors == []

    def test_valid_select_with_where(self):
        """带 WHERE 子句的 SELECT 应通过。"""
        sql = "SELECT name, score FROM scores WHERE score > 60"
        is_valid, errors = validate_sql(sql)
        assert is_valid is True

    def test_valid_select_with_join(self):
        """带 JOIN 的 SELECT 应通过。"""
        sql = "SELECT s.name, c.name FROM students s JOIN scores sc ON s.id = sc.student_id"
        is_valid, errors = validate_sql(sql)
        assert is_valid is True

    def test_reject_insert(self):
        """INSERT 语句应被拒绝。"""
        is_valid, errors = validate_sql("INSERT INTO students VALUES (1, '张三')")
        assert is_valid is False

    def test_reject_update(self):
        """UPDATE 语句应被拒绝。"""
        is_valid, errors = validate_sql("UPDATE students SET name='李四' WHERE id=1")
        assert is_valid is False

    def test_reject_delete(self):
        """DELETE 语句应被拒绝。"""
        is_valid, errors = validate_sql("DELETE FROM students WHERE id=1")
        assert is_valid is False

    def test_reject_drop(self):
        """DROP 语句应被拒绝。"""
        is_valid, errors = validate_sql("DROP TABLE students")
        assert is_valid is False

    def test_reject_select_into(self):
        """SELECT INTO 应被拒绝。"""
        is_valid, errors = validate_sql("SELECT * INTO new_table FROM students")
        assert is_valid is False

    def test_empty_sql(self):
        """空 SQL 应被拒绝。"""
        is_valid, errors = validate_sql("")
        assert is_valid is False

    def test_trailing_semicolon(self):
        """尾部分号不影响校验。"""
        is_valid, errors = validate_sql("SELECT * FROM students;")
        assert is_valid is True


class TestSanitizeSQL:
    """sanitize_sql 函数测试。"""

    def test_sanitize_valid(self):
        """合法 SQL 应返回清理后的字符串。"""
        result = sanitize_sql("  SELECT * FROM students ;  ")
        assert result == "SELECT * FROM students"

    def test_sanitize_invalid_returns_none(self):
        """非法 SQL 应返回 None。"""
        result = sanitize_sql("DROP TABLE students")
        assert result is None
