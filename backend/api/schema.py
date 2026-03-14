"""Schema 路由：获取数据库表列表、表结构详情、刷新元数据。"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import inspect as sa_inspect

from backend.db.engine import get_db, engine
from backend.db.models.schema_meta import SchemaMetadata
from backend.lib.response import success

router = APIRouter()


@router.get("/tables")
def list_tables(db: Session = Depends(get_db)):
    """获取所有业务表列表。"""
    tables_query = (
        db.query(
            SchemaMetadata.table_name,
            SchemaMetadata.comment,
        )
        .distinct(SchemaMetadata.table_name)
        .all()
    )

    table_names = set()
    tables = []
    for row in tables_query:
        if row.table_name in table_names:
            continue
        table_names.add(row.table_name)
        col_count = (
            db.query(SchemaMetadata)
            .filter(SchemaMetadata.table_name == row.table_name)
            .count()
        )
        tables.append({
            "name": row.table_name,
            "comment": row.comment,
            "column_count": col_count,
        })

    return success(data={"tables": tables})


@router.get("/tables/{table_name}")
def get_table_detail(table_name: str, db: Session = Depends(get_db)):
    """获取指定表的详细结构。"""
    columns = (
        db.query(SchemaMetadata)
        .filter(SchemaMetadata.table_name == table_name)
        .all()
    )
    if not columns:
        raise HTTPException(status_code=404, detail=f"表 '{table_name}' 不存在")

    return success(data={
        "table_name": table_name,
        "columns": [
            {
                "name": col.column_name,
                "type": col.column_type,
                "comment": col.comment,
                "is_primary": col.is_primary,
                "is_nullable": col.is_nullable,
            }
            for col in columns
        ],
        "row_count": None,
    })


@router.post("/refresh")
def refresh_metadata(db: Session = Depends(get_db)):
    """重新扫描数据库表结构，刷新 schema_metadata 缓存。"""
    inspector = sa_inspect(engine)
    table_names = inspector.get_table_names()

    db.query(SchemaMetadata).filter(
        SchemaMetadata.table_name.in_(table_names)
    ).delete(synchronize_session="fetch")

    total_columns = 0
    for table_name in table_names:
        columns = inspector.get_columns(table_name)
        pk_columns = {
            col["name"]
            for col in inspector.get_pk_constraint(table_name).get("constrained_columns", [])
        } if inspector.get_pk_constraint(table_name) else set()

        for col in columns:
            meta = SchemaMetadata(
                table_name=table_name,
                column_name=col["name"],
                column_type=str(col["type"]),
                is_primary=col["name"] in pk_columns,
                is_nullable=col.get("nullable", True),
                comment=col.get("comment"),
            )
            db.add(meta)
            total_columns += 1

    db.commit()

    return success(data={
        "refreshed_tables": len(table_names),
        "total_columns": total_columns,
    })
