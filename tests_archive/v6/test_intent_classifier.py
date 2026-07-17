from database.ai.intent.intent_classifier import IntentClassifier


def test_show():
    c = IntentClassifier()
    assert c.classify("show invoices").intent == "SHOW"


def test_count():
    c = IntentClassifier()
    assert c.classify("count invoices").intent == "COUNT"


def test_sum():
    c = IntentClassifier()
    assert c.classify("sum invoices").intent == "SUM"


def test_average():
    c = IntentClassifier()
    assert c.classify("average invoice amount").intent == "AVERAGE"


def test_min():
    c = IntentClassifier()
    assert c.classify("minimum invoice amount").intent == "MIN"


def test_max():
    c = IntentClassifier()
    assert c.classify("maximum invoice amount").intent == "MAX"


def test_list():
    c = IntentClassifier()
    assert c.classify("list customers").intent == "LIST"


def test_unknown():
    c = IntentClassifier()
    assert c.classify("hello world").intent == "UNKNOWN"
