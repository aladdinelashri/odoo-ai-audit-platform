#!/usr/bin/env python3
"""
Performance Optimization Setup Script.
Applies indexes, WAL mode, and connection pool config.
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.core.storage.sqlite.index_manager import setup_critical_indexes
from database.core.storage.sqlite.sqlite_pool import SQLitePool


def main():
    parser = argparse.ArgumentParser(description="Setup performance optimizations")
    parser.add_argument("--db", default="database/storage/audit.db", help="Database path")
    parser.add_argument("--all", action="store_true", help="Create all recommended indexes")
    parser.add_argument("--critical-only", action="store_true", help="Create only critical indexes")
    parser.add_argument("--analyze", action="store_true", help="Run ANALYZE on all tables")
    args = parser.parse_args()
    
    print("=" * 60)
    print("PERFORMANCE OPTIMIZATION SETUP")
    print("=" * 60)
    
    # Initialize pool
    print("\n[1/3] Initializing SQLite Connection Pool with WAL mode...")
    SQLitePool.initialize(args.db)
    conn = SQLitePool.get_connection()
    
    cursor = conn.execute("PRAGMA journal_mode")
    print(f"      Journal mode: {cursor.fetchone()[0]}")
    
    cursor = conn.execute("PRAGMA synchronous")
    print(f"      Synchronous: {cursor.fetchone()[0]}")
    
    # Create indexes
    print("\n[2/3] Creating indexes...")
    if args.all:
        from database.core.storage.sqlite.index_manager import setup_performance_indexes
        results = setup_performance_indexes(args.db)
        created = sum(1 for v in results.values() if v)
        print(f"      Created: {created} indexes")
    elif args.critical_only:
        results = setup_critical_indexes(args.db)
        created = sum(1 for v in results.values() if v)
        print(f"      Created: {created} critical indexes")
    else:
        print("      Use --all or --critical-only to create indexes")
    
    # Analyze tables
    if args.analyze:
        print("\n[3/3] Analyzing tables...")
        tables = ["account_moves", "account_move_lines", "account_accounts",
                  "account_taxs", "account_journals"]
        for table in tables:
            try:
                SQLitePool.execute(f"ANALYZE {table}")
                print(f"      OK: {table}")
            except Exception as e:
                print(f"      SKIP: {table}: {e}")
    
    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
