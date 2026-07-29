# database/core/audits/base/base_pos_audit.py
"""
Base class for all POS-related audits.
Provides common functionality and sets the category to 'pos'.
"""
from .base_audit import BaseAudit


class BasePOSAudit(BaseAudit):
    """
    Base class for POS audits.
    
    All POS audit modules should inherit from this class.
    It sets the category to 'pos' and ensures proper constructor chaining.
    """
    category = "pos"

    def __init__(self):
        """
        Initialize the POS audit.
        Calls the parent constructor without any arguments to avoid
        TypeError when BaseAudit.__init__() does not accept parameters.
        """
        super().__init__()

    # Additional shared POS audit methods can be added here.
