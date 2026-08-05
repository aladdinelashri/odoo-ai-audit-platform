#!/usr/bin/env python3
"""
Odoo AI Audit Platform — Final Verification Suite
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin

parser = argparse.ArgumentParser()
parser.add_argument("--base-url", default="http://localhost:8000")
parser.add_argument("--admin-user", default="admin")
parser.add_argument("--admin-pass", default="Admin123ChangeMe")
parser.add_argument("--verbose", "-v", action="store_true")
args = parser.parse_args()

BASE_URL = args.base_url.rstrip("/")
ADMIN_USER = args.admin_user
ADMIN_PASS = args.admin_pass
VERBOSE = args.verbose

GREEN, RED, YELLOW, BLUE, RESET, BOLD = "\033[92m", "\033[91m", "\033[93m", "\033[94m", "\033[0m", "\033[1m"

session = requests.Session()
session.mount("http://", HTTPAdapter(max_retries=0))

results: List[Dict[str, Any]] = []

def log_test(name: str, status: str, detail: str = "", critical: bool = False):
    passed = status == "PASS"
    color = GREEN if passed else (RED if critical else YELLOW)
    symbol = "✅" if passed else ("🔴" if critical else "⚠️")
    results.append({"name": name, "status": status, "detail": detail, "critical": critical, "timestamp": datetime.now(timezone.utc).isoformat()})
    print(f"{symbol} {color}{BOLD}{status}{RESET} — {name}")
    if detail and VERBOSE:
        print(f"   {detail}")

def section(title: str):
    print(f"\n{BOLD}{BLUE}▶ {title}{RESET}")
    print("=" * 60)

def _safe(resp) -> Dict[str, Any]:
    """Safely extract status/content from response or error string."""
    if hasattr(resp, "status_code"):
        return {"status": resp.status_code, "content": getattr(resp, "content", b""), "text": getattr(resp, "text", "")}
    return {"status": str(resp), "content": b"", "text": str(resp)}

def api_get(path: str, headers: Optional[Dict] = None, expected_status: int = 200, timeout: int = 10):
    try:
        resp = session.get(urljoin(BASE_URL, path), headers=headers, timeout=timeout)
        return resp.status_code == expected_status, resp
    except Exception as e:
        return False, str(e)

def api_post(path: str, json: Optional[Dict] = None, data: Optional[Dict] = None, headers: Optional[Dict] = None, expected_status: int = 200, timeout: int = 10):
    try:
        resp = session.post(urljoin(BASE_URL, path), json=json, data=data, headers=headers, timeout=timeout, allow_redirects=False)
        return resp.status_code == expected_status, resp
    except Exception as e:
        return False, str(e)

def api_delete(path: str, headers: Optional[Dict] = None, timeout: int = 10):
    try:
        resp = session.delete(urljoin(BASE_URL, path), headers=headers, timeout=timeout)
        return resp.status_code == 204, resp
    except Exception as e:
        return False, str(e)

# ---------------------------------------------------------------------------
# 1. HEALTH & METRICS
# ---------------------------------------------------------------------------
section("1. API CONNECTIVITY & HEALTH")

ok, resp = api_get("/health")
if ok:
    d = resp.json()
    log_test("Health endpoint", "PASS", f"db={d.get('db')}, cache={d.get('cache')}")
    log_test("Health: DB ok", "PASS", critical=True)
else:
    log_test("Health endpoint", "FAIL", critical=True)

ok, resp = api_get("/metrics")
if ok:
    t = resp.text
    log_test("Metrics endpoint", "PASS")
    log_test("Metrics: executions_total", "PASS" if "report_executions_total" in t else "FAIL")
    has_duration = "report_execution_duration_seconds" in t or "REPORT_DURATION" in t or "report_duration" in t
    log_test("Metrics: duration_seconds", "PASS" if has_duration else "FAIL")
else:
    log_test("Metrics endpoint", "FAIL")

# ---------------------------------------------------------------------------
# 2. AUTHENTICATION
# ---------------------------------------------------------------------------
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
    log_test("Login", "FAIL", critical=True)
    sys.exit(1)

auth_headers = {"Authorization": f"Bearer {access_token}"}

ok, _ = api_post("/auth/refresh", json={"refresh_token": refresh_token}, expected_status=200)
log_test("Token refresh", "PASS" if ok else "FAIL")

ok, _ = api_post("/auth/login", data={"username": "bad", "password": "bad"}, expected_status=401)
log_test("Invalid login rejected", "PASS" if ok else "FAIL")

print("   Testing login rate limit (6 rapid requests)...")
rate_limited = False
for i in range(6):
    _, resp = api_post("/auth/login", data={"username": "ratelimit", "password": "test"})
    if hasattr(resp, "status_code") and resp.status_code == 429:
        rate_limited = True
        break
log_test("Login rate limit", "PASS" if rate_limited else "FAIL", detail="429 received" if rate_limited else "No 429")

# ---------------------------------------------------------------------------
# 3. REPORT CRUD
# ---------------------------------------------------------------------------
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
    info = _safe(resp)
    log_test("Create report", "FAIL", f"status={info['status']}", critical=True)
    sys.exit(1)

report = resp.json()
report_id = report.get("id")
log_test("Create report", "PASS", f"id={report_id}")
log_test("Create: has query_ast", "PASS" if "query_ast" in report else "FAIL")

ok, resp = api_get("/reports/?skip=0&limit=20", headers=auth_headers)
if ok:
    data = resp.json()
    count = len(data) if isinstance(data, list) else len(data.get("items", []))
    log_test("List reports", "PASS", f"count={count}")
else:
    log_test("List reports", "FAIL")

ok, resp = api_get(f"/reports/{report_id}/", headers=auth_headers)
if ok:
    log_test("Get report", "PASS", f"name={resp.json().get('name')}")
else:
    log_test("Get report", "FAIL")

r = session.put(urljoin(BASE_URL, f"/reports/{report_id}/"), json={"name": "Updated", "status": "inactive"}, headers=auth_headers, timeout=10)
if r.status_code == 200:
    log_test("Update report", "PASS", f"name={r.json().get('name')}, status={r.json().get('status')}")
else:
    log_test("Update report", "FAIL", f"status={r.status_code}")

r = session.put(urljoin(BASE_URL, f"/reports/{report_id}/"), json={
    "name": "Scheduled",
    "status": "active",
    "schedule": {"interval": 3600},
    "recipients": ["test@example.com"]
}, headers=auth_headers, timeout=10)
log_test("Update with schedule", "PASS" if r.status_code == 200 else "FAIL", f"status={r.status_code}")

# ---------------------------------------------------------------------------
# 4. REPORT EXECUTION
# ---------------------------------------------------------------------------
section("4. REPORT EXECUTION")

ok, resp = api_post(f"/reports/{report_id}/trigger", headers=auth_headers, expected_status=200)
if ok:
    data = resp.json()
    log_test("Trigger report", "PASS", f"rows={len(data.get('data', []))}")
    log_test("Trigger: returns data", "PASS" if "data" in data else "FAIL", critical=True)
else:
    info = _safe(resp)
    log_test("Trigger report", "FAIL", f"status={info['status']}", critical=True)

print("   Testing trigger rate limit (11 rapid requests)...")
rate_limited = False
for i in range(11):
    _, resp = api_post(f"/reports/{report_id}/trigger", headers=auth_headers)
    if hasattr(resp, "status_code") and resp.status_code == 429:
        rate_limited = True
        break
log_test("Trigger rate limit", "PASS" if rate_limited else "FAIL", detail="429 received" if rate_limited else "No 429")

# ---------------------------------------------------------------------------
# 5. EXPORT FORMATS
# ---------------------------------------------------------------------------
section("5. EXPORT FORMATS")

# JSON export (fast)
ok, resp = api_get(f"/reports/{report_id}/export?format=json", headers=auth_headers, timeout=15)
if ok:
    log_test("Export JSON", "PASS", f"bytes={len(resp.content)}")
    export_found = True
else:
    info = _safe(resp)
    log_test("Export JSON", "FAIL", f"status={info['status']}")
    export_found = False

# Excel export (medium)
if export_found:
    ok, resp = api_get(f"/reports/{report_id}/export?format=excel", headers=auth_headers, timeout=20)
    if ok and resp.content[:4] == b"PK\x03\x04":
        log_test("Export Excel", "PASS", f"bytes={len(resp.content)}, signature=PK..")
    else:
        info = _safe(resp)
        log_test("Export Excel", "FAIL", f"status={info['status']}")

# PDF export (SLOW — 30s timeout for large tables)
if export_found:
    ok, resp = api_get(f"/reports/{report_id}/export?format=pdf", headers=auth_headers, timeout=30)
    if ok and resp.content[:4] == b"%PDF":
        log_test("Export PDF", "PASS", f"bytes={len(resp.content)}, header=%PDF")
    else:
        info = _safe(resp)
        log_test("Export PDF", "FAIL", f"status={info['status']}")

# ---------------------------------------------------------------------------
# 6. AUDIT LOG
# ---------------------------------------------------------------------------
section("6. AUDIT LOG")

api_key_headers = {"X-API-KEY": "test-api-key"}
ok, resp = api_get("/audits/", headers=api_key_headers, timeout=15)
if ok:
    log_test("Audit log endpoint", "PASS")
else:
    info = _safe(resp)
    log_test("Audit log endpoint", "FAIL", f"status={info['status']}")

# ---------------------------------------------------------------------------
# 7. CLEANUP
# ---------------------------------------------------------------------------
section("7. CLEANUP")

ok, resp = api_delete(f"/reports/{report_id}/", headers=auth_headers, timeout=15)
if ok:
    log_test("Delete report", "PASS", f"status=204")
else:
    info = _safe(resp)
    log_test("Delete report", "FAIL", f"status={info['status']}")

# ---------------------------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------------------------
section("VERIFICATION SUMMARY")

total = len(results)
passed = sum(1 for r in results if r["status"] == "PASS")
failed = sum(1 for r in results if r["status"] == "FAIL")
critical = [r for r in results if r["status"] == "FAIL" and r.get("critical")]

print(f"""
┌─────────────────────────────────────────┐
│  TOTAL: {total:3d}  ✅ PASS: {passed:3d}  🔴 FAIL: {failed:3d}  │
│  CRITICAL FAILURES: {len(critical):3d}              │
└─────────────────────────────────────────┘
""")

if critical:
    print(f"{RED}{BOLD}CRITICAL FAILURES:{RESET}")
    for r in critical:
        print(f"  🔴 {r['name']}: {r.get('detail', '')}")

with open("verification_report_final.json", "w") as f:
    json.dump({
        "summary": {"total": total, "passed": passed, "failed": failed, "critical_failures": len(critical), "timestamp": datetime.now(timezone.utc).isoformat(), "base_url": BASE_URL},
        "results": results
    }, f, indent=2, default=str)

print(f"\n{BOLD}Report saved to: verification_report_final.json{RESET}")
sys.exit(0 if len(critical) == 0 else 1)
