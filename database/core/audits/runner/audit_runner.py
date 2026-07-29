"""
Audit Runner - Executes audits and manages results
"""
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from database.core.audits.registry.audit_registry import AuditRegistry, registry
from database.core.audits.base.base_audit import BaseAudit

logger = logging.getLogger(__name__)


class AuditRunner:
    """Runner for executing audits."""
    
    def __init__(self):
        self.results = {}
    
    def list_audits(self) -> List[Dict[str, Any]]:
        """List all available audits."""
        audits = []
        for info in registry.list_all():
            audits.append({
                "code": info.code,
                "name": info.name,
                "description": info.description,
                "category": info.category,
                "enabled": info.enabled
            })
        return audits
    
    def run(self, code: str = None, context: Optional[Dict] = None, 
            category: str = None, run_all: bool = False, **kwargs) -> Dict[str, Any]:
        """
        Main entry point for running audits.
        
        Args:
            code: Specific audit code to run
            context: Optional context (date range, filters, etc.)
            category: Category to run ('pos' or 'accounting')
            run_all: Run all audits if True
            **kwargs: Additional arguments (e.g., session_id, date_from, date_to)
        
        Returns:
            Audit results
        """
        # Merge context with kwargs
        if context is None:
            context = {}
        for key, value in kwargs.items():
            if key not in context:
                context[key] = value
        
        if run_all:
            return self.run_all(**context)
        elif category:
            return self.run_by_category(category, context)
        elif code:
            return self.run_audit(code, context)
        else:
            return {
                "status": "error",
                "error": "No audit specified. Provide code, category, or run_all=True",
                "timestamp": datetime.now().isoformat()
            }
    
    def run_audit(self, code: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Run a single audit by code.
        
        Args:
            code: Audit code to run
            context: Optional context (date range, filters, etc.)
            
        Returns:
            Audit results
        """
        try:
            # Get audit info
            info = registry.get(code)
            if not info:
                return {
                    "audit": code,
                    "status": "error",
                    "error": f"Audit '{code}' not found",
                    "executed_at": datetime.now().isoformat()
                }
            
            # Get audit class
            audit_class = registry.get_audit_class(code)
            if not audit_class:
                return {
                    "audit": code,
                    "status": "error",
                    "error": f"Could not load audit class for '{code}'",
                    "executed_at": datetime.now().isoformat()
                }
            
            # Instantiate and run
            audit_instance = audit_class(context or {})
            result = audit_instance.analyze()
            
            # Add metadata
            result["executed_at"] = datetime.now().isoformat()
            result["audit_code"] = code
            
            # Store result
            self.results[code] = result
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to run audit '{code}': {e}")
            return {
                "audit": code,
                "status": "error",
                "error": str(e),
                "executed_at": datetime.now().isoformat()
            }
    
    def run_all(self, context: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """
        Run all enabled audits.
        
        Args:
            context: Optional context (date range, filters, etc.)
            **kwargs: Additional arguments to merge into context
            
        Returns:
            Summary of all audit results
        """
        # Merge kwargs into context
        if context is None:
            context = {}
        for key, value in kwargs.items():
            if key not in context:
                context[key] = value
        
        results = {}
        completed = 0
        errors = 0
        
        for info in registry.list_all():
            if not info.enabled:
                continue
            
            result = self.run_audit(info.code, context)
            results[info.code] = result
            
            if result.get("status") == "error":
                errors += 1
            else:
                completed += 1
        
        return {
            "category": "all",
            "timestamp": datetime.now().isoformat(),
            "total": len(results),
            "completed": completed,
            "errors": errors,
            "results": results
        }
    
    def run_by_category(self, category: str, context: Optional[Dict] = None, **kwargs) -> Dict[str, Any]:
        """
        Run all audits in a category.
        
        Args:
            category: Category name ('pos' or 'accounting')
            context: Optional context
            **kwargs: Additional arguments to merge into context
            
        Returns:
            Summary of audit results
        """
        # Merge kwargs into context
        if context is None:
            context = {}
        for key, value in kwargs.items():
            if key not in context:
                context[key] = value
        
        results = {}
        completed = 0
        errors = 0
        
        for info in registry.list_by_category(category):
            if not info.enabled:
                continue
            
            result = self.run_audit(info.code, context)
            results[info.code] = result
            
            if result.get("status") == "error":
                errors += 1
            else:
                completed += 1
        
        return {
            "category": category,
            "timestamp": datetime.now().isoformat(),
            "total": len(results),
            "completed": completed,
            "errors": errors,
            "results": results
        }
    
    def get_result(self, code: str) -> Optional[Dict[str, Any]]:
        """Get a stored audit result."""
        return self.results.get(code)
    
    def clear_results(self) -> None:
        """Clear all stored results."""
        self.results.clear()
