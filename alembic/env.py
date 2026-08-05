# alembic/env.py
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Force psycopg2 registration
import psycopg2  # noqa: F401

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Add project root to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import your metadata – make sure database/models.py exists
from database.models import metadata

# Alembic Config object
config = context.config

# Configure logging
fileConfig(config.config_file_name)

target_metadata = metadata

def get_database_url():
    db_type = os.getenv("DATABASE_TYPE", "sqlite").lower()
    if db_type == "postgresql":
        dsn = os.getenv("POSTGRES_DSN")
        if not dsn:
            raise ValueError("POSTGRES_DSN env var required for PostgreSQL")
        return dsn
    else:
        db_path = os.getenv("AUDIT_DB_PATH", "database/storage/audit.db")
        return f"sqlite:///{db_path}"

def run_migrations_offline():
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    # Get the config section as a dict and inject the URL manually
    config_dict = config.get_section(config.config_ini_section)
    config_dict["sqlalchemy.url"] = get_database_url()
    connectable = engine_from_config(
        config_dict,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
