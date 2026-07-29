# ast.py
from typing import List, Dict, Any, Optional
import json
from sqlalchemy import text, Table, MetaData, select, join, and_, or_, func
from sqlalchemy.sql import elements

class QueryAST:
    """
    Simple container for AST. We'll use dicts for flexibility and JSON serialization.
    """

    @staticmethod
    def validate(ast: dict) -> bool:
        """Basic validation of AST structure."""
        required = ["select", "from"]
        for r in required:
            if r not in ast:
                raise ValueError(f"Missing required key: {r}")
        # more validation as needed
        return True
