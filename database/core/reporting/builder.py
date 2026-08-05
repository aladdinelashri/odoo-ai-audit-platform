from typing import Dict, Any, List, Tuple, Optional
from .ast import validate_ast, SimpleSelectAST, QueryAST


class SQLBuilder:
    @staticmethod
    def _is_simple_ast(ast: Dict[str, Any]) -> bool:
        """Detect simple AST format: has 'columns' and 'from' is a string (or 'table' is a string)."""
        has_columns = "columns" in ast
        from_is_string = isinstance(ast.get("from"), str)
        has_table_string = isinstance(ast.get("table"), str)
        return has_columns and (from_is_string or has_table_string)

    # ---------- Simple format builders ----------

    @staticmethod
    def _build_select_simple(ast: SimpleSelectAST) -> str:
        if not ast.columns or ast.columns == ["*"]:
            return "SELECT *"
        return "SELECT " + ", ".join(ast.columns)

    @staticmethod
    def _build_from_simple(ast: SimpleSelectAST) -> str:
        table = ast.table or ast.from_
        return f"FROM {table}"

    @staticmethod
    def _build_where_simple(ast: SimpleSelectAST, params: List[Any]) -> Optional[str]:
        if not ast.where:
            return None

        conditions = []
        where = ast.where

        # Explicit condition format: {"left": "col", "operator": "=", "right": "val"}
        if "left" in where and "operator" in where:
            cond_sql = SQLBuilder._parse_condition(where, params)
            if cond_sql:
                conditions.append(cond_sql)
        else:
            # Simple key-value format: {"col": "val", "col2": "val2"}
            for key, value in where.items():
                conditions.append(f"{key} = %s")
                params.append(value)

        if not conditions:
            return None
        return "WHERE " + " AND ".join(conditions)

    @staticmethod
    def _build_order_by_simple(ast: SimpleSelectAST) -> Optional[str]:
        if not ast.order_by:
            return None
        return "ORDER BY " + ", ".join(ast.order_by)

    # ---------- Complex format builders ----------

    @staticmethod
    def _build_select_complex(ast: QueryAST) -> str:
        parts = []
        for item in ast.select:
            if isinstance(item, str):
                parts.append(item)
            else:
                # SelectItem with 'column' and optional 'alias'
                if item.alias:
                    parts.append(f"{item.column} AS {item.alias}")
                else:
                    parts.append(item.column)
        return "SELECT " + ", ".join(parts)

    @staticmethod
    def _build_from_complex(ast: QueryAST) -> str:
        table = ast.from_.table
        alias = ast.from_.alias
        if alias:
            return f"FROM {table} AS {alias}"
        return f"FROM {table}"

    @staticmethod
    def _build_where_complex(ast: QueryAST, params: List[Any]) -> Optional[str]:
        if not ast.where:
            return None

        where_clause = ast.where
        if isinstance(where_clause, dict):
            where_clause = [where_clause]

        conditions = []
        for cond in where_clause:
            sql_cond = SQLBuilder._parse_condition(cond, params)
            if sql_cond:
                conditions.append(sql_cond)

        if not conditions:
            return None
        return "WHERE " + " AND ".join(conditions)

    @staticmethod
    def _build_order_by_complex(ast: QueryAST) -> Optional[str]:
        if not ast.order_by:
            return None
        parts = []
        for item in ast.order_by:
            direction = (item.direction or "ASC").upper()
            parts.append(f"{item.column} {direction}")
        return "ORDER BY " + ", ".join(parts)

    # ---------- Shared condition parser ----------

    @staticmethod
    def _parse_condition(cond: Dict[str, Any], params: List[Any]) -> Optional[str]:
        """Parse a single WHERE condition dict."""
        if "logical" in cond:
            # Nested logical group: {"logical": "AND", "conditions": [...]}
            sub_conds = []
            for sub in cond.get("conditions", []):
                parsed = SQLBuilder._parse_condition(sub, params)
                if parsed:
                    sub_conds.append(parsed)
            if not sub_conds:
                return None
            logic = cond["logical"]
            return f"({f' {logic} '.join(sub_conds)})"

        # Simple condition: {"left": "col", "operator": "=", "right": "val"}
        left = cond.get("left")
        operator = cond.get("operator", "=")
        right = cond.get("right")

        if not left or not operator:
            return None

        op = operator.upper()

        if op in ("=", "!=", "<>", ">", "<", ">=", "<="):
            params.append(right)
            return f"{left} {op} %s"
        elif op == "IN":
            if not isinstance(right, list):
                raise ValueError("IN operator requires a list of values")
            if not right:
                return "1=0"
            placeholders = ",".join(["%s"] * len(right))
            params.extend(right)
            return f"{left} IN ({placeholders})"
        elif op == "NOT IN":
            if not isinstance(right, list):
                raise ValueError("NOT IN operator requires a list of values")
            if not right:
                return "1=1"
            placeholders = ",".join(["%s"] * len(right))
            params.extend(right)
            return f"{left} NOT IN ({placeholders})"
        elif op == "IS NULL":
            return f"{left} IS NULL"
        elif op == "IS NOT NULL":
            return f"{left} IS NOT NULL"
        elif op == "BETWEEN":
            if not isinstance(right, (list, tuple)) or len(right) != 2:
                raise ValueError("BETWEEN requires a list of two values")
            params.extend(right)
            return f"{left} BETWEEN %s AND %s"
        elif op == "NOT BETWEEN":
            if not isinstance(right, (list, tuple)) or len(right) != 2:
                raise ValueError("NOT BETWEEN requires a list of two values")
            params.extend(right)
            return f"{left} NOT BETWEEN %s AND %s"
        elif op in ("LIKE", "ILIKE"):
            params.append(right)
            return f"{left} {op} %s"
        else:
            # Fallback for unknown operators
            params.append(right)
            return f"{left} {op} %s"

    # ---------- Public API ----------

    @staticmethod
    def ast_to_sql(ast: Dict[str, Any]) -> Tuple[str, List[Any]]:
        """
        Convert an AST dictionary to SQL and parameters.
        Supports both simple and complex formats.
        """
        if not validate_ast(ast):
            raise ValueError("Invalid AST structure")

        params: List[Any] = []
        sql_parts: List[str] = []

        if SQLBuilder._is_simple_ast(ast):
            # Simple format
            simple = SimpleSelectAST(**ast)
            sql_parts.append(SQLBuilder._build_select_simple(simple))
            sql_parts.append(SQLBuilder._build_from_simple(simple))

            where_sql = SQLBuilder._build_where_simple(simple, params)
            if where_sql:
                sql_parts.append(where_sql)

            order_sql = SQLBuilder._build_order_by_simple(simple)
            if order_sql:
                sql_parts.append(order_sql)

            if simple.limit is not None:
                sql_parts.append("LIMIT %s")
                params.append(simple.limit)
            if simple.offset is not None:
                sql_parts.append("OFFSET %s")
                params.append(simple.offset)
        else:
            # Complex format
            complex_ast = QueryAST(**ast)
            sql_parts.append(SQLBuilder._build_select_complex(complex_ast))
            sql_parts.append(SQLBuilder._build_from_complex(complex_ast))

            where_sql = SQLBuilder._build_where_complex(complex_ast, params)
            if where_sql:
                sql_parts.append(where_sql)

            order_sql = SQLBuilder._build_order_by_complex(complex_ast)
            if order_sql:
                sql_parts.append(order_sql)

            if complex_ast.limit is not None:
                sql_parts.append("LIMIT %s")
                params.append(complex_ast.limit)
            if complex_ast.offset is not None:
                sql_parts.append("OFFSET %s")
                params.append(complex_ast.offset)

        sql = " ".join(sql_parts)
        return sql, params

    @staticmethod
    def build(query_plan: Dict[str, Any]) -> Tuple[str, List[Any]]:
        """Build SQL from query plan. Returns (sql, params)."""
        return SQLBuilder.ast_to_sql(query_plan)
