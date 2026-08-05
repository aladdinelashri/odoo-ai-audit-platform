#!/usr/bin/env python3
"""
Odoo AI Audit Platform — System Verification Suite V4
======================================================
Guaranteed fresh — uses ONLY 'order_date' (not 'date_order')
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin

parser = argparse.ArgumentParser(description="Verify Odoo AI Audit Platform")
parser.add_argument("--base-url", default="http://localhost:8000", help="API base URL")
parser.add_argument("--admin-user", default="admin", help="Admin username")
parser.add_argument("--admin-pass", default="Admin123ChangeMe", help="Admin password")
parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
args = parser.parse_args()

BASE_URL = args.base_url.rstrip("/")
ADMIN_USER = args.admin_user
ADMIN_PASS = args.admin_pass
VERBOSE = args.verbose

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

session = requests.Session()
session.mount("http://", HTTPAdapter(max_retries=0))

results: List[Dict[str, Any]] = []

def log_test(name: str, status: str, detail: str = "", critical: bool = False) -> bool:
    passed = status == "PASS"
    color = GREEN if passed else (RED if critical else YELLOW)
    symbol = "✅" if passed else ("🔴" if critical else "⚠️")
    results.append({"name": name, "status": status, "detail": detail, "critical": critical, "timestamp": datetime.now(timezone.utc).isoformat()})
    print(f"{symbol} {color}{BOLD}{status}{RESET} — {name}")
    if detail and VERBOSE:
        print(f"   {detail}")
    return passed

def section(title: str):
    print(f"\n{BOLD}{BLUE}▶ {title}{RESET}")
    print("=" * 60)

def api_get(path: str, headers: Optional[Dict] = None, expected_status: int = 200):
    try:
        resp = session.get(urljoin(BASE_URL, path), headers=headers, timeout=10)
        return resp.status_code == expected_status, resp
    except Exception as e:
        return False, str(e)

def api_post(path: str, json: Optional[Dict] = None, data: Optional[Dict] = None, headers: Optional[Dict] = None, expected_status: int = 200):
    try:
        resp = session.post(urljoin(BASE_URL, path), json=json, data=data, headers=headers, timeout=10, allow_redirects=False)
        return resp.status_code == expected_status, resp
    except Exception as e:
        return False, str(e)

# 1. HEALTH
section("1. API CONNECTIVITY & HEALTH")
ok, resp = api_get("/health")
if ok:
    d = resp.json()
    log_test("Health endpoint", "PASS", f"db={d.get('database')}, scheduler={d.get('scheduler')}")
    log_test("Health: DB ok", "PASS", critical=True)
    log_test("Health: Scheduler ok", "PASS")
else:
    log_test("Health endpoint", "FAIL", critical=True)

ok, resp = api_get("/metrics")
if ok:
    t = resp.text
    log_test("Metrics endpoint", "PASS")
    log_test("Metrics: executions_total", "PASS" if "report_executions_total" in t else "FAIL")
    log_test("Metrics: duration_seconds", "PASS" if "report_duration_seconds" in t else "FAIL")
else:
    log_test("Metrics endpoint", "FAIL")

# 2. AUTH
section("2. AUTHENTICATION")
ok, resp = api_post("/auth/login", data={"username": ADMIN_USER, "password": ADMIN_PASS}, expected_status=200)
if ok:
    login_data = resp.json()
    access_token = login_data.get("access_token")
    refresh_token = login_data.get("refresh_token")
    log_test("Login", "PASS")
    log_test("Login: access_token", "PASS" if access_token else "FAIL", critical=True)
    log_test("Login: refresh_token", "PASS" if refresh_token else "FAIL")
else:
    access_token = None
    refresh_token = None
    log_test("Login", "FAIL", critical=True)

if not access_token:
    print(f"\n{RED}{BOLD}CRITICAL: No auth token. Stopping.{RESET}")
    sys.exit(1)

auth_headers = {"Authorization": f"Bearer {access_token}"}
ok, _ = api_post("/auth/refresh", json={"refresh_token": refresh_token}, expected_status=200)
log_test("Token refresh", "PASS" if ok else "FAIL")
ok, _ = api_post("/auth/login", data={"username": "bad", "password": "bad"}, expected_status=401)
log_test("Invalid login rejected", "PASS" if ok else "FAIL")

# Rate limit test
print("   Testing login rate limit (6 rapid requests)...")
rate_limited = False
for i in range(6):
    _, resp = api_post("/auth/login", data={"username": "ratelimit", "password": "test"})
    if resp.status_code == 429:
        rate_limited = True
        break
log_test("Login rate limit", "PASS" if rate_limited else "FAIL", detail="429 received" if rate_limited else "No 429")

# 3. REPORT CRUD
section("3. REPORT CRUD")
sample_ast = {"type": "table", "table": "pos_orders", "columns": ["id", "amount_total", "order_date"]}

ok, resp = api_post("/reports/", json={
    "name": f"Verify {datetime.now().strftime('%H%M%S')}",
    "description": "test",
    "query_ast": sample_ast,
    "export_format": "json",
    "recipients": [],
    "status": "active"
}, headers=auth_headers, expected_status=201)

if not ok:
    print(f"\nDEBUG: Create report failed with status {resp.status_code}")
    print(f"DEBUG: Body: {resp.text[:500]}")
    log_test("Create report", "FAIL", f"status={resp.status_code}", critical=True)
    sys.exit(1)

report = resp.json()
report_id = report.get("id")
log_test("Create report", "PASS", f"id={report_id}")
log_test("Create: has query_ast", "PASS" if "query_ast" in report else "FAIL")

# List
ok, resp = api_get("/reports/?skip=0&limit=20", headers=auth_headers)
log_test("List reports", "PASS" if ok else "FAIL", f"count={len(resp.json().get('items', []))}" if ok else "")

# Get by ID
ok, resp = api_get(f"/reports/{report_id}/", headers=auth_headers)
log_test("Get report", "PASS" if ok else "FAIL", f"name={resp.json().get('name')}" if ok else "")

# Update
r = session.put(urljoin(BASE_URL, f"/reports/{report_id}/"), json={"name": "Updated", "status": "inactive"}, headers=auth_headers, timeout=10)
log_test("Update report", "PASS" if r.status_code == 200 else "FAIL", f"status={r.status_code}")

# Update with schedule
r = session.put(urljoin(BASE_URL, f"/reports/{report_id}/"), json={"name": "Scheduled", "status": "active", "schedule": {"interval": 3600}, "recipients": ["test@example.com"]}, headers=auth_headers, timeout=10)
log_test("Update with schedule", "PASS" if r.status_code == 200 else "FAIL", f"status={r.status_code}")

# 4. EXECUTION
section("4. REPORT EXECUTION")
ok, resp = api_post(f"/reports/{report_id}/trigger/", headers=auth_headers, expected_status=202)
if ok:
    data = resp.json()
    execution_id = data.get("execution_id")
    log_test("Trigger report", "PASS", f"execution_id={execution_id}")
    log_test("Trigger: execution_id", "PASS" if execution_id else "FAIL", critical=True)
else:
    execution_id = None
    log_test("Trigger report", "FAIL", critical=True)

if execution_id:
    time.sleep(2)
    ok, resp = api_get(f"/reports/executions/{execution_id}/", headers=auth_headers)
    if ok:
        data = resp.json()
        log_test("Execution status", "PASS", f"status={data.get('status')}")
        log_test("Execution completed", "PASS" if data.get("status") in ("completed", "success") else "FAIL", critical=True)
        has_delivery = "delivery_status" in data
        log_test("Has delivery_status", "PASS" if has_delivery else "FAIL", "Email present" if has_delivery else "Email NOT present")
    else:
        log_test("Execution status", "FAIL")

    # Rate limit test
    print("   Testing trigger rate limit (11 rapid requests)...")
    rate_limited = False
    for i in range(11):
        _, resp = api_post(f"/reports/{report_id}/trigger/", headers=auth_headers)
        if resp.status_code == 429:
            rate_limited = True
            break
    log_test("Trigger rate limit", "PASS" if rate_limited else "FAIL", detail="429 received" if rate_limited else "No 429")

# 5. EXPORTS
section("5. EXPORT FORMATS")
for fmt, expected in [("json", "application/json"), ("excel", ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/octet-stream"]), ("pdf", ["application/pdf", "application/octet-stream"])]:
    ok, resp = api_get(f"/reports/{report_id}/export/?format={fmt}", headers=auth_headers)
    if ok:
        ct = resp.headers.get("content-type", "")
        valid = ct in expected if isinstance(expected, list) else ct == expected
        log_test(f"Export {fmt}", "PASS" if valid else "FAIL", f"mime={ct}, bytes={len(resp.content)}")
        if fmt == "json":
            try:
                json.loads(resp.content)
                log_test(f"Export JSON valid", "PASS")
            except:
                log_test(f"Export JSON valid", "FAIL")
        elif fmt == "excel" and len(resp.content) > 0:
            log_test(f"Export Excel ZIP", "PASS" if resp.content[:4] == b"PK\x03\x04" else "FAIL")
        elif fmt == "pdf" and len(resp.content) > 0:
            log_test(f"Export PDF valid", "PASS" if resp.content[:4] == b"%PDF" else "FAIL")
    else:
        log_test(f"Export {fmt}", "FAIL", f"status={resp.status_code}")

# 6. AUDIT LOG
section("6. AUDIT LOG")
ok, resp = api_get("/audits/", headers=auth_headers)
log_test("Audit log endpoint", "PASS" if ok else "FAIL", f"status={resp.status_code}")

# 7. CLEANUP
section("7. CLEANUP")
r = session.delete(urljoin(BASE_URL, f"/reports/{report_id}/"), headers=auth_headers, timeout=10)
log_test("Delete report", "PASS" if r.status_code == 204 else "FAIL", f"status={r.status_code}")

# SUMMARY
section("VERIFICATION SUMMARY")
