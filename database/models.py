# database/models.py
from sqlalchemy import Table, Column, Integer, String, DateTime, JSON, Text, MetaData, ForeignKey, func

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50), unique=True, nullable=False),
    Column("hashed_password", String(255), nullable=False),
    Column("role", String(20), nullable=False),
    Column("created_at", DateTime, server_default=func.now()),
)

reports = Table(
    "reports",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255), nullable=False),
    Column("description", Text),
    Column("query_ast", JSON, nullable=False),
    Column("parameters", JSON),
    Column("schedule", String(100)),
    Column("export_format", String(20), default="json"),
    Column("recipients", JSON),
    Column("status", String(20), default="active"),
    Column("created_by", Integer, ForeignKey("users.id")),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, onupdate=func.now()),
    Column("last_run", DateTime),
    Column("next_run", DateTime),
)

report_executions = Table(
    "report_executions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("report_id", Integer, ForeignKey("reports.id")),
    Column("executed_at", DateTime, server_default=func.now()),
    Column("parameters", JSON),
    Column("result_size", Integer),
    Column("execution_time_ms", Integer),
    Column("error", Text),
    Column("output_url", String(255)),
)

# Optional audit_log
audit_log = Table(
    "audit_log",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("action", String(50)),
    Column("resource_type", String(50)),
    Column("resource_id", Integer),
    Column("details", JSON),
    Column("timestamp", DateTime, server_default=func.now()),
)
