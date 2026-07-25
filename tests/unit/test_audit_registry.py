"""Tests for AuditRegistry — Registry Pattern."""

import pytest
from database.core.audits.registry.audit_registry import AuditRegistry, AuditInfo


@pytest.fixture
def registry():
    return AuditRegistry()


# ─── Registration ───
def test_registry_has_all_default_audits(registry):
    audits = registry.list_audits()
    assert len(audits) == 10


def test_registry_contains_missing_receipts(registry):
    assert "missing_receipts" in registry.list_audits()


def test_registry_contains_refunds(registry):
    assert "refunds" in registry.list_audits()


def test_registry_contains_daily_summary(registry):
    assert "daily_summary" in registry.list_audits()


def test_registry_contains_monthly_summary(registry):
    assert "monthly_summary" in registry.list_audits()


def test_registry_contains_sales_summary(registry):
    assert "sales_summary" in registry.list_audits()


def test_registry_contains_payment_methods(registry):
    assert "payment_methods" in registry.list_audits()


def test_registry_contains_cashier_performance(registry):
    assert "cashier_performance" in registry.list_audits()


def test_registry_contains_session(registry):
    assert "session" in registry.list_audits()


def test_registry_contains_business_unit_kpi(registry):
    assert "business_unit_kpi" in registry.list_audits()


def test_registry_contains_category_ranking(registry):
    assert "category_ranking" in registry.list_audits()


# ─── Get Audit ───
def test_get_existing_audit(registry):
    info = registry.get("missing_receipts")
    assert info is not None
    assert isinstance(info, AuditInfo)
    assert info.code == "MISSING_RCPT"
    assert info.name == "missing_receipts"


def test_get_audit_with_description(registry):
    info = registry.get("cashier_performance")
    assert info.description == "Cashier performance KPI"


def test_get_nonexistent_audit(registry):
    assert registry.get("nonexistent_audit") is None


# ─── Custom Registration ───
def test_register_new_audit(registry):
    new_audit = AuditInfo(
        name="custom_audit",
        code="CUSTOM",
        description="A custom test audit",
        module_path="tests.dummy",
    )
    registry.register(new_audit)
    assert "custom_audit" in registry.list_audits()
    assert registry.get("custom_audit").code == "CUSTOM"


# ─── Category Filter ───
def test_list_by_category_pos(registry):
    pos_audits = registry.list_audits(category="pos")
    assert len(pos_audits) == 10


def test_list_by_category_empty(registry):
    empty = registry.list_audits(category="accounting")
    assert len(empty) == 0


# ─── Audit Metadata ───
def test_all_audits_have_codes(registry):
    for name, info in registry.list_audits().items():
        assert info.code, f"Audit {name} missing code"
        assert info.module_path, f"Audit {name} missing module_path"


def test_all_audits_have_descriptions(registry):
    for name, info in registry.list_audits().items():
        assert info.description, f"Audit {name} missing description"
