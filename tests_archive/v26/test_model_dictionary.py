from database.knowledge.model_dictionary import ModelDictionary


def test_add_model():

    dictionary = ModelDictionary()

    dictionary.add(
        model="account.move",
        display_name="Journal Entry",
    )

    assert dictionary.exists("account.move")

    model = dictionary.get("account.move")

    assert model["display_name"] == "Journal Entry"


def test_all_models():

    dictionary = ModelDictionary()

    dictionary.add("account.move", "Journal Entry")
    dictionary.add("res.partner", "Contact")

    assert len(dictionary.all()) == 2
