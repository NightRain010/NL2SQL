"""查询历史模型。"""

from sqlalchemy import Column, Integer, String, Text, JSON, Enum, ForeignKey
from sqlalchemy.orm import relationship

from backend.db.base import Base, TimestampMixin


class QueryHistory(Base, TimestampMixin):
    """查询历史表，记录每次自然语言查询的完整生命周期。"""

    __tablename__ = "query_history"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="记录ID")
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True, comment="关联用户"
    )
    nl_input = Column(Text, nullable=False, comment="用户自然语言输入")
    intent_type = Column(String(32), nullable=True, comment="识别到的意图类型")
    generated_sql = Column(Text, nullable=True, comment="AI 生成的 SQL 语句")
    query_result = Column(JSON, nullable=True, comment="查询结果（JSON 序列化）")
    status = Column(
        Enum("pending", "success", "failed", "rejected"),
        default="pending",
        nullable=False,
        comment="查询状态",
    )
    error_message = Column(Text, nullable=True, comment="错误信息")
    execution_ms = Column(Integer, nullable=True, comment="SQL 执行耗时（毫秒）")

    user = relationship("User", backref="queries")
