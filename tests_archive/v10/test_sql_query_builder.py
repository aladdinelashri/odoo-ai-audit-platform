from database.compiler.sql_query_builder import SQLQueryBuilder


def test_simple_query():
    builder = SQLQueryBuilder()

    plan = {
        "select": ["*"],
        "from": "account.move",
        "where": [],
        "order": [],
        "limit": 100,
    }

    sql, params = builder.build(plan)

    assert sql.startswith("SELECT *")
    assert params == []


def test_query_with_parameter():
    builder = SQLQueryBuilder()

    plan = {
        "select": ["*"],
        "from": "account.move",
        "where": [
            "state = %s",
        ],
        "where_values": [
            "posted",
        ],
        "order": [],
        "limit": 100,
    }

    sql, params = builder.build(plan)

    assert "WHERE state = %s" in sql
    assert params == ["posted"]


def test_multiple_parameters():
    builder = SQLQueryBuilder()

    plan = {
        "select": ["*"],
        "from": "account.move",
        "where": [
            "state = %s",
            "amount_total > %s",
        ],
        "where_values": [
            "posted",
            100,
        ],
        "order": [],
        "limit": 100,
    }

    sql, params = builder.build(plan)

    assert len(params) == 2
    assert params == ["posted", 100]


def test_aggregate_query():
    builder = SQLQueryBuilder()

    plan = {
        "select": ["COUNT(*)"],
        "from": "account.move",
        "where": [],
        "order": [],
        "limit": None,
    }

    sql, params = builder.build(plan)

    assert sql.startswith("SELECT COUNT(*)")
    assert params == []


def test_order_limit():
    builder = SQLQueryBuilder()

    plan = {
        "select": ["*"],
        "from": "account.move",
        "where": [],
        "order": [
            "create_date DESC",
        ],
        "limit": 10,
    }

    sql, params = builder.build(plan)

    assert "ORDER BY create_date DESC" in sql
    assert "LIMIT 10" in sql
