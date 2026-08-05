#!/usr/bin/env python3
"""
Odoo AI Audit Platform — System Verification Suite
====================================================
Run this script against your running instance to get an objective
PASS/FAIL report on every component claimed in the current state.

Usage:
    python verify_system.py
    python verify_system.py --base-url http://localhost:8000
    python verify_system.py --admin-user admin --admin-pass secret
"""

import argparse
import json
import os
import sys
import time
import traceback
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin

# ---------------------------------------------------------------------------
# Configuration & CLI
# ---------------------------------------------------------------------------
parser = argparse.ArgumentParser(description="Verify Odoo AI Audit Platform")
parser.add_argument("--base-url", default="http://localhost:8000", help="API base URL")
parser.add_argument("--admin-user", default="admin", help="Admin username")
parser.add_argument("--admin-pass", default="admin123", help="Admin password")
parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
args = parser.parse_args()

BASE_URL = args.base_url.rstrip("/")
ADMIN_USER = args.admin_user
ADMIN_PASS = args.admin_pass
VERBOSE = args.verbose

# Colored output helpers
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

session = requests.Session()
session.mount("http://", HTTPAdapter(max_retries=0))
session.mount("https://", HTTPAdapter(max_retries=0))

# ---------------------------------------------------------------------------
# Results tracking
# ---------------------------------------------------------------------------
results: List[Dict[str, Any]] = []


