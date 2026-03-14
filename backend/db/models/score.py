"""成绩业务模型。"""

from sqlalchemy import Column, Integer, Float, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from backend.db.base import Base, TimestampMixin


class Score(Base, TimestampMixin):
    """成绩表，NL2SQL 演示查询的业务数据。"""

    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="成绩ID")
    student_id = Column(
        Integer, ForeignKey("students.id"), nullable=False, index=True, comment="学生"
    )
    course_id = Column(
        Integer, ForeignKey("courses.id"), nullable=False, index=True, comment="课程"
    )
    score = Column(Float, nullable=False, comment="分数")
    exam_type = Column(
        Enum("期中", "期末", "平时"), nullable=False, comment="考试类型"
    )

    student = relationship("Student", backref="scores")
    course = relationship("Course", backref="scores")

    __table_args__ = (
        UniqueConstraint(
            "student_id", "course_id", "exam_type", name="uq_student_course_exam"
        ),
    )
