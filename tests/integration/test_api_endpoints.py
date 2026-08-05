"""Integration tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient


class TestAuth:
    """Test authentication endpoints."""

    def test_login_form_data(self, client: TestClient):
        response = client.post(
            "/auth/login",
            data={"username": "admin", "password": "Admin123ChangeMe"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_json_fails(self, client: TestClient):
        """Ensure JSON login is NOT accepted (spec requirement)."""
        response = client.post(
            "/auth/login",
            json={"username": "admin", "password": "Admin123ChangeMe"},
        )
        assert response.status_code == 422

    def test_login_wrong_password(self, client: TestClient):
        response = client.post(
            "/auth/login",
            data={"username": "admin", "password": "wrongpassword"},
        )
        assert response.status_code == 401


class TestReportCRUD:
    """Test report CRUD operations."""

    def test_create_report(self, client: TestClient, auth_headers: dict):
        payload = {
            "name": "Test Report",
            "description": "Integration test",
            "query_ast": {
                "select": ["id", "order_name", "amount_total"],
                "from": "pos_orders",
                "limit": 10,
            },
            "recipients": ["test@example.com"],
            "status": "active",
        }
        response = client.post("/reports/", params=payload, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Report"
        assert data["query_ast"] is not None
        return data["id"]

    def test_list_reports(self, client: TestClient, auth_headers: dict):
        response = client.get("/reports/?skip=0&limit=20", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_report(self, client: TestClient, auth_headers: dict):
        # Create first
        create_resp = client.post(
            "/reports/",
            params={
                "name": "Get Test",
                "query_ast": {"select": ["id"], "from": "pos_orders", "limit": 5},
            },
            headers=auth_headers,
        )
        report_id = create_resp.json()["id"]
        
        response = client.get(f"/reports/{report_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["id"] == report_id

    def test_update_report(self, client: TestClient, auth_headers: dict):
        create_resp = client.post(
            "/reports/",
            params={
                "name": "Update Test",
                "query_ast": {"select": ["id"], "from": "pos_orders", "limit": 5},
            },
            headers=auth_headers,
        )
        report_id = create_resp.json()["id"]
        
        response = client.put(
            f"/reports/{report_id}",
            params={"name": "Updated Name", "status": "inactive"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Name"

    def test_delete_report(self, client: TestClient, auth_headers: dict):
        create_resp = client.post(
            "/reports/",
            params={
                "name": "Delete Test",
                "query_ast": {"select": ["id"], "from": "pos_orders", "limit": 5},
            },
            headers=auth_headers,
        )
        report_id = create_resp.json()["id"]
        
        response = client.delete(f"/reports/{report_id}", headers=auth_headers)
        assert response.status_code == 204


class TestReportTrigger:
    """Test report execution."""

    def test_trigger_report(self, client: TestClient, auth_headers: dict):
        # Create report
        create_resp = client.post(
            "/reports/",
            params={
                "name": "Trigger Test",
                "query_ast": {
                    "select": ["id", "order_name", "amount_total"],
                    "from": "pos_orders",
                    "where": {"field": "state", "op": "=", "value": "paid"},
                    "limit": 10,
                },
                "recipients": [],
            },
            headers=auth_headers,
        )
        report_id = create_resp.json()["id"]
        
        # Trigger
        response = client.post(f"/reports/{report_id}/trigger", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)


class TestExportEndpoint:
    """Test Priority 1: Export endpoint."""

    def test_export_json(self, client: TestClient, auth_headers: dict):
        create_resp = client.post(
            "/reports/",
            params={
                "name": "Export JSON Test",
                "query_ast": {"select": ["id"], "from": "pos_orders", "limit": 5},
            },
            headers=auth_headers,
        )
        report_id = create_resp.json()["id"]
        
        response = client.get(
            f"/reports/{report_id}/export?format=json",
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert "Export JSON Test.json" in response.headers["content-disposition"]
        import json
        data = json.loads(response.content)
        assert isinstance(data, list)

    def test_export_excel(self, client: TestClient, auth_headers: dict):
        create_resp = client.post(
            "/reports/",
            params={
                "name": "Export Excel Test",
                "query_ast": {"select": ["id"], "from": "pos_orders", "limit": 5},
            },
            headers=auth_headers,
        )
        report_id = create_resp.json()["id"]
        
        response = client.get(
            f"/reports/{report_id}/export?format=excel",
            headers=auth_headers,
        )
        assert response.status_code == 200
        # ZIP signature for XLSX
        assert response.content[:4] == b"PK\x03\x04"

    def test_export_pdf(self, client: TestClient, auth_headers: dict):
        create_resp = client.post(
            "/reports/",
            params={
                "name": "Export PDF Test",
                "query_ast": {"select": ["id"], "from": "pos_orders", "limit": 5},
            },
            headers=auth_headers,
        )
        report_id = create_resp.json()["id"]
        
        response = client.get(
            f"/reports/{report_id}/export?format=pdf",
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.content[:4] == b"%PDF"


class TestRateLimiting:
    """Test rate limiting on login."""

    def test_login_rate_limit(self, client: TestClient):
        # Make 5 failed attempts
        for _ in range(5):
            client.post(
                "/auth/login",
                data={"username": "admin", "password": "wrong"},
            )
        
        # 6th attempt should be rate limited
        response = client.post(
            "/auth/login",
            data={"username": "admin", "password": "wrong"},
        )
        assert response.status_code == 429


class TestAuditLog:
    """Test audit log API key auth."""

    def test_audit_without_api_key(self, client: TestClient):
        response = client.get("/audits/")
        assert response.status_code == 401

    def test_audit_with_api_key(self, client: TestClient):
        response = client.get(
            "/audits/",
            headers={"X-API-KEY": "test-api-key"},
        )
        assert response.status_code == 200
