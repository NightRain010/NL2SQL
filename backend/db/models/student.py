"""学生业务模型。"""

from sqlalchemy import Column, Integer, String, Date, Enum

from backend.db.base import Base, TimestampMixin


class Student(Base, TimestampMixin):
    """学生表，NL2SQL 演示查询的业务数据。"""

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="学生ID")
    name = Column(String(64), nullable=False, comment="姓名")
    gender = Column(Enum("男", "女"), nullable=False, comment="性别")
    birth_date = Column(Date, nullable=True, comment="出生日期")
    grade = Column(String(32), nullable=False, comment="年级")
    class_name = Column(String(32), nullable=False, comment="班级")
    enrollment_date = Column(Date, nullable=False, comment="入学日期")
