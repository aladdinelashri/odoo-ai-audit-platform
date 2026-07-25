#!/usr/bin/env python3
"""
Odoo AI Audit Platform — Thin CLI Entry Point
Delegates all logic to AuditRunner.
"""

import sys
import argparse
import json
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
    
    # ─── Audit ───
    audit_p = subparsers.add_parser('audit', help='Run an audit')
    audit_p.add_argument('name', help='Audit name (e.g., missing_receipts)')
    audit_p.add_argument('--session-id', type=int)
    audit_p.add_argument('--business-unit-id', type=int)
    audit_p.add_argument('--date-from', help='YYYY-MM-DD')
    audit_p.add_argument('--date-to', help='YYYY-MM-DD')
    audit_p.add_argument('--json', action='store_true', help='JSON output')
    
    # ─── Run All ───
    all_p = subparsers.add_parser('run-all', help='Run all POS audits')
    all_p.add_argument('--json', action='store_true')
    
    # ─── List ───
    list_p = subparsers.add_parser('list', help='List available audits')
    
    # ─── Status ───
    status_p = subparsers.add_parser('status', help='Show system status')
    
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
        print("\n" + "="*60)
        print("  Available Audits")
        print("="*60)
        for name, desc in audits.items():
            print(f"  {name:20s} — {desc}")
        print("="*60 + "\n")
    
    elif args.command == 'audit':
        result = runner.run(
            args.name,
            session_id=args.session_id,
            business_unit_id=args.business_unit_id,
            date_from=args.date_from,
            date_to=args.date_to
        )
        _print(result, args.json)
    
    elif args.command == 'run-all':
        result = runner.run_all(
            session_id=args.session_id,
            business_unit_id=args.business_unit_id,
            date_from=args.date_from,
            date_to=args.date_to
        )
        _print(result, args.json)
    
    elif args.command == 'status':
        _status()


def _print(result, as_json):
    if as_json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print("\n" + "="*60)
        print(f"  Status: {result.get('status', 'unknown')}")
        print("="*60)
        print(json.dumps(result, indent=2, default=str))
        print("="*60 + "\n")


def _status():
    from database.core.storage.sqlite.sqlite_service import SQLiteService
    sqlite = SQLiteService()
    
    print("\n" + "="*60)
    print("  Odoo AI Audit Platform — Status")
    print("="*60)
    print(f"  Odoo URL:     {Settings.ODOO_URL}")
    print(f"  Database:     {Settings.SQLITE_PATH}")
    print(f"  Log Level:    {Settings.LOG_LEVEL}")
    print()
    
    tables = ['pos_orders', 'pos_payments', 'pos_sessions', 'business_units']
    for t in tables:
        try:
            count = sqlite.count(t)
            print(f"  {t:25s}: {count:>8,} rows")
        except Exception as e:
            print(f"  {t:25s}: Error ({e})")
    
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
