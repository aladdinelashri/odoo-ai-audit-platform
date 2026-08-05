"""Pytest fixtures."""
import os
import pytest
import tempfile
import shutil
from fastapi.testclient import TestClient

# Set test environment before imports
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["INITIAL_ADMIN_PASSWORD"] = "Admin123ChangeMe"
os.environ["POSTGRES_DB"] = "odoo_audit_test"
os.environ["SQLITE_PATH"] = "test_audit.db"
os.environ["SMTP_PASSWORD"] = "test-smtp-password"
os.environ["API_KEY"] = "test-api-key"

from api.main import create_app
from database.core.storage.sqlite.sqlite_pool import SQLitePool


@pytest.fixture(scope="session")
def test_sqlite_path():
    """Create temporary SQLite database."""
    tmpdir = tempfile.mkdtemp()
    db_path = os.path.join(tmpdir, "test_audit.db")
    os.environ["SQLITE_PATH"] = db_path
    yield db_path
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture(scope="session")
def app(test_sqlite_path):
    """Create test app."""
    # Initialize test SQLite
    sqlite_pool = SQLitePool(test_sqlite_path)
    
    # Create admin user if your main.py doesn't do it automatically
    from api.auth import init_admin_user
    init_admin_user()
    
    return create_app()


@pytest.fixture
def client(app):
    """Test client."""
    return TestClient(app)


@pytest.fixture
def admin_token(client):
    """Get admin JWT token."""
    response = client.post(
        "/auth/login",
        data={"username": "admin", "password": "Admin123ChangeMe"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(admin_token):
    """Authorization headers with admin token."""
    return {"Authorization": f"Bearer {admin_token}"}
