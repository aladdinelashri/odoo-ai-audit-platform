#!/bin/bash
set -euo pipefail

PROJECT_DIR="$(pwd)"
DB_PATH="database/storage/audit.db"
BACKUP_DIR="${PROJECT_DIR}/.backup_$(date +%Y%m%d_%H%M%S)"

echo "============================================================"
echo "  Odoo AI Audit — Performance Optimization Deployment"
echo "============================================================"
echo ""

# Step 1: Backup existing files
mkdir -p "${BACKUP_DIR}/database/core/audits/accounting"
mkdir -p "${BACKUP_DIR}/database/core/storage/sqlite"

for f in database/core/audits/accounting/journal_audit.py \
         database/core/audits/accounting/tax_validation_audit.py \
         database/core/audits/accounting/ledger_integrity_audit.py \
         database/core/audits/accounting/__init__.py; do
    if [ -f "$f" ]; then
        cp "$f" "${BACKUP_DIR}/$f"
        echo "[BACKUP] $f"
    fi
done

# Step 2: Create new directories
mkdir -p database/core/storage/sqlite
mkdir -p scripts
mkdir -p tests/unit

echo ""
echo "[INFO] Backup saved to: ${BACKUP_DIR}"
echo ""
