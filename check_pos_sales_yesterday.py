#!/usr/bin/env python
"""
Check POS Sales for Yesterday
Runs a query against the local SQLite database to get yesterday's sales summary.
"""

import sys
from pathlib import Path

# Add project root to path so we can import modules
sys.path.insert(0, str(Path(__file__).parent))

from database.core.storage.sqlite.sqlite_pool import SQLitePool


def get_yesterday_sales():
    """
    Retrieve POS sales summary for yesterday.
    """
    # Initialize the pool (uses default db path from config)
    SQLitePool.initialize()

    query = """
        SELECT
            DATE(date_order) as sale_date,
            COUNT(*) as order_count,
            SUM(amount_total) as total_sales,
            AVG(amount_total) as avg_order_value,
            SUM(CASE WHEN amount_total < 0 THEN amount_total ELSE 0 END) as refunds_total,
            COUNT(CASE WHEN amount_total < 0 THEN 1 END) as refund_count
        FROM pos_orders
        WHERE DATE(date_order) = DATE('now', '-1 day')
            AND state IN ('done', 'paid')
        GROUP BY DATE(date_order)
        ORDER BY sale_date DESC;
    """

    result = SQLitePool.execute(query)

    if result:
        row = result[0]
        print("=" * 60)
        print("📊 POS Sales Summary for Yesterday")
        print("=" * 60)
        print(f"📅 Date:                 {row['sale_date']}")
        print(f"🧾 Total Orders:         {row['order_count']}")
        print(f"💰 Total Sales:          ${row['total_sales']:,.2f}")
        print(f"📊 Avg Order Value:      ${row['avg_order_value']:,.2f}")
        print(f"🔄 Refunds Total:        ${row['refunds_total']:,.2f}")
        print(f"🔢 Refund Count:         {row['refund_count']}")
        print("=" * 60)

        net_sales = (row['total_sales'] or 0) - (row['refunds_total'] or 0)
        print(f"📈 Net Sales:            ${net_sales:,.2f}")
        print("=" * 60)

        return row
    else:
        print("❌ No sales found for yesterday.")
        return None


def get_detailed_yesterday_sales():
    """
    Get detailed breakdown by branch and cashier.
    """
    query = """
        SELECT
            DATE(o.date_order) as sale_date,
            COALESCE(bu.name, 'Unknown') as business_unit,
            COALESCE(u.name, 'Unknown') as cashier,
            COUNT(*) as order_count,
            SUM(o.amount_total) as total_sales,
            AVG(o.amount_total) as avg_order_value
        FROM pos_orders o
        LEFT JOIN pos_session s ON o.session_id = s.id
        LEFT JOIN res_users u ON s.user_id = u.id
        LEFT JOIN business_unit bu ON o.business_unit_id = bu.id
        WHERE DATE(o.date_order) = DATE('now', '-1 day')
            AND o.state IN ('done', 'paid')
        GROUP BY sale_date, bu.name, u.name
        ORDER BY total_sales DESC;
    """

    result = SQLitePool.execute(query)

    if result:
        print("\n" + "=" * 80)
        print("📊 Detailed POS Sales by Branch & Cashier - Yesterday")
        print("=" * 80)
        print(f"{'Branch':<20} {'Cashier':<20} {'Orders':<10} {'Total Sales':<15} {'Avg Order':<12}")
        print("-" * 80)

        for row in result:
            print(f"{row['business_unit'][:20]:<20} "
                  f"{row['cashier'][:20]:<20} "
                  f"{row['order_count']:<10} "
                  f"${row['total_sales']:>12,.2f}  "
                  f"${row['avg_order_value']:>10,.2f}")

        print("=" * 80)
        return result
    else:
        print("❌ No detailed sales found for yesterday.")
        return None


if __name__ == "__main__":
    print("\n🚀 Running POS Sales Report...\n")

    # Basic summary
    get_yesterday_sales()

    # Detailed breakdown
    get_detailed_yesterday_sales()
