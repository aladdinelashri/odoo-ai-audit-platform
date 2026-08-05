"""Unit tests for AST validation."""
import pytest
from database.core.reporting.ast import validate_ast, ASTValidationError


class TestASTValidation:
    """Test AST validation and SQL injection prevention."""

    def test_valid_simple_query(self):
        ast = {
            "select": ["id", "order_name", "amount_total"],
            "from": "pos_orders",
            "where": {"field": "state", "op": "=", "value": "paid"},
            "limit": 100,
        }
        validate_ast(ast)  # Should not raise

    def test_valid_complex_query(self):
        ast = {
            "select": ["id", "order_name"],
            "from": "pos_orders",
            "where": {
                "and": [
                    {"field": "amount_total", "op": ">", "value": 100},
                    {"field": "state", "op": "=", "value": "paid"},
                ]
            },
            "order_by": [{"field": "order_date", "direction": "desc"}],
            "limit": 50,
        }
        validate_ast(ast)

    def test_invalid_table(self):
        ast = {"select": ["id"], "from": "users"}
        with pytest.raises(ASTValidationError, match="not in whitelist"):
            validate_ast(ast)

    def test_invalid_column(self):
        ast = {"select": ["id", "hacked_column"], "from": "pos_orders"}
        with pytest.raises(ASTValidationError, match="not allowed"):
            validate_ast(ast)

    def test_sql_injection_prevention(self):
        ast = {
            "select": ["id"],
            "from": "pos_orders",
            "where": {"field": "state", "op": "=", "value": "'; DROP TABLE pos_orders; --"},
        }
        with pytest.raises(ASTValidationError, match="injection"):
            validate_ast(ast)

    def test_union_injection_blocked(self):
        ast = {
            "select": ["id"],
            "from": "pos_orders",
            "where": {"field": "order_name", "op": "=", "value": "test' UNION SELECT * FROM users--"},
        }
        with pytest.raises(ASTValidationError):
            validate_ast(ast)

    def test_limit_too_high(self):
        ast = {"select": ["id"], "from": "pos_orders", "limit": 999999}
        with pytest.raises(ASTValidationError, match="limit"):
            validate_ast(ast)

    def test_nested_logical_operators(self):
        ast = {
            "select": ["id"],
            "from": "pos_orders",
            "where": {
                "and": [
                    {"field": "amount_total", "op": ">", "value": 50},
                    {
                        "or": [
                            {"field": "state", "op": "=", "value": "paid"},
                            {"field": "state", "op": "=", "value": "pending"},
                        ]
                    },
                ]
            },
        }
        validate_ast(ast)

    def test_is_null_operator(self):
        ast = {
            "select": ["id"],
            "from": "pos_orders",
            "where": {"field": "partner_id", "op": "is_null"},
        }
        validate_ast(ast)

    def test_in_operator(self):
        ast = {
            "select": ["id"],
            "from": "pos_orders",
            "where": {"field": "state", "op": "in", "value": ["paid", "pending"]},
        }
        validate_ast(ast)
