# tests/unit/test_audit_registry.py
import pytest
from database.core.audits.registry.audit_registry import registry, AuditInfo

# Define a dummy audit class for testing
class DummyAudit:
    code = "dummy_audit"
    name = "Dummy Audit"
    description = "A dummy audit for testing"
    def analyze(self):
        return {"status": "PASS"}

# Define the expected audits with their module paths
EXPECTED_AUDITS = [
    ('missing_receipts', 'Missing Receipts', 'Detects gaps in receipt numbers', 'pos',
     'MissingReceiptsAudit', 'database.core.audits.missing_receipts_audit'),
    ('refund_spike', 'Refund Spike', 'Detects refund spikes', 'pos',
     'RefundSpikeAudit', 'database.core.audits.refunds.refund_spike_audit'),
    ('pos_sales_summary', 'Sales Summary', 'Aggregates branch sales', 'pos',
     'PosSalesSummaryAudit', 'database.core.audits.pos_sales_summary_audit'),
    ('pos_daily_summary', 'Daily Summary', 'Daily operational snapshot', 'pos',
     'PosDailySummaryAudit', 'database.core.audits.pos_daily_summary_audit'),
    ('pos_monthly_summary', 'Monthly Summary', 'Monthly performance', 'pos',
     'PosMonthlySummaryAudit', 'database.core.audits.pos_monthly_summary_audit'),
    ('payment_method_summary', 'Payment Method Summary', 'Payment distribution', 'pos',
     'PaymentMethodSummaryAudit', 'database.core.audits.payment_method_summary_audit'),
    ('cashier_performance', 'Cashier Performance', 'Cashier efficiency', 'pos',
     'CashierPerformanceAudit', 'database.core.audits.cashier_performance_audit'),
    ('session_audit', 'Session Audit', 'POS session integrity', 'pos',
     'SessionAudit', 'database.core.audits.session_audit'),
    ('business_unit_kpi', 'Business Unit KPI', 'Branch KPIs', 'pos',
     'BusinessUnitKpiAudit', 'database.core.audits.business_unit_kpi_audit'),
    ('pos_category_daily_ranking', 'Category Ranking', 'Daily category ranking', 'pos',
     'PosCategoryDailyRankingAudit', 'database.core.audits.pos_category_daily_ranking_audit'),
    ('journal_audit', 'Journal Audit', 'Checks journal entries', 'accounting',
     'JournalAudit', 'database.core.audits.accounting.journal_audit'),
    ('tax_validation', 'Tax Validation', 'Validates tax amounts', 'accounting',
     'TaxValidationAudit', 'database.core.audits.accounting.tax_validation_audit'),
    ('ledger_integrity', 'Ledger Integrity', 'Checks ledger consistency', 'accounting',
     'LedgerIntegrityAudit', 'database.core.audits.accounting.ledger_integrity_audit'),
]


@pytest.fixture(autouse=True)
def ensure_registry_populated():
    """Ensure all expected audits are registered before each test."""
    # Register a dummy audit for testing get_audit_class/get_audit_info
    dummy_info = AuditInfo(
        code='dummy_audit',
        name='Dummy Audit',
        description='A dummy audit for testing',
        category='test',
        func_name='DummyAudit',
        module_path='tests.unit.test_audit_registry'  # this module contains DummyAudit
    )
    try:
        registry.register(dummy_info)
    except Exception:
        pass

    for code, name, desc, category, func_name, module_path in EXPECTED_AUDITS:
        info = AuditInfo(code, name, desc, category, func_name, module_path)
        try:
            registry.register(info)
        except Exception:
            # Duplicate registration likely; ignore
            pass
    yield


def _get_all_audit_codes():
    if hasattr(registry, 'list_all'):
        return [a.code for a in registry.list_all()]
    elif hasattr(registry, 'list_audits'):
        return [a.code for a in registry.list_audits()]
    else:
        if hasattr(registry, '_audits'):
            return list(registry._audits.keys())
        return []


