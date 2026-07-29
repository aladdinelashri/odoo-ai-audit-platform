"""
Audit Registry - Manages all available audit modules
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Type
from database.core.audits.base.base_audit import BaseAudit


@dataclass
class AuditInfo:
    """Information about an audit module."""
    code: str
    name: str
    description: str
    module_path: str
    func_name: str
    category: str = "pos"
    enabled: bool = True


class AuditRegistry:
    """Registry for all audit modules."""
    
    _registry: Dict[str, AuditInfo] = {}
    
    @classmethod
    def register(cls, audit_info: AuditInfo) -> None:
        """Register a new audit."""
        cls._registry[audit_info.code] = audit_info
    
    @classmethod
    def get(cls, code: str) -> Optional[AuditInfo]:
        """Get audit info by code."""
        return cls._registry.get(code)
    
    @classmethod
    def list_all(cls) -> List[AuditInfo]:
        """List all registered audits."""
        return list(cls._registry.values())
    
    @classmethod
    def list_by_category(cls, category: str) -> List[AuditInfo]:
        """List audits by category."""
        return [a for a in cls._registry.values() if a.category == category]
    
    @classmethod
    def get_audit_class(cls, code: str) -> Optional[Type[BaseAudit]]:
        """Get the audit class by code."""
        info = cls.get(code)
        if not info:
            return None
        
        try:
            module = __import__(info.module_path, fromlist=[info.func_name])
            return getattr(module, info.func_name)
        except (ImportError, AttributeError) as e:
            print(f"Error loading audit {code}: {e}")
            return None


# Create a singleton instance for backward compatibility
registry = AuditRegistry()


def _register_default_audits():
    """Register all default audits."""
    # Try to import accounting audits first (they should work)
    try:
        from database.core.audits.accounting.journal_audit import JournalAudit
        registry.register(AuditInfo(
            code="journal_audit",
            name="Journal Audit",
            description="Checks for unbalanced entries, sequence gaps, duplicates.",
            module_path="database.core.audits.accounting.journal_audit",
            func_name="JournalAudit",
            category="accounting"
        ))
    except ImportError as e:
        print(f"Warning: Could not import JournalAudit: {e}")
    
    try:
        from database.core.audits.accounting.tax_validation_audit import TaxValidationAudit
        registry.register(AuditInfo(
            code="tax_validation",
            name="Tax Validation Audit",
            description="Validates tax amounts and rates.",
            module_path="database.core.audits.accounting.tax_validation_audit",
            func_name="TaxValidationAudit",
            category="accounting"
        ))
    except ImportError as e:
        print(f"Warning: Could not import TaxValidationAudit: {e}")
    
    try:
        from database.core.audits.accounting.ledger_integrity_audit import LedgerIntegrityAudit
        registry.register(AuditInfo(
            code="ledger_integrity",
            name="Ledger Integrity Audit",
            description="Checks ledger integrity and account consistency.",
            module_path="database.core.audits.accounting.ledger_integrity_audit",
            func_name="LedgerIntegrityAudit",
            category="accounting"
        ))
    except ImportError as e:
        print(f"Warning: Could not import LedgerIntegrityAudit: {e}")
    
    # Register POS audits (if they exist)
    try:
        from database.core.audits.missing_receipts_audit import MissingReceiptsAudit
        registry.register(AuditInfo(
            code="missing_receipts",
            name="Missing Receipts Audit",
            description="Detects sequential gaps in receipt numbering.",
            module_path="database.core.audits.missing_receipts_audit",
            func_name="MissingReceiptsAudit",
            category="pos"
        ))
    except ImportError:
        pass
    
    try:
        from database.core.audits.refunds.refund_spike_audit import RefundSpikeAudit
        registry.register(AuditInfo(
            code="refunds",
            name="Refund Spike Audit",
            description="Detects unusual spikes in refund activity.",
            module_path="database.core.audits.refunds.refund_spike_audit",
            func_name="RefundSpikeAudit",
            category="pos"
        ))
    except ImportError:
        pass


# Auto-register on import
_register_default_audits()
