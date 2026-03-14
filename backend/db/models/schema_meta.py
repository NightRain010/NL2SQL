"""表结构元数据缓存模型。"""

from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint

from backend.db.base import Base, TimestampMixin


class SchemaMetadata(Base, TimestampMixin):
    """表结构元数据缓存表，用于 Schema 感知 Agent 快速检索表结构信息。"""

    __tablename__ = "schema_metadata"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="元数据ID")
    table_name = Column(String(128), nullable=False, index=True, comment="表名")
    column_name = Column(String(128), nullable=False, comment="字段名")
    column_type = Column(String(64), nullable=False, comment="字段类型")
    is_primary = Column(Boolean, default=False, comment="是否为主键")
    is_nullable = Column(Boolean, default=True, comment="是否允许 NULL")
    comment = Column(String(512), nullable=True, comment="字段注释")

    __table_args__ = (
        UniqueConstraint("table_name", "column_name", name="uq_table_column"),
    )