def log_test(name: str, status: str, detail: str = "", critical: bool = False) -> bool:
    """Log a test result and return whether it passed."""
    passed = status == "PASS"
    color = GREEN if passed else (RED if critical else YELLOW)
    symbol = "✅" if passed else ("🔴" if critical else "⚠️")

    results.append({
        "name": name,
        "status": status,
        "detail": detail,
        "critical": critical,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    print(f"{symbol} {color}{BOLD}{status}{RESET} — {name}")
    if detail and VERBOSE:
        print(f"   {detail}")
    return passed


def section(title: str):
    print(f"\n{BOLD}{BLUE}▶ {title}{RESET}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# 1. Environment & File System
# ---------------------------------------------------------------------------
section("1. ENVIRONMENT & FILE SYSTEM")

def check_env_var(name: str, critical: bool = True) -> bool:
    value = os.getenv(name)
    if value:
        masked = value[:4] + "***" if "password" in name.lower() or "secret" in name.lower() or "key" in name.lower() else value
        return log_test(f"Env: {name}", "PASS", f"set = {masked}", critical=critical)
    return log_test(f"Env: {name}", "FAIL", "not set", critical=critical)

check_env_var("DATABASE_TYPE")
check_env_var("POSTGRES_DSN")
check_env_var("JWT_SECRET_KEY")
check_env_var("SMTP_HOST", critical=False)
check_env_var("SMTP_USER", critical=False)
check_env_var("SMTP_PASSWORD", critical=False)

# Check key files exist
key_files = [
    "api/main.py",
    "api/auth.py",
    "api/routers/reports.py",
    "database/core/reporting/ast.py",
    "database/core/reporting/builder.py",
    "database/core/reporting/scheduler.py",
    "database/core/reporting/exports.py",
    "database/core/storage/postgresql/postgresql_pool.py",
    "database/core/storage/sqlite/sqlite_pool.py",
]

for f in key_files:
    exists = os.path.exists(f)
    log_test(f"File exists: {f}", "PASS" if exists else "FAIL", critical=("scheduler.py" in f or "exports.py" in f))

# ---------------------------------------------------------------------------
# 2. API CONNECTIVITY & HEALTH
# ---------------------------------------------------------------------------
section("2. API CONNECTIVITY & HEALTH")

def api_get(path: str, headers: Optional[Dict] = None, expected_status: int = 200) -> Tuple[bool, Any]:
    try:
        resp = session.get(urljoin(BASE_URL, path), headers=headers, timeout=10)
        ok = resp.status_code == expected_status
        return ok, resp
    except Exception as e:
        return False, str(e)

def api_post(path: str, json_data: Optional[Dict] = None, headers: Optional[Dict] = None, expected_status: int = 200) -> Tuple[bool, Any]:
    try:
        resp = session.post(urljoin(BASE_URL, path), json=json_data, headers=headers, timeout=10)
        ok = resp.status_code == expected_status
        return ok, resp
    except Exception as e:
        return False, str(e)

# Health check
ok, resp = api_get("/health")
if ok:
    data = resp.json()
    db_status = data.get("database", "unknown")
    sched_status = data.get("scheduler", "unknown")
    log_test("Health endpoint", "PASS", f"db={db_status}, scheduler={sched_status}")
    log_test("Health: DB connected", "PASS" if db_status == "connected" else "FAIL", critical=True)
    log_test("Health: Scheduler ok", "PASS" if sched_status == "ok" else "FAIL", critical=False)
else:
    log_test("Health endpoint", "FAIL", f"status={getattr(resp, 'status_code', resp)}", critical=True)

# Metrics endpoint
ok, resp = api_get("/metrics")
if ok:
    text = resp.text
    has_executions = "report_executions_total" in text
    has_duration = "report_duration_seconds" in text
    log_test("Metrics endpoint", "PASS")
    log_test("Metrics: report_executions_total", "PASS" if has_executions else "FAIL")
    log_test("Metrics: report_duration_seconds", "PASS" if has_duration else "FAIL")
else:
    log_test("Metrics endpoint", "FAIL", critical=False)

# ---------------------------------------------------------------------------
# 3. AUTHENTICATION
# ---------------------------------------------------------------------------
section("3. AUTHENTICATION")

# Login
ok, resp = api_post("/auth/login", {"username": ADMIN_USER, "password": ADMIN_PASS}, expected_status=200)
if ok:
    login_data = resp.json()
    access_token = login_data.get("access_token")
    refresh_token = login_data.get("refresh_token")
    role = login_data.get("role")
    log_test("Login endpoint", "PASS", f"role={role}")
    log_test("Login returns access_token", "PASS" if access_token else "FAIL", critical=True)
    log_test("Login returns refresh_token", "PASS" if refresh_token else "FAIL")
    log_test("Login returns role", "PASS" if role else "FAIL")
else:
    access_token = None
    log_test("Login endpoint", "FAIL", f"status={getattr(resp, 'status_code', resp)}", critical=True)

if not access_token:
    print(f"\n{RED}{BOLD}CRITICAL: Cannot authenticate. Skipping protected endpoint tests.{RESET}")
    auth_headers = {}
else:
    auth_headers = {"Authorization": f"Bearer {access_token}"}

    # Token refresh
    ok, resp = api_post("/auth/refresh", headers={"Authorization": f"Bearer {refresh_token}"}, expected_status=200)
    log_test("Token refresh", "PASS" if ok else "FAIL")

    # Invalid login
    ok, resp = api_post("/auth/login", {"username": "bad", "password": "bad"}, expected_status=401)
    log_test("Invalid login rejected", "PASS" if ok else "FAIL")

# ---------------------------------------------------------------------------
# 4. RATE LIMITING
# ---------------------------------------------------------------------------
section("4. RATE LIMITING")

if access_token:
    # Test login rate limit (5/min)
    print("   Testing login rate limit (6 rapid requests)...")
    rate_limited = False
    for i in range(6):
        ok, resp = api_post("/auth/login", {"username": "ratelimit", "password": "test"})
        if resp.status_code == 429:
            rate_limited = True
            break
    log_test("Login rate limit (5/min)", "PASS" if rate_limited else "FAIL", 
             detail="429 received" if rate_limited else "No 429 after 6 requests")

    # Test trigger rate limit (10/min) — need a report first
    # Will test after report creation

# ---------------------------------------------------------------------------
# 5. REPORT CRUD
# ---------------------------------------------------------------------------
section("5. REPORT CRUD (Admin Protected)")

created_report_id = None

if access_token:
    sample_ast = {
        "type": "table",
        "table": "pos_orders",
        "columns": ["id", "amount_total", "date_order"]
    }

    # Create
    ok, resp = api_post("/reports", {
        "name": f"Verification Report {datetime.now().strftime('%H%M%S')}",
        "description": "Auto-generated verification report",
        "ast_query": sample_ast,
        "schedule_config": None,
        "export_format": "json",
        "email_recipients": [],
        "is_active": True
    }, headers=auth_headers, expected_status=201)

    if ok:
        report = resp.json()
        created_report_id = report.get("id")
        log_test("Create report", "PASS", f"id={created_report_id}")
        log_test("Create report returns AST", "PASS" if "ast_query" in report else "FAIL")
        log_test("Create report returns name", "PASS" if report.get("name") else "FAIL")
    else:
        log_test("Create report", "FAIL", f"status={resp.status_code if hasattr(resp, 'status_code') else resp}", critical=True)

    if created_report_id:
        # List
        ok, resp = api_get("/reports?skip=0&limit=20", headers=auth_headers)
        if ok:
            data = resp.json()
            has_items = "items" in data and isinstance(data["items"], list)
            log_test("List reports", "PASS", f"count={len(data.get('items', []))}")
        else:
            log_test("List reports", "FAIL")

        # Get by ID
        ok, resp = api_get(f"/reports/{created_report_id}", headers=auth_headers)
        if ok:
            data = resp.json()
            log_test("Get report by ID", "PASS", f"name={data.get('name', 'N/A')}")
        else:
            log_test("Get report by ID", "FAIL")

        # Update
        ok, resp = session.put(
            urljoin(BASE_URL, f"/reports/{created_report_id}"),
            json={"name": "Updated Verification Report", "is_active": False},
            headers=auth_headers,
            timeout=10
        )
        if ok.status_code == 200:
            data = ok.json()
            log_test("Update report", "PASS", f"new_name={data.get('name')}, active={data.get('is_active')}")
        else:
            log_test("Update report", "FAIL", f"status={ok.status_code}")

        # Update with schedule
        ok, resp = session.put(
            urljoin(BASE_URL, f"/reports/{created_report_id}"),
            json={
                "name": "Scheduled Verification Report",
                "is_active": True,
                "schedule_config": {"interval": 3600},
                "email_recipients": ["verify@example.com"]
            },
            headers=auth_headers,
            timeout=10
        )
        if ok.status_code == 200:
            log_test("Update report with schedule", "PASS")
        else:
            log_test("Update report with schedule", "FAIL", f"status={ok.status_code}")
else:
    log_test("Report CRUD", "SKIP", "No auth token available", critical=True)

# ---------------------------------------------------------------------------
# 6. REPORT EXECUTION (MANUAL TRIGGER)
# ---------------------------------------------------------------------------
section("6. REPORT EXECUTION (Manual Trigger)")

execution_id = None

if created_report_id and access_token:
    ok, resp = api_post(f"/reports/{created_report_id}/trigger", headers=auth_headers, expected_status=202)
    if ok:
        data = resp.json()
        execution_id = data.get("execution_id")
        log_test("Trigger report", "PASS", f"execution_id={execution_id}")
        log_test("Trigger returns execution_id", "PASS" if execution_id else "FAIL", critical=True)
        log_test("Trigger returns status=queued", "PASS" if data.get("status") == "queued" else "FAIL")
    else:
        log_test("Trigger report", "FAIL", f"status={resp.status_code if hasattr(resp, 'status_code') else resp}", critical=True)

    # Check execution status
    if execution_id:
        time.sleep(2)  # Allow execution to complete
        ok, resp = api_get(f"/reports/executions/{execution_id}", headers=auth_headers)
        if ok:
            data = resp.json()
            status = data.get("status")
            log_test("Get execution status", "PASS", f"status={status}")
            log_test("Execution completed", "PASS" if status in ("completed", "success") else "FAIL", critical=True)

            # Check delivery status field exists (email integration marker)
            if "delivery_status" in data:
                log_test("Execution has delivery_status field", "PASS", f"value={data.get('delivery_status')}")
            else:
                log_test("Execution has delivery_status field", "FAIL", "Field missing — email integration not present")
        else:
            log_test("Get execution status", "FAIL")

    # Test trigger rate limit (10/min)
    print("   Testing trigger rate limit (11 rapid requests)...")
    rate_limited = False
    for i in range(11):
        ok, resp = api_post(f"/reports/{created_report_id}/trigger", headers=auth_headers)
        if resp.status_code == 429:
            rate_limited = True
            break
    log_test("Trigger rate limit (10/min)", "PASS" if rate_limited else "FAIL",
             detail="429 received" if rate_limited else "No 429 after 11 requests")
else:
    log_test("Report execution", "SKIP", "No report created or no auth", critical=True)

# ---------------------------------------------------------------------------
# 7. EXPORT FORMATS
# ---------------------------------------------------------------------------
section("7. EXPORT FORMATS")

if created_report_id and access_token:
    formats = [
        ("json", "application/json"),
        ("excel", ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/octet-stream"]),
        ("pdf", ["application/pdf", "application/octet-stream"]),
    ]

    for fmt, expected_mime in formats:
        ok, resp = api_get(f"/reports/{created_report_id}/export?format={fmt}", headers=auth_headers)
        if ok:
            content_type = resp.headers.get("content-type", "")
            content_length = len(resp.content)
            mime_ok = content_type in expected_mime if isinstance(expected_mime, list) else content_type == expected_mime

            log_test(f"Export {fmt.upper()}", "PASS" if mime_ok else "FAIL",
                     f"mime={content_type}, bytes={content_length}")

            # Validate file integrity
            if fmt == "json":
                try:
                    json.loads(resp.content)
                    log_test(f"Export JSON valid", "PASS")
                except Exception as e:
                    log_test(f"Export JSON valid", "FAIL", str(e))
            elif fmt == "excel" and content_length > 0:
                # Check for ZIP signature (xlsx is a zip file)
                is_zip = resp.content[:4] == b"PK\x03\x04"
                log_test(f"Export Excel is valid ZIP", "PASS" if is_zip else "FAIL")
            elif fmt == "pdf" and content_length > 0:
                is_pdf = resp.content[:4] == b"%PDF"
                log_test(f"Export PDF is valid PDF", "PASS" if is_pdf else "FAIL")
        else:
            log_test(f"Export {fmt.upper()}", "FAIL", f"status={resp.status_code if hasattr(resp, 'status_code') else resp}")
else:
    log_test("Export formats", "SKIP", "No report created or no auth")

# ---------------------------------------------------------------------------
# 8. SCHEDULER VERIFICATION
# ---------------------------------------------------------------------------
section("8. SCHEDULER VERIFICATION")

# Check if scheduler actually loaded jobs from DB
if access_token:
    ok, resp = api_get("/health")
    if ok:
        data = resp.json()
        sched = data.get("scheduler", "unknown")
        log_test("Scheduler health status", "PASS" if sched == "ok" else "FAIL", f"status={sched}")

    # We can't easily verify scheduled jobs fire without waiting, but we can
    # check if the report we created with a schedule is in the scheduler
    # This requires an internal endpoint or checking the DB directly
    print(f"   {YELLOW}Note: Automatic job firing cannot be verified without waiting.{RESET}")
    print(f"   {YELLOW}Create a report with {{'interval': 60}} and check report_executions in 2 minutes.{RESET}")

# ---------------------------------------------------------------------------
# 9. EMAIL DELIVERY VERIFICATION
# ---------------------------------------------------------------------------
section("9. EMAIL DELIVERY VERIFICATION")

# Check if email config is present
smtp_vars = ["SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD", "SMTP_FROM"]
smtp_configured = all(os.getenv(v) for v in smtp_vars)
log_test("SMTP fully configured", "PASS" if smtp_configured else "FAIL",
         detail="All SMTP vars set" if smtp_configured else "Some SMTP vars missing")

# Check if execution record has delivery fields
if execution_id and access_token:
    ok, resp = api_get(f"/reports/executions/{execution_id}", headers=auth_headers)
    if ok:
        data = resp.json()
        has_delivery = "delivery_status" in data
        has_delivery_error = "delivery_error" in data
        log_test("Execution record has delivery_status", "PASS" if has_delivery else "FAIL",
                 "Email integration present" if has_delivery else "Email integration NOT present — scheduler.py may not be integrated")
        log_test("Execution record has delivery_error", "PASS" if has_delivery_error else "FAIL")
    else:
        log_test("Email delivery check", "FAIL", "Could not fetch execution")
else:
    log_test("Email delivery check", "SKIP", "No execution to check")

# ---------------------------------------------------------------------------
# 10. AUDIT LOG VERIFICATION
# ---------------------------------------------------------------------------
section("10. AUDIT LOG VERIFICATION")

if access_token:
    ok, resp = api_get("/audits", headers=auth_headers)
    if ok:
        data = resp.json()
        has_items = "items" in data
        count = len(data.get("items", []))
        log_test("Audit log endpoint", "PASS", f"entries={count}")

        # Check if our report creation was logged
        if count > 0:
            recent = data["items"][:5]
            actions = [r.get("action") for r in recent]
            has_create = "create_report" in actions or "CREATE" in [a.upper() for a in actions]
            log_test("Audit log captures admin actions", "PASS" if has_create else "FAIL",
                     f"recent_actions={actions}")
    else:
        log_test("Audit log endpoint", "FAIL", f"status={resp.status_code if hasattr(resp, 'status_code') else resp}")
else:
    log_test("Audit log", "SKIP", "No auth token")

# ---------------------------------------------------------------------------
# 11. CLEANUP
# ---------------------------------------------------------------------------
section("11. CLEANUP")

if created_report_id and access_token:
    ok = session.delete(urljoin(BASE_URL, f"/reports/{created_report_id}"), headers=auth_headers, timeout=10)
    if ok.status_code == 204:
        log_test("Delete report", "PASS", f"id={created_report_id}")
    else:
        log_test("Delete report", "FAIL", f"status={ok.status_code}")
else:
    log_test("Cleanup", "SKIP", "No report to delete")

# ---------------------------------------------------------------------------
# SUMMARY REPORT
# ---------------------------------------------------------------------------
section("VERIFICATION SUMMARY")

total = len(results)
passed = sum(1 for r in results if r["status"] == "PASS")
failed = sum(1 for r in results if r["status"] == "FAIL")
skipped = sum(1 for r in results if r["status"] == "SKIP")
critical_failures = [r for r in results if r["status"] == "FAIL" and r.get("critical")]

print(f"""
┌─────────────────────────────────────────────────────────────┐
│  TOTAL TESTS: {total:3d}                                          │
│  ✅ PASSED:    {passed:3d}                                          │
│  🔴 FAILED:    {failed:3d}                                          │
│  ⏭️  SKIPPED:   {skipped:3d}                                          │
│  🔴 CRITICAL FAILURES: {len(critical_failures):3d}                          │
└─────────────────────────────────────────────────────────────┘
""")

if critical_failures:
    print(f"{RED}{BOLD}CRITICAL FAILURES — MUST FIX BEFORE PRODUCTION:{RESET}")
    for r in critical_failures:
        print(f"  🔴 {r['name']}")
        if r.get("detail"):
            print(f"     → {r['detail']}")

print(f"\n{BOLD}Detailed results written to: verification_report.json{RESET}")

# Write JSON report
with open("verification_report.json", "w") as f:
    json.dump({
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "critical_failures": len(critical_failures),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "base_url": BASE_URL,
        },
        "results": results,
    }, f, indent=2, default=str)

# Exit code
sys.exit(0 if len(critical_failures) == 0 else 1)
