import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from database.core.odoo.readers import (
    CompanyReader,
    UserReader,
    PartnerReader,
    ProductTemplateReader,
    ProductProductReader,
    ProductCategoryReader,
    POSCategoryReader,
    POSConfigReader,
    POSSessionReader,
    POSOrderReader,
    POSOrderLineReader,
    POSPaymentReader,
    AccountAccountReader,
    AccountMoveReader,
    AccountMoveLineReader,
    AccountJournalReader,
    AccountPaymentReader,
    AccountTaxReader,
    StockMoveReader,
    StockMoveLineReader,
    StockQuantReader,
)


def test_all_readers():

    readers = [
        CompanyReader(),
        UserReader(),
        PartnerReader(),
        ProductTemplateReader(),
        ProductProductReader(),
        ProductCategoryReader(),
        POSCategoryReader(),
        POSConfigReader(),
        POSSessionReader(),
        POSOrderReader(),
        POSOrderLineReader(),
        POSPaymentReader(),
        AccountAccountReader(),
        AccountMoveReader(),
        AccountMoveLineReader(),
        AccountJournalReader(),
        AccountPaymentReader(),
        AccountTaxReader(),
        StockMoveReader(),
        StockMoveLineReader(),
        StockQuantReader(),
    ]

    for reader in readers:
        record = reader.first()
        assert record is not None
