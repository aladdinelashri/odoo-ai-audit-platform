#!/usr/bin/env python3
"""
Tenant Onboarding — Accounting Module
Discovers schema, creates tables, and syncs data for a new client.
Run once per tenant to enable accounting audits.
"""
import sys
import os
import sqlite3

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
from database.core.odoo.connector import OdooConnector
from database.core.storage.sqlite.database import SQLiteDatabase
from database.core.discovery import OdooModelDiscovery, DynamicSyncService
from config.settings import Settings


def onboard_accounting():
    """Discover accounting models, build SQLite tables, and sync data."""
    load_dotenv()

    # 1. Connect to Odoo
    print("🔗 Connecting to Odoo...")
    odoo = OdooConnector()
    print(f"   ✅ Connected: {odoo}")

    # 2. Init SQLite
    db = SQLiteDatabase()

    # 3. Init discovery & sync services
    discovery = OdooModelDiscovery(odoo)
    sync = DynamicSyncService(odoo, db)

    # 4. Required models for Phase 3 (Accounting Audits)
    required_models = [
        "account.account",
        "account.move",
        "account.move.line",
        "account.journal",
        "account.tax",
    ]

    print("\n" + "=" * 60)
    print("  ACCOUNTING TENANT ONBOARDING")
    print("=" * 60)

    for model in required_models:
        print(f"\n🔍 Discovering {model}...")
        try:
            schema = discovery.get_model_schema(model)
            print(f"   📋 Fields: {len(schema['fields'])} | Table: {schema['table']}")
        except Exception as e:
            print(f"   ⚠️  Discovery failed: {e}")
            continue

        print(f"🔄 Syncing {model}...")
        try:
            count = sync.sync(model, clear=True)
            print(f"   ✅ Synced {count:,} records")
        except Exception as e:
            print(f"   ❌ Sync failed: {e}")

    # 5. Verify using raw sqlite3 (bypasses wrapper method name issues)
    print("\n" + "=" * 60)
    print("  VERIFICATION")
    print("=" * 60)

    conn = sqlite3.connect(Settings.SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'account_%'")
    tables = cur.fetchall()

    print(f"   Accounting tables created: {len(tables)}")
    for t in tables:
        name = t["name"]
        cur.execute(f"SELECT COUNT(*) as c FROM {name}")
        count = cur.fetchone()["c"]
        print(f"   • {name}: {count:,} rows")

    conn.close()

    print("\n" + "=" * 60)
    print("  🏁 ONBOARDING COMPLETE")
    print("=" * 60)
    print("\nYou can now run:")
    print("   python cli/audit.py list")
    print("   python cli/audit.py audit journal_audit")
    print("   python cli/audit.py audit tax_validation")
    print("   python cli/audit.py audit ledger_integrity")
    print("   python cli/audit.py run-all")
    print("=" * 60)


if __name__ == "__main__":
    onboard_accounting()
