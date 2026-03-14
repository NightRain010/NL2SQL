"""教师业务模型。"""

from sqlalchemy import Column, Integer, String

from backend.db.base import Base, TimestampMixin


class Teacher(Base, TimestampMixin):
    """教师表，NL2SQL 演示查询的业务数据。"""

    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="教师ID")
    name = Column(String(64), nullable=False, comment="姓名")
    title = Column(String(32), nullable=True, comment="职称")
    department = Column(String(64), nullable=False, comment="所属院系")
    phone = Column(String(20), nullable=True, comment="联系电话")
