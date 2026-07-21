from .company_reader import CompanyReader
from .model_reader import ModelReader
from .partner_reader import PartnerReader
from .user_reader import UserReader

from .product_template_reader import ProductTemplateReader
from .product_product_reader import ProductProductReader
from .product_category_reader import ProductCategoryReader

from .pos_category_reader import POSCategoryReader
from .pos_config_reader import POSConfigReader
from .pos_session_reader import POSSessionReader
from .pos_order_reader import POSOrderReader
from .pos_order_line_reader import POSOrderLineReader
from .pos_payment_reader import POSPaymentReader

from .account_account_reader import AccountAccountReader
from .account_move_reader import AccountMoveReader
from .account_move_line_reader import AccountMoveLineReader
from .account_journal_reader import AccountJournalReader
from .account_payment_reader import AccountPaymentReader
from .account_tax_reader import AccountTaxReader

from .stock_move_reader import StockMoveReader
from .stock_move_line_reader import StockMoveLineReader
from .stock_quant_reader import StockQuantReader


__all__ = [
    "CompanyReader",
    "ModelReader",
    "PartnerReader",
    "UserReader",

    "ProductTemplateReader",
    "ProductProductReader",
    "ProductCategoryReader",

    "POSCategoryReader",
    "POSConfigReader",
    "POSSessionReader",
    "POSOrderReader",
    "POSOrderLineReader",
    "POSPaymentReader",

    "AccountAccountReader",
    "AccountMoveReader",
    "AccountMoveLineReader",
    "AccountJournalReader",
    "AccountPaymentReader",
    "AccountTaxReader",

    "StockMoveReader",
    "StockMoveLineReader",
    "StockQuantReader",
]
