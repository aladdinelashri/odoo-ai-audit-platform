"""
Audit Runner — executes audits using the registry and context builder.
Separates execution logic from CLI.
"""

import json
from typing import Any, Dict, Optional

from config.logging import get_logger
from database.core.context.context_builder import AuditContextBuilder, AuditContext
from database.core.audits.registry.audit_registry import AuditRegistry, registry

logger = get_logger('audit.runner')


class AuditRunner:
    """
    High-level runner for audit operations.
    Can be used by CLI, API, scheduler, or tests.
    """
    
    def __init__(self, sqlite_service=None):
        self.context_builder = AuditContextBuilder(sqlite_service)
        self.registry = registry
    
    def run(
        self,
        audit_name: str,
        session_id: int = None,
        business_unit_id: int = None,
        date_from: str = None,
        date_to: str = None,
        **filters
    ) -> Dict[str, Any]:
        """
        Run a single audit with full context.
        
        Args:
            audit_name: Name of registered audit
            session_id: Optional session filter
            business_unit_id: Optional business unit filter
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
            **filters: Additional audit-specific filters
        
        Returns:
            Dictionary with audit results and metadata
        """
        logger.info(f"AuditRunner starting: {audit_name}")
        
        # Build context
        context = self.context_builder.build(
            session_id=session_id,
            business_unit_id=business_unit_id,
            date_from=date_from,
            date_to=date_to,
            **filters
        )
        
        # Run audit via registry
        result = self.registry.run(audit_name, context, **filters)
        
        # Wrap result with metadata
        return {
            'audit': audit_name,
            'timestamp': self._now(),
            'context': {
                'business_unit': context.business_unit.name if context.business_unit else None,
                'session_id': session_id,
                'date_from': date_from,
                'date_to': date_to,
            },
            'result': result,
            'status': 'success'
        }
    
    def run_all(
        self,
        category: str = 'pos',
        session_id: int = None,
        business_unit_id: int = None,
        date_from: str = None,
        date_to: str = None,
        **filters
    ) -> Dict[str, Any]:
        """
        Run all audits in a category.
        
        Returns:
            Dictionary mapping audit names to results
        """
        audits = self.registry.list_audits(category=category)
        results = {}
        
        for name in audits:
            try:
                results[name] = self.run(
                    name,
                    session_id=session_id,
                    business_unit_id=business_unit_id,
                    date_from=date_from,
                    date_to=date_to,
                    **filters
                )
            except Exception as e:
                logger.error(f"Audit '{name}' failed: {e}")
                results[name] = {
                    'audit': name,
                    'status': 'error',
                    'error': str(e)
                }
        
        return {
            'category': category,
            'timestamp': self._now(),
            'total': len(audits),
            'completed': sum(1 for r in results.values() if r.get('status') == 'success'),
            'results': results
        }
    
    def list_available(self, category: str = None) -> Dict[str, str]:
        """List available audits with descriptions."""
        audits = self.registry.list_audits(category=category)
        return {name: info.description for name, info in audits.items()}
    
    def _now(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()


# Convenience function
def run_audit(audit_name: str, **kwargs) -> Dict[str, Any]:
    """Quick-run a single audit."""
    runner = AuditRunner()
    return runner.run(audit_name, **kwargs)
