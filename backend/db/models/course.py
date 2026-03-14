"""课程业务模型。"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from backend.db.base import Base, TimestampMixin


class Course(Base, TimestampMixin):
    """课程表，NL2SQL 演示查询的业务数据。"""

    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="课程ID")
    name = Column(String(128), nullable=False, comment="课程名称")
    code = Column(String(32), unique=True, nullable=False, comment="课程编号")
    credit = Column(Float, nullable=False, comment="学分")
    teacher_id = Column(
        Integer, ForeignKey("teachers.id"), nullable=False, comment="授课教师"
    )
    semester = Column(String(32), nullable=False, comment="学期")

    teacher = relationship("Teacher", backref="courses")
