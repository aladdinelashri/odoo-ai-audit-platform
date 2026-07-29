"""
Dynamic Sync Service — Sync any Odoo model into SQLite dynamically.
Supports: Full Sync, Delta Sync, and sync metadata tracking.
"""

import time
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List


class DynamicSyncService:
    def __init__(self, odoo_connector, db):
        self.odoo = odoo_connector
        self.db = db
        self._table_schemas = {}
        self._ensure_sync_meta_table()

    # ==========================================================
    #  PUBLIC API
    # ==========================================================

    def sync(self, model_name, domain=None, clear=True, fields=None, batch_size=5000):
        """
        Sync any Odoo model into SQLite.
        clear=True  → DELETE then INSERT (Full Sync)
        clear=False → INSERT OR REPLACE (Delta Sync)
        """
        start_time = time.perf_counter()
        table_name = self._model_to_table(model_name)

        # 1. Discover fields from Odoo (exclude problematic types)
        odoo_fields = fields or self._discover_fields(model_name)

        # 2. Ensure SQLite table exists
        self._ensure_table(table_name, odoo_fields)

        # 3. Fetch from Odoo in batches (with XML-RPC error fallback)
        records = self._fetch_batch(model_name, domain or [], odoo_fields, batch_size)

        # 4. Clear if full sync
        if clear:
            self.db.execute("DELETE FROM " + table_name)

        # 5. Insert
        inserted = self._insert_records(table_name, records)

        duration = time.perf_counter() - start_time

        return {
            "model": model_name,
            "table": table_name,
            "records_synced": inserted,
            "duration": duration,
            "clear": clear,
        }

    def sync_delta(self, model_name, last_sync=None, fields=None, batch_size=2000):
        """
        Sync only records modified since last_sync.
        If no previous sync exists → falls back to Full Sync.
        """
        start_time = time.perf_counter()

        if last_sync is None:
            last_sync = self._get_last_sync(model_name)

        if last_sync is None:
            print("🆕 No previous sync for " + model_name + ". Running FULL sync...")
            result = self.sync(model_name, clear=True, fields=fields, batch_size=batch_size)
            self._update_sync_meta(model_name, result, sync_type='full')
            return result

        domain = [("write_date", ">", last_sync)]
        result = self.sync(model_name, domain=domain, clear=False, fields=fields, batch_size=batch_size)

        new_last_sync = self._get_max_write_date(model_name)
        if not new_last_sync:
            new_last_sync = datetime.now(timezone.utc).isoformat()

        self._update_sync_meta(model_name, result, sync_type='delta', last_sync_override=new_last_sync)

        result["last_sync"] = last_sync
        result["new_last_sync"] = new_last_sync
        result["sync_type"] = "delta"
        result["total_duration"] = time.perf_counter() - start_time

        return result

    # ==========================================================
    #  SYNC METADATA (_sync_meta)
    # ==========================================================

    def _ensure_sync_meta_table(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS _sync_meta (
                model TEXT PRIMARY KEY,
                last_sync TEXT NOT NULL,
                record_count INTEGER DEFAULT 0,
                sync_duration REAL DEFAULT 0.0,
                sync_type TEXT DEFAULT 'full',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        try:
            self.db.execute("CREATE INDEX IF NOT EXISTS idx_sync_meta_model ON _sync_meta(model)")
        except Exception:
            pass

    def _get_last_sync(self, model_name):
        """Read last sync timestamp from _sync_meta."""
        try:
            row = self.db.query_one(
                "SELECT last_sync FROM _sync_meta WHERE model = ?",
                (model_name,)
            )
            if row is None:
                return None
            if isinstance(row, dict):
                return row.get('last_sync')
            if isinstance(row, (list, tuple)):
                return row[0] if len(row) > 0 else None
            return None
        except Exception:
            return None

    def _update_sync_meta(self, model_name, sync_result, sync_type='full', last_sync_override=None):
        now = datetime.now(timezone.utc).isoformat()
        last_sync = last_sync_override or now

        self.db.execute("""
            INSERT INTO _sync_meta (model, last_sync, record_count, sync_duration, sync_type, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(model) DO UPDATE SET
                last_sync = excluded.last_sync,
                record_count = excluded.record_count,
                sync_duration = excluded.sync_duration,
                sync_type = excluded.sync_type,
                updated_at = excluded.updated_at
        """, (
            model_name,
            last_sync,
            sync_result.get("records_synced", 0),
            sync_result.get("duration", 0.0),
            sync_type,
            now
        ))

    def _get_max_write_date(self, model_name):
        """Get the latest write_date from the synced table."""
        table = self._model_to_table(model_name)
        try:
            row = self.db.query_one("SELECT MAX(write_date) FROM " + table)
            if row is None:
                return None
            if isinstance(row, dict):
                val = row.get('MAX(write_date)')
                if val is None:
                    keys = [k for k in row.keys() if 'max' in str(k).lower()]
                    if keys:
                        val = row.get(keys[0])
                return val
            if isinstance(row, (list, tuple)):
                return row[0] if len(row) > 0 else None
            return None
        except Exception:
            return None

    # ==========================================================
    #  INTERNAL HELPERS
    # ==========================================================

    def _model_to_table(self, model_name):
        return model_name.replace(".", "_") + "s"

    def _discover_fields(self, model_name):
        """
        Discover fields from Odoo ir.model.fields.
        EXCLUDE problematic types and known trouble fields.
        """
        try:
            fields_info = self.odoo.search_read(
                'ir.model.fields',
                [('model', '=', model_name)],
                ['name', 'ttype', 'store', 'related', 'compute']
            )

            excluded_types = {
                'binary', 'one2many', 'many2many', 'reference',
                'json', 'properties', 'html', 'image'
            }

            excluded_names = {
                'tax_totals', 'amount_by_group', 'amount_total_in_currency_signed',
                'invoice_line_ids', 'line_ids', 'edi_document_ids',
                'message_ids', 'message_attachment_count', 'activity_ids',
                'attachment_ids', 'access_token', 'access_url',
                'display_name', '__last_update', 'portal_url',
                'needed_terms', 'payment_term_details', 'show_payment_term_details',
            }

            names = []
            for f in fields_info:
                fname = f.get('name', '')
                ttype = f.get('ttype', '')

                if not fname or fname in excluded_names:
                    continue
                if ttype in excluded_types:
                    continue

                is_computed = bool(f.get('compute') or f.get('related'))
                if is_computed and fname not in ['id', 'name', 'create_date', 'write_date', 'state']:
                    continue

                names.append(fname)

            for critical in ['id', 'create_date', 'write_date']:
                if critical not in names:
                    names.insert(0, critical)

            return names
        except Exception as e:
            print("      ⚠️  Field discovery failed: " + str(e) + ", using defaults")
            return ['id', 'name', 'create_date', 'write_date']

    def _fetch_batch(self, model_name, domain, fields, batch_size=2000):
        """
        Fetch records from Odoo in batches.
        If XML-RPC serialization fails, fallback to safe fields.
        """
        try:
            return self._fetch_batch_raw(model_name, domain, fields, batch_size)
        except Exception as e:
            err = str(e)
            if 'dictionary key must be string' in err or 'cannot marshal None' in err:
                print("      ⚠️  XML-RPC error with discovered fields, trying safe fields...")
                safe_fields = self._safe_fields_for_model(model_name)
                return self._fetch_batch_raw(model_name, domain, safe_fields, batch_size)
            raise

    def _fetch_batch_raw(self, model_name, domain, fields, batch_size=2000):
        """Raw batch fetcher."""
        all_records = []
        offset = 0

        while True:
            batch = self.odoo.search_read(
                model_name,
                domain,
                fields,
                limit=batch_size,
                offset=offset
            )
            if not batch:
                break

            cleaned = [self._clean_record(r, fields) for r in batch]
            all_records.extend(cleaned)

            if len(batch) < batch_size:
                break
            offset += batch_size
            print("      ... fetched " + str(len(all_records)) + " so far")

        return all_records

    def _safe_fields_for_model(self, model_name):
        """Return a minimal safe field list per model to avoid XML-RPC errors."""
        base = ['id', 'name', 'create_date', 'write_date', 'state']

        mapping = {
            'account.move': ['journal_id', 'partner_id', 'amount_total',
                             'state', 'date', 'move_type', 'name', 'ref',
                             'posted_before', 'is_storno'],
            'account.move.line': ['move_id', 'account_id', 'partner_id',
                                  'debit', 'credit', 'balance', 'amount_currency',
                                  'name', 'date', 'journal_id', 'tax_line_id',
                                  'tax_ids', 'analytic_distribution'],
            'account.account': ['code', 'name', 'account_type', 'reconcile',
                                'deprecated', 'parent_id'],
            'account.journal': ['code', 'name', 'type', 'default_account_id',
                                'company_id'],
            'account.tax': ['name', 'amount', 'type_tax_use', 'tax_group_id',
                            'price_include', 'company_id'],
        }

        extra = mapping.get(model_name, [])
        combined = base + extra
        seen = set()
        result = []
        for x in combined:
            if x not in seen:
                seen.add(x)
                result.append(x)
        return result

    def _clean_record(self, record, fields):
        """
        Clean a record to be XML-RPC safe and SQLite friendly.
        """
        cleaned = {}
        for key in fields:
            val = record.get(key)

            if val is None:
                cleaned[key] = False
            elif isinstance(val, dict):
                cleaned[key] = json.dumps(val, default=str)
            elif isinstance(val, (list, tuple)):
                if len(val) == 2 and isinstance(val[0], int) and isinstance(val[1], str):
                    cleaned[key] = val[0]
                else:
                    cleaned[key] = json.dumps(val, default=str)
            else:
                cleaned[key] = val

        return cleaned

    def _table_columns(self, table_name):
        """Return list of column names in SQLite table."""
        if table_name in self._table_schemas:
            return self._table_schemas[table_name]

        try:
            rows = self.db.query("PRAGMA table_info(" + table_name + ")")
            cols = []
            for r in rows:
                if isinstance(r, dict):
                    name = r.get('name')
                    if name is None:
                        vals = list(r.values()) if hasattr(r, 'values') else []
                        name = vals[1] if len(vals) > 1 else None
                elif isinstance(r, (list, tuple)):
                    name = r[1] if len(r) > 1 else r[0]
                else:
                    name = str(r)
                if name:
                    cols.append(name)

            self._table_schemas[table_name] = cols
            return cols
        except Exception as e:
            print("      ⚠️  Could not read table columns: " + str(e))
            return []

    def _ensure_table(self, table_name, fields):
        """
        Create table if not exists.
        If exists, add missing columns via ALTER TABLE.
        """
        existing = self._table_columns(table_name)

        if not existing:
            columns = []
            for f in fields:
                if f == 'id':
                    columns.append("id INTEGER PRIMARY KEY")
                else:
                    columns.append(f + " TEXT")
            sql = "CREATE TABLE IF NOT EXISTS " + table_name + " (" + ", ".join(columns) + ")"
            self.db.execute(sql)
            self._table_schemas[table_name] = fields.copy()
            return

        for f in fields:
            if f not in existing:
                try:
                    self.db.execute("ALTER TABLE " + table_name + " ADD COLUMN " + f + " TEXT")
                    print("      ➕ Added column: " + f)
                    existing.append(f)
                except Exception as e:
                    print("      ⚠️  Could not add column " + f + ": " + str(e))

        self._table_schemas[table_name] = existing

    def _insert_records(self, table_name, records):
        """Insert only columns that exist in the actual table."""
        if not records:
            return 0

        columns = self._table_columns(table_name)

        if not columns and records:
            columns = list(records[0].keys())
            print("      ℹ️  Using record keys as columns")

        if not columns:
            print("      ⚠️  Cannot determine columns, skipping insert")
            return 0

        placeholders = ", ".join(["?" for _ in columns])
        col_names = ", ".join(columns)
        sql = "INSERT OR REPLACE INTO " + table_name + " (" + col_names + ") VALUES (" + placeholders + ")"

        values = []
        for rec in records:
            row = []
            for c in columns:
                val = rec.get(c)
                if val is False:
                    row.append(None)
                else:
                    row.append(val)
            values.append(tuple(row))

        self.db.executemany(sql, values)
        return len(values)
