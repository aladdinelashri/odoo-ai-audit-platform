from database.compiler.sql_parameter_compiler import SQLParameterCompiler


def test_empty():
    compiler = SQLParameterCompiler()

    plan = {}

    assert compiler.compile(plan) == []


def test_one_value():
    compiler = SQLParameterCompiler()

    plan = {
        "where_values": [
            "posted",
        ]
    }

    assert compiler.compile(plan) == [
        "posted",
    ]


def test_two_values():
    compiler = SQLParameterCompiler()

    plan = {
        "where_values": [
            "posted",
            100,
        ]
    }

    assert compiler.compile(plan) == [
        "posted",
        100,
    ]


def test_boolean():
    compiler = SQLParameterCompiler()

    plan = {
        "where_values": [
            True,
        ]
    }

    assert compiler.compile(plan) == [
        True,
    ]


def test_none():
    compiler = SQLParameterCompiler()

    plan = {
        "where_values": [
            None,
        ]
    }

    assert compiler.compile(plan) == [
        None,
    ]
