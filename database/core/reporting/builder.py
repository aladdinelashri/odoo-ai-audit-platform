# builder.py
from typing import Dict, Any, List, Tuple
import json

class SQLBuilder:
    @staticmethod
    def ast_to_sql(ast: Dict[str, Any]) -> Tuple[str, List[Any]]:
        """
        Convert AST dict to SQL string with ? placeholders and a list of parameter values.
        """
        sql_parts = []
        params = []

        # ---------- SELECT ----------
        select_list = []
        for col in ast.get("select", []):
            expr = col["expr"]
            alias = col.get("alias")
            if alias:
                select_list.append(f"{expr} AS {alias}")
            else:
                select_list.append(expr)
        if not select_list:
            raise ValueError("SELECT list is empty")
        sql_parts.append("SELECT " + ", ".join(select_list))

        # ---------- FROM ----------
        from_table = ast["from"]["table"]
        from_alias = ast["from"].get("alias")
        if from_alias:
            from_clause = f"{from_table} AS {from_alias}"
        else:
            from_clause = from_table
        sql_parts.append("FROM " + from_clause)

        # ---------- JOINs ----------
        for join_def in ast.get("joins", []):
            join_type = join_def.get("type", "INNER").upper()
            join_table = join_def["table"]
            join_alias = join_def.get("alias")
            if join_alias:
                join_clause = f"{join_table} AS {join_alias}"
            else:
                join_clause = join_table
            on_cond = join_def["on"]
            # on_cond expected: {"left": "left_col", "right": "right_col"} or complex expression
            # For simplicity we assume equality
            on_sql = f"{on_cond['left']} = {on_cond['right']}"
            sql_parts.append(f"{join_type} JOIN {join_clause} ON {on_sql}")

        # ---------- WHERE ----------
        where_conditions = ast.get("where", {}).get("conditions", [])
        if where_conditions:
            where_clauses = []
            for cond in where_conditions:
                field = cond["field"]
                op = cond["op"].upper()
                value = cond["value"]

                if op in ("=", ">", "<", ">=", "<="):
                    where_clauses.append(f"{field} {op} ?")
                    params.append(value)
                elif op == "IN":
                    if not isinstance(value, list):
                        raise ValueError("IN operator requires a list of values")
                    placeholders = ",".join(["?"] * len(value))
                    where_clauses.append(f"{field} IN ({placeholders})")
                    params.extend(value)
                elif op in ("LIKE", "ILIKE"):
                    where_clauses.append(f"{field} {op} ?")
                    params.append(value)
                else:
                    raise ValueError(f"Unsupported operator: {op}")

            logic = ast.get("where", {}).get("logic", "AND").upper()
            sql_parts.append("WHERE " + f" {logic} ".join(where_clauses))

        # ---------- GROUP BY ----------
        group_by = ast.get("group_by")
        if group_by:
            sql_parts.append("GROUP BY " + ", ".join(group_by))

        # ---------- ORDER BY ----------
        order_by = ast.get("order_by")
        if order_by:
            order_list = []
            for order in order_by:
                field = order["field"]
                direction = order.get("direction", "ASC").upper()
                order_list.append(f"{field} {direction}")
            sql_parts.append("ORDER BY " + ", ".join(order_list))

        # ---------- LIMIT / OFFSET ----------
        limit = ast.get("limit")
        if limit is not None:
            sql_parts.append("LIMIT ?")
            params.append(limit)
        offset = ast.get("offset")
        if offset is not None:
            sql_parts.append("OFFSET ?")
            params.append(offset)

        sql = " ".join(sql_parts)
        return sql, params
