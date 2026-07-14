from database.compiler.sql_compiler import SQLCompiler


def test_simple_select():
    compiler = SQLCompiler()

    plan = {
        "select": ["*"],
        "from": "account.move",
        "where": [],
        "order": [],
        "limit": 100,
    }

    sql = compiler.compile(plan)

    assert sql == (
        "SELECT *\n"
        "FROM account.move\n"
        "LIMIT 100"
    )


def test_where():
    compiler = SQLCompiler()

    plan = {
        "select": ["*"],
        "from": "account.move",
        "where": [
            "state = %s",
        ],
        "order": [],
        "limit": 100,
    }

    sql = compiler.compile(plan)

    assert "WHERE state = %s" in sql


def test_order():
    compiler = SQLCompiler()

    plan = {
        "select": ["*"],
        "from": "account.move",
        "where": [],
        "order": [
            "create_date DESC",
        ],
        "limit": 100,
    }

    sql = compiler.compile(plan)

    assert "ORDER BY create_date DESC" in sql


def test_no_limit():
    compiler = SQLCompiler()

    plan = {
        "select": ["COUNT(*)"],
        "from": "account.move",
        "where": [],
        "order": [],
        "limit": None,
    }

    sql = compiler.compile(plan)

    assert "LIMIT" not in sql


def test_full_query():
    compiler = SQLCompiler()

    plan = {
        "select": ["SUM(amount_total)"],
        "from": "account.move",
        "where": [
            "state = %s",
            "DATE(create_date)=CURRENT_DATE",
        ],
        "order": [
            "create_date DESC",
        ],
        "limit": 10,
    }

    sql = compiler.compile(plan)

    assert sql.startswith("SELECT SUM(amount_total)")
    assert "FROM account.move" in sql
    assert "WHERE state = %s AND DATE(create_date)=CURRENT_DATE" in sql
    assert "ORDER BY create_date DESC" in sql
    assert sql.endswith("LIMIT 10")
