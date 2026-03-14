"""ORM 模型统一导出。"""

from backend.db.models.user import User
from backend.db.models.query_history import QueryHistory
from backend.db.models.schema_meta import SchemaMetadata
from backend.db.models.student import Student
from backend.db.models.teacher import Teacher
from backend.db.models.course import Course
from backend.db.models.score import Score

__all__ = [
    "User",
    "QueryHistory",
    "SchemaMetadata",
    "Student",
    "Teacher",
    "Course",
    "Score",
]