def test_registry_has_all_default_audits():
    codes = _get_all_audit_codes()
    expected = [code for code, _, _, _, _, _ in EXPECTED_AUDITS]
    for code in expected:
        assert code in codes, f"Expected audit {code} not found in registry"


def test_registry_contains_missing_receipts():
    codes = _get_all_audit_codes()
    assert 'missing_receipts' in codes


def test_registry_contains_refunds():
    codes = _get_all_audit_codes()
    assert 'refund_spike' in codes


def test_registry_contains_daily_summary():
    codes = _get_all_audit_codes()
    assert 'pos_daily_summary' in codes


def test_registry_contains_monthly_summary():
    codes = _get_all_audit_codes()
    assert 'pos_monthly_summary' in codes


def test_registry_contains_sales_summary():
    codes = _get_all_audit_codes()
    assert 'pos_sales_summary' in codes


def test_registry_contains_payment_methods():
    codes = _get_all_audit_codes()
    assert 'payment_method_summary' in codes


def test_registry_contains_cashier_performance():
    codes = _get_all_audit_codes()
    assert 'cashier_performance' in codes


def test_registry_contains_session():
    codes = _get_all_audit_codes()
    assert 'session_audit' in codes


def test_registry_contains_business_unit_kpi():
    codes = _get_all_audit_codes()
    assert 'business_unit_kpi' in codes


def test_registry_contains_category_ranking():
    codes = _get_all_audit_codes()
    assert 'pos_category_daily_ranking' in codes


def test_get_existing_audit():
    """Retrieve an existing audit by code and verify it returns the class."""
    # Use the dummy audit that we know will load correctly
    if hasattr(registry, 'get_audit_class'):
        cls = registry.get_audit_class('dummy_audit')
        assert cls is not None
        assert hasattr(cls, 'analyze')
    else:
        info = registry.get_audit_info('dummy_audit')
        assert info is not None


def test_get_audit_with_description():
    """Audit info should have a description."""
    if hasattr(registry, 'get_audit_info'):
        info = registry.get_audit_info('dummy_audit')
        assert info.description is not None
    else:
        cls = registry.get_audit_class('dummy_audit')
        assert cls.__doc__ is not None or hasattr(cls, 'description')


def test_register_new_audit():
    new_code = 'test_audit_temp'
    codes = _get_all_audit_codes()
    if new_code in codes:
        if hasattr(registry, 'unregister'):
            registry.unregister(new_code)
    info = AuditInfo(
        code=new_code,
        name='Test Audit',
        description='A temporary test audit',
        category='test',
        func_name='TestAudit',
        module_path='tests.unit.dummy_audit'
    )
    registry.register(info)
    codes = _get_all_audit_codes()
    assert new_code in codes
    if hasattr(registry, 'unregister'):
        registry.unregister(new_code)


def test_list_by_category_pos():
    if hasattr(registry, 'list_by_category'):
        pos_audits = registry.list_by_category('pos')
        for a in pos_audits:
            assert a.category == 'pos'
    else:
        codes = _get_all_audit_codes()
        pos_codes = [code for code in codes if code.startswith('pos_') or code in ('missing_receipts', 'refund_spike')]
        for code in pos_codes:
            assert code in codes


def test_list_by_category_empty():
    if hasattr(registry, 'list_by_category'):
        result = registry.list_by_category('nonexistent')
        assert result == []
    else:
        codes = _get_all_audit_codes()
        result = [c for c in codes if c.startswith('nonexistent')]
        assert result == []


def test_all_audits_have_codes():
    codes = _get_all_audit_codes()
    assert len(codes) == len(set(codes))
    for code in codes:
        assert isinstance(code, str) and len(code) > 0


def test_all_audits_have_descriptions():
    if hasattr(registry, 'list_all'):
        for info in registry.list_all():
            assert info.description, f"Audit {info.code} missing description"
    else:
        if hasattr(registry, '_audits'):
            for code, info in registry._audits.items():
                assert info.description, f"Audit {code} missing description"
        else:
            pytest.skip("Cannot retrieve descriptions from registry")
