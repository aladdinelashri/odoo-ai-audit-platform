"""Unit tests for SQL builder."""
import pytest
from database.core.reporting.builder import SQLBuilder
from database.core.reporting.ast import validate_ast


class TestSQLBuilder:
    """Test AST to SQL conversion."""

    def test_simple_select(self):
        ast = {
            "select": ["id", "order_name"],
            "from": "pos_orders",
            "limit": 10,
        }
        validate_ast(ast)
        sql, params = SQLBuilder.ast_to_sql(ast)
        assert "SELECT" in sql
        assert "FROM" in sql
        assert "pos_orders" in sql
        assert params == []

    def test_where_condition(self):
        ast = {
            "select": ["id"],
            "from": "pos_orders",
            "where": {"field": "state", "op": "=", "value": "paid"},
        }
        validate_ast(ast)
        sql, params = SQLBuilder.ast_to_sql(ast)
        assert "WHERE" in sql
        assert params == ["paid"]

    def test_and_condition(self):
        ast = {
            "select": ["id"],
            "from": "pos_orders",
            "where": {
                "and": [
                    {"field": "amount_total", "op": ">", "value": 100},
                    {"field": "state", "op": "=", "value": "paid"},
                ]
            },
        }
        validate_ast(ast)
        sql, params = SQLBuilder.ast_to_sql(ast)
        assert "AND" in sql
        assert params == [100, "paid"]

    def test_or_condition(self):
        ast = {
            "select": ["id"],
            "from": "pos_orders",
            "where": {
                "or": [
                    {"field": "state", "op": "=", "value": "paid"},
                    {"field": "state", "op": "=", "value": "pending"},
                ]
            },
        }
        validate_ast(ast)
        sql, params = SQLBuilder.ast_to_sql(ast)
        assert "OR" in sql
        assert params == ["paid", "pending"]

    def test_order_by(self):
        ast = {
            "select": ["id", "order_date"],
            "from": "pos_orders",
            "order_by": [{"field": "order_date", "direction": "desc"}],
        }
        validate_ast(ast)
        sql, params = SQLBuilder.ast_to_sql(ast)
        assert "ORDER BY" in sql
        assert "DESC" in sql

    def test_in_operator(self):
        ast = {
            "select": ["id"],
            "from": "pos_orders",
            "where": {"field": "state", "op": "in", "value": ["paid", "pending"]},
        }
        validate_ast(ast)
        sql, params = SQLBuilder.ast_to_sql(ast)
        assert "IN" in sql
        assert params == ["paid", "pending"]

    def test_like_operator(self):
        ast = {
            "select": ["id"],
            "from": "pos_orders",
            "where": {"field": "order_name", "op": "like", "value": "Order-%"},
        }
        validate_ast(ast)
        sql, params = SQLBuilder.ast_to_sql(ast)
        assert "LIKE" in sql
        assert params == ["Order-%"]
