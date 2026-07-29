"""
Odoo AI Audit Platform — Thin CLI Entry Point
Delegates all logic to AuditRunner.
"""

import sys
import argparse
import json
import os
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.logging import setup_logging
from config.settings import Settings
from database.core.audits.runner.audit_runner import AuditRunner


def main():
    parser = argparse.ArgumentParser(
        prog='odoo-audit',
        description='Odoo AI Audit Platform CLI'
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Audit
    audit_p = subparsers.add_parser('audit', help='Run an audit')
    audit_p.add_argument('name', help='Audit name (e.g., missing_receipts)')
    audit_p.add_argument('--session-id', type=int)
    audit_p.add_argument('--business-unit-id', type=int)
    audit_p.add_argument('--date-from', help='YYYY-MM-DD')
    audit_p.add_argument('--date-to', help='YYYY-MM-DD')
    audit_p.add_argument('--json', action='store_true', help='JSON output')

    # Run All
    all_p = subparsers.add_parser('run-all', help='Run all POS audits')
    all_p.add_argument('--session-id', type=int)
    all_p.add_argument('--business-unit-id', type=int)
    all_p.add_argument('--date-from', help='YYYY-MM-DD')
    all_p.add_argument('--date-to', help='YYYY-MM-DD')
    all_p.add_argument('--json', action='store_true')

    # List
    list_p = subparsers.add_parser('list', help='List available audits')

    # Status
    status_p = subparsers.add_parser('status', help='Show system status')

    # Sync (Delta / Full)
    sync_p = subparsers.add_parser('sync', help='Sync Odoo data to SQLite')
    sync_p.add_argument('model', nargs='?', help='Model name (e.g., account.move). If omitted, syncs all accounting models.')
    sync_p.add_argument('--delta', action='store_true', help='Delta sync: only records changed since last sync')
    sync_p.add_argument('--full', action='store_true', help='Force full sync (delete all and re-insert)')
    sync_p.add_argument('--list-meta', action='store_true', help='Show sync metadata table (_sync_meta)')
    sync_p.add_argument('--json', action='store_true', help='JSON output')
    sync_p.add_argument('--odoo-url', help='Odoo server URL')
    sync_p.add_argument('--odoo-db', help='Odoo database name')
    sync_p.add_argument('--odoo-username', help='Odoo username')
    sync_p.add_argument('--odoo-password', help='Odoo password')

    # Global
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()

    # Logging
    level = 'DEBUG' if args.debug else ('INFO' if args.verbose else 'WARNING')
    setup_logging(level=level, console=True)

    if not args.command:
        parser.print_help()
        return

    runner = AuditRunner()

    if args.command == 'list':
        audits = runner.list_available()
        print("\n" + "=" * 60)
        print("  Available Audits")
        print("=" * 60)
        for name, desc in audits.items():
            print("  {:20s} — {}".format(name, desc))
        print("=" * 60 + "\n")

    elif args.command == 'audit':
        result = runner.run(
            args.name,
            session_id=getattr(args, 'session_id', None),
            business_unit_id=getattr(args, 'business_unit_id', None),
            date_from=getattr(args, 'date_from', None),
            date_to=getattr(args, 'date_to', None)
        )
        _print(result, args.json)

    elif args.command == 'run-all':
        result = runner.run_all(
            session_id=getattr(args, 'session_id', None),
            business_unit_id=getattr(args, 'business_unit_id', None),
            date_from=getattr(args, 'date_from', None),
            date_to=getattr(args, 'date_to', None)
        )
        _print(result, args.json)

    elif args.command == 'status':
        _status()

    elif args.command == 'sync':
        _handle_sync(args)


def _print(result, as_json):
    if as_json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print("\n" + "=" * 60)
        status = result.get('status', 'unknown')
        print("  Status: " + str(status))
        print("=" * 60)
        print(json.dumps(result, indent=2, default=str))
        print("=" * 60 + "\n")


def _status():
    from database.core.storage.sqlite.sqlite_service import SQLiteService
    sqlite = SQLiteService()

    print("\n" + "=" * 60)
    print("  Odoo AI Audit Platform — Status")
    print("=" * 60)
    print("  Odoo URL:     " + str(Settings.ODOO_URL))
    db_path = getattr(Settings, 'SQLITE_PATH', 'N/A')
    print("  Database:     " + str(db_path))
    log_level = getattr(Settings, 'LOG_LEVEL', 'N/A')
    print("  Log Level:    " + str(log_level))
    print()

    tables = ['pos_orders', 'pos_payments', 'pos_sessions', 'business_units',
              'account_moves', 'account_move_lines', 'account_accounts',
              'account_journals', 'account_taxs', '_sync_meta']
    for t in tables:
        try:
            count = sqlite.count(t)
            print("  {:25s}: {:>8,} rows".format(t, count))
        except Exception as e:
            print("  {:25s}: Error ({})".format(t, e))

    print("=" * 60 + "\n")


def _resolve_setting(name, aliases=None, cli_value=None):
    if cli_value is not None:
        return cli_value
    val = getattr(Settings, name, None)
    if val is not None:
        return val
    if aliases:
        for alias in aliases:
            val = getattr(Settings, alias, None)
            if val is not None:
                return val
    val = os.getenv(name)
    if val is not None:
        return val
    if aliases:
        for alias in aliases:
            val = os.getenv(alias)
            if val is not None:
                return val
    return None


def _handle_sync(args):
    from database.core.odoo.connector import OdooConnector
    from database.core.discovery.dynamic_sync import DynamicSyncService
    from database.core.storage.sqlite.database import SQLiteDatabase

    odoo_url = _resolve_setting('ODOO_URL', cli_value=getattr(args, 'odoo_url', None))
    odoo_db = _resolve_setting('ODOO_DB', cli_value=getattr(args, 'odoo_db', None))
    odoo_user = _resolve_setting('ODOO_USER', aliases=['ODOO_USERNAME'], cli_value=getattr(args, 'odoo_username', None))
    odoo_pass = _resolve_setting('ODOO_PASSWORD', aliases=['ODOO_PASS'], cli_value=getattr(args, 'odoo_password', None))
    sqlite_path = _resolve_setting('SQLITE_PATH', cli_value=None) or 'database/storage/audit.db'

    missing = []
    if not odoo_url:
        missing.append('ODOO_URL')
    if not odoo_db:
        missing.append('ODOO_DB')
    if not odoo_user:
        missing.append('ODOO_USERNAME (or ODOO_USER)')
    if not odoo_pass:
        missing.append('ODOO_PASSWORD')

    if missing:
        print("\n" + "!" * 60)
        print("  ERROR: Missing required Odoo connection settings!")
        print("  Missing:")
        for m in missing:
            print("    • " + m)
        print("\n  Quick fix — add to your .env file:")
        print("    ODOO_URL=https://production.misralgadeda.site")
        print("    ODOO_DB=production")
        print("    ODOO_USERNAME=aitechpro29@gmail.com")
        print("    ODOO_PASSWORD=your_password")
        print("\n  Or run with inline args:")
        print("    python cli/audit.py sync --odoo-url ... --odoo-username ...")
        print("!" * 60 + "\n")
        return

    db = SQLiteDatabase(sqlite_path)
    odoo = OdooConnector(
        url=odoo_url,
        db=odoo_db,
        username=odoo_user,
        password=odoo_pass
    )
    syncer = DynamicSyncService(odoo, db)

    if args.list_meta:
        try:
            rows = db.query("SELECT * FROM _sync_meta ORDER BY updated_at DESC")
        except Exception as e:
            print("\n⚠️  _sync_meta not found: " + str(e))
            print("   Run a full sync first to create it.\n")
            return

        print("\n" + "=" * 75)
        print("  Sync Metadata (_sync_meta)")
        print("=" * 75)
        print("  {:<30} {:<22} {:<7} {:<8} {:<10}".format("Model", "Last Sync", "Type", "Count", "Duration"))
        print("-" * 75)
        for r in rows:
            # Handle both dict rows and tuple rows
            if isinstance(r, dict):
                model = r.get('model', '')
                last_sync = r.get('last_sync', '')
                sync_type = r.get('sync_type', '')
                record_count = r.get('record_count', 0) or 0
                sync_duration = r.get('sync_duration', 0.0) or 0.0
            else:
                model = r[0] if len(r) > 0 else ''
                last_sync = r[1] if len(r) > 1 else ''
                record_count = r[2] if len(r) > 2 else 0
                sync_type = r[4] if len(r) > 4 else ''
                sync_duration = r[3] if len(r) > 3 else 0.0

            print("  {:<30} {:<22} {:<7} {:<8} {:<10.2f}".format(
                str(model), str(last_sync), str(sync_type), int(record_count), float(sync_duration)
            ))
        print("=" * 75 + "\n")
        return

    if args.model:
        models = [args.model]
    else:
        models = [
            "account.account",
            "account.move",
            "account.move.line",
            "account.journal",
            "account.tax",
        ]

    force_full = args.full or (not args.delta)

    results = []
    print("\n" + "=" * 60)
    mode_str = "FULL" if force_full else "DELTA"
    print("  Sync Mode: " + mode_str)
    print("=" * 60)

    for model in models:
        print("\n📦 Syncing: " + model)
        try:
            if force_full:
                result = syncer.sync(model, clear=True)
                syncer._update_sync_meta(model, result, sync_type='full')
                duration = result.get('duration', 0)
                print("   ✅ {} records | {:.2f}s | FULL".format(result['records_synced'], duration))
            else:
                result = syncer.sync_delta(model)
                total_dur = result.get('total_duration', 0)
                print("   ✅ {} records | {:.2f}s | DELTA".format(result['records_synced'], total_dur))
                last_sync = result.get('last_sync', 'N/A')
                new_sync = result.get('new_last_sync', 'N/A')
                print("      Last sync was: " + str(last_sync))
                print("      New sync time: " + str(new_sync))
            results.append(result)
        except Exception as e:
            print("   ❌ Error: " + str(e))
            results.append({"model": model, "error": str(e)})

    print("\n" + "=" * 60)
    print("  Sync Summary")
    print("=" * 60)
    total = sum(r.get("records_synced", 0) for r in results if "error" not in r)
    errors = sum(1 for r in results if "error" in r)
    print("  Total records synced : " + str(total))
    print("  Models with errors   : " + str(errors))
    mode_label = "FULL" if force_full else "DELTA"
    print("  Mode                 : " + mode_label)
    print("=" * 60)
    print("\n💡 Tip: Next time use --delta for faster incremental sync.\n")

    if args.json:
        print(json.dumps(results, indent=2, default=str))


if __name__ == '__main__':
    main()
